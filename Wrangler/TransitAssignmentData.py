#
# Original revision: Lisa Zorn 2010-8-5
# based on old "combineTransitDBFs.py"
#
import csv,os,logging,string,sys,traceback,xlrd
from dataTable import DataTable, dbfTableReader, FieldType
from .TransitCapacity import TransitCapacity
from .TransitLine import TransitLine
from .Logger import WranglerLogger
from .Network import Network
from .NetworkException import NetworkException
from collections import defaultdict

print("Importing ", __file__)

__all__ = ['TransitAssignmentData', 'TransitAssignmentDataException']

class TransitAssignmentDataException(Exception): pass

class TransitAssignmentData:
    
    TIMEPERIOD_TO_VEHTYPIDX = { "AM":2, "MD": 4, "PM":3, "EV":4, "EA":4 }

    
    def __init__(self, directory=".", timeperiod="AM", modelType=Network.MODEL_TYPE_CHAMP, 
                 champtype="champ4", muniTEP=True, ignoreModes=[], 
                 system=[], profileNode=False,tpfactor="quickboards",grouping=None,
                 transitCapacity=None,
                 lineLevelAggregateFilename=None, linkLevelAggregateFilename=None):
        """

           * *directory* is the location of the transit assignment files
           * *modelType* should be MODEL_TYPE_CHAMP, MODEL_TYPE_TM1, or MODEL_TYPE_TM2
           * *timeperiod* is a string in ["AM", "MD", "PM", "EV", "EA" ]
           * *champtype* is a string in ["champ4", "champ3", "champ3-sfonly"]
           * *muniTEP* is only important for Muni files, but it matters because vehicle type is different
           * pass *ignoreModes* to ignore some, such as [11,12,13,14,15,16,17] to ignore access/egress/xfer
           * pass *system* to restrict looking only at given systems, e.g. ["SF MUNI", "BART" ]
           * pass *profileNode* to only look at links to or from that node
           * *tpfactor* determines the time period peak hour factor.  Must be one of ```quickboards```
             or ```constant``` or ```constant_with_peaked_muni```.
           * Uses *transitLineToVehicle* and *transitVehicleToCapacity* to map transit lines to vehicle types, 
             and vehicle types to capacities.
           * If *lineLevelAggregateFilename* or *linkLevelAggregateFilename* are passed in, then
             it is assumed that the many transit assignment dbfs have already been aggregated (likely
             by this very class!) and we should just read those instead of doing the work again.
        """
        
             
        # from quickboards
        if tpfactor=="quickboards":
            self.TIMEPERIOD_FACTOR = { "AM":0.44, "MD":0.18, "PM":0.37, "EV":0.22, "EA":0.58 } 
        elif tpfactor=="constant":
            self.TIMEPERIOD_FACTOR ={}
            for tp in ["AM", "MD", "PM", "EV", "EA"]:
                self.TIMEPERIOD_FACTOR[tp] = 1.0/TransitLine.HOURS_PER_TIMEPERIOD[modelType][tp]
        elif tpfactor=="constant_with_peaked_muni":
            # defaults
            self.TIMEPERIOD_FACTOR ={}
            for tp in ["AM", "MD", "PM", "EV", "EA"]:
                self.TIMEPERIOD_FACTOR[tp] = 1.0/TransitLine.HOURS_PER_TIMEPERIOD[modelType][tp]
            # muni peaking
            muni_peaking = {"AM":0.45, # 0.39 / 0.85 (Muni peaking factor from 2010 APC / Muni's capacity ratio)
                            "MD":1/TransitLine.HOURS_PER_TIMEPERIOD[modelType]["MD"],
                            "PM":0.45,
                            "EV":0.2,
                            "EA":1/TransitLine.HOURS_PER_TIMEPERIOD[modelType]["EA"]}
            if modelType == Network.MODEL_TYPE_CHAMP:
                self.TIMEPERIOD_FACTOR[11] = muni_peaking # muni bus
                self.TIMEPERIOD_FACTOR[12] = muni_peaking # muni express bus
                self.TIMEPERIOD_FACTOR[13] = muni_peaking # muni BRT
                self.TIMEPERIOD_FACTOR[14] = muni_peaking # muni cable car
                self.TIMEPERIOD_FACTOR[15] = muni_peaking # muni LRT
            elif modelType == Network.MODEL_TYPE_TM1:
                self.TIMEPERIOD_FACTOR[20]  = muni_peaking # muni cable car
                self.TIMEPERIOD_FACTOR[21]  = muni_peaking # muni local bus
                self.TIMEPERIOD_FACTOR[110] = muni_peaking # muni LRT
        else:
            raise TransitAssignmentDataException("Invalid time period factor "+str(tpfactor))

        self.assigndir  = directory
        self.timeperiod = timeperiod
        self.modelType  = modelType
        self.champtype  = champtype
        self.ignoreModes= ignoreModes
        self.system     = system
        self.profileNode= profileNode
        self.aggregateAll = True # aggregate for A,B?
        if transitCapacity:
            self.capacity   = transitCapacity
        else:
            self.capacity   = TransitCapacity()
        self.csvColnames= None # uninitialized           

        if self.timeperiod not in ["AM", "MD", "PM", "EV", "EA"]:
            raise TransitAssignmentDataException("Invalid timeperiod "+str(timeperiod))
        if self.champtype not in ["champ3","champ4","champ3-sfonly"]:
            raise TransitAssignmentDataException("Invalid champtypte "+str(champtype))

        # supplementary workbooks
        if grouping and (grouping.upper() == "RAPID"):
            self.lineToGroup = self.assignMuniRapid()
        else:
            self.lineToGroup = self.readTransitLineGrouping(mapfile=grouping)


        # Already aggregated up?
        if lineLevelAggregateFilename:
            self.readAggregateDbfs(asgnFileName=lineLevelAggregateFilename,
                                   aggregateFileName=linkLevelAggregateFilename)
            return

        # To determine what files we'll open
        if not 'ALLTRIPMODES' in os.environ:
            raise NetworkException("No ALLTRIPMODES in environment for TransitAssignmentData to decide on input files")
        self.MODES = os.environ["ALLTRIPMODES"].split(" ")
        WranglerLogger.debug("TransitAssignmentData MODES = " + str(self.MODES))

        self.readTransitAssignmentCsvs()

    def readTransitLineGrouping(self, mapfile=None):
        """
        Read the transit line groupings file which assigns a grouping to lines
        """
        if not mapfile: return {}
        
        lineToGroup = {}
        try:
            workbook       = xlrd.open_workbook(filename=mapfile,encoding_override='ascii')
        except:
            print("couldn't find that workbook %s, yo!  No Groupings used!".format(mapefile))
            return lineToGroup
        sheet    = workbook.sheet_by_name("Lookup")
        row = 1
        while (row < sheet.nrows):
            group = sheet.cellvalue(row,1).encode('utf-8')
            self.lineToGroup[lookupsheet.cell_value(row,0).encode('utf-8')]=lookupsheet.cell_value(row,1).encode('utf-8')
            row+=1
        return lineToGroup
    
    def assignMuniRapid(self):
        lineToGroup = {}
        RapidList=["E","J","K","L","M","N",
                   "1","1DRM","1PRS","1STN","1CRN","1SHT",
                   "5","5SHT","5EV","5L",
                   "9","9SHT","9L","9EVE","9X",
                   "14L","14X",
                   "22",
                   "28L",
                   "30","30SHT","30WSQ","30X",
                   "38L",
                   "47",
                   "49","49L",
                   "71","71L"]
        for genericLine in RapidList:
            for dir in ["I","O"]:
                lineToGroup["MUN"+genericLine+dir]="RAPID"
        return lineToGroup


    def initializeFields(self, headerRow=None):
        """
        Initializes the *trnAsgnFields*, *trnAsgnCopyFields*, *trnAsgnAdditiveFields*,
        and *aggregateFields*
        """
        if headerRow:
            self.csvColnames = headerRow
        else:
            self.csvColnames = ["A","B","TIME","MODE", #"FREQ",
                                "PLOT", #"COLOR",
                                "STOP_A","STOP_B","DIST",
                                "NAME", #"SEQ",
                                "OWNER",
                                "AB_VOL","AB_BRDA","AB_XITA","AB_BRDB","AB_XITB",
                                "BA_VOL","BA_BRDA","BA_XITA","BA_BRDB","BA_XITB"]
        
        self.colnameToCsvIndex = dict((self.csvColnames[idx],idx) for idx in range(len(self.csvColnames)))

        # copy these directly
        self.trnAsgnFields = {"A":      'u4',
                              "B":      'u4',
                              "TIME":   'u4',
                              "MODE":   'u1',
                              "PLOT":   'u1',
                              "STOP_A": 'b',
                              "STOP_B": 'b',
                              "DIST":   'u4',
                              "NAME":   'a13',
                              "OWNER":  'a10',
                              }
        self.trnAsgnCopyFields = list(self.trnAsgnFields.keys())
        # these are in the dbf not the csv (grrrr)
        self.trnAsgnFields["FREQ"]      = 'f4'
        self.trnAsgnFields["SEQ"]       = 'u1'
        self.trnAsgnFields["COLOR"]     = 'u1'

        # Lets also ad these for easy joining
        self.trnAsgnFields["AB"]        ='a15'
        self.trnAsgnFields["ABNAMESEQ"] ='a30'
        # Straight lookup based on the line name
        self.trnAsgnFields["GROUP"]     ='a20'
        self.trnAsgnFields["FULLNAME"]  ='a40'
        self.trnAsgnFields["SYSTEM"]    ='a25'
        self.trnAsgnFields["VEHTYPE"]   ='a40'
        self.trnAsgnFields["VEHCAP"]    ='u2'

        # Calculated in the first pass
        self.trnAsgnFields["PERIODCAP"] ='f4'

        # Additive fields are all U4
        #Here, I need to read in if volume is float, if is, flag if it is, write accordingly
        self.trnAsgnAdditiveFields = ["AB_VOL","AB_BRDA","AB_XITA","AB_BRDB","AB_XITB",
                                      "BA_VOL","BA_BRDA","BA_XITA","BA_BRDB","BA_XITB"]
        for field in self.trnAsgnAdditiveFields:
            self.trnAsgnFields[field]='f4'


        # Calculated at the end
        self.trnAsgnFields["LOAD"]      ='f4'

        # aggregate fields
        self.aggregateFields = {"A":    'u4',
                                "B":    'u4',
                                "AB":   'a15',
                                "FREQ": 'f4',        # combined freq
                                "DIST": 'u4',        # should be the same so first
                                "VEHCAP":'u2',      # sum
                                "PERIODCAP":'f4',   # sum
                                "LOAD": 'f4',        # combined
                                "MAXLOAD":'f4',     # max load of any line on the link
                                }
        for field in self.trnAsgnAdditiveFields:
            self.aggregateFields[field]='f4'

    def readTransitAssignmentCsvs(self):
        """
        Read the transit assignment dbfs, the direct output of Cube's transit assignment.
        """
        self.trnAsgnTable   = False
        self.aggregateTable = False
        warnline = {}
        ABNameSeq_List = []  # (A,B,NAME,SEQ) from the dbf/csvs
                
        # open the input assignment files
        for mode in self.MODES:
            if self.modelType == Network.MODEL_TYPE_CHAMP:
                if mode == "WMWVIS":
                    filename = os.path.join(self.assigndir, "VISWMW" + self.timeperiod + ".csv")
                elif mode[1]=="T":
                    filename = os.path.join(self.assigndir, "NS" + mode + self.timeperiod + ".csv")
                else:
                    filename = os.path.join(self.assigndir, "SF" + mode + self.timeperiod + ".csv")
            elif self.modelType == Network.MODEL_TYPE_TM1:
                filename = os.path.join(self.assigndir, "trnlink{}_{}.csv".format(self.timeperiod.lower(), mode))
                
            # Read the DBF file into datatable
            WranglerLogger.info("Reading "+filename)

            # Create our table data structure once
            if mode == self.MODES[0]:
                # figure out how many records
                numrecs = 0
                totalrows = 0
                                
                filereader = csv.reader(open(filename, 'r'), delimiter=',', quoting=csv.QUOTE_NONE)
                for row in filereader:
                    
                    # header row?
                    if row[0]=="A": 
                        self.initializeFields(row)
                        continue
                    elif totalrows==0 and not self.csvColnames:
                        self.initializeFields()

                    
                    totalrows += 1
                    if self.profileNode and \
                       (int(row[self.colnameToCsvIndex["A"]]) != self.profileNode and
                        int(row[self.colnameToCsvIndex["B"]]) != self.profileNode): continue
                    
                    if int(row[self.colnameToCsvIndex["MODE"]]) in self.ignoreModes: continue
                    
                    linename = row[self.colnameToCsvIndex["NAME"]].strip()

                    # exclude this system?
                    (system, vehicletype) = self.capacity.getSystemAndVehicleType(linename, self.timeperiod)

                    if len(self.system)>0 and system not in self.system: continue

                    numrecs += 1
                WranglerLogger.info("Keeping %d records out of %d" % (numrecs, totalrows))
                
                self.trnAsgnTable = DataTable(numRecords=numrecs,
                                              fieldNames=self.trnAsgnFields.keys(),
                                              numpyFieldTypes=list(self.trnAsgnFields.values()))
                ABNameSeqSet = set()
                WranglerLogger.debug("Created dataTable")
            
            # Go through the records
            newrownum = 0  # row number in the trnAsgnTable,ABNameSeq_List -- rows we're keeping
            oldrownum = 0  # row number in the csv,dbf -- all input rows
            
            filereader = csv.reader(open(filename, 'r'), delimiter=',', quoting=csv.QUOTE_NONE)
            # for the first csv only, also read the dbf for the freq and seq fields
            if mode == self.MODES[0]:
                if self.modelType == Network.MODEL_TYPE_CHAMP:
                    indbf = dbfTableReader(os.path.join(self.assigndir, "SFWBW" + self.timeperiod + ".dbf"))
                elif self.modelType == Network.MODEL_TYPE_TM1:
                    indbf = dbfTableReader(os.path.join(self.assigndir, "trnlink{}_{}.dbf".format(self.timeperiod.lower(), mode)))
            else:
                indbf = None
            
            for row in filereader:
                # header row?
                if row[0]=="A": continue
                                                       
                if self.profileNode:
                    if (int(row[self.colnameToCsvIndex["A"]]) != self.profileNode and
                        int(row[self.colnameToCsvIndex["B"]]) != self.profileNode): continue
                    elif int(row[self.colnameToCsvIndex["AB_VOL"]]) > 0:
                        WranglerLogger.info("Link %s %s for mode %s has AB_VOL %s" % 
                                     (row[self.colnameToCsvIndex["A"]], 
                                      row[self.colnameToCsvIndex["B"]], mode, 
                                      row[self.colnameToCsvIndex["AB_VOL"]]))
            
                if int(row[self.colnameToCsvIndex["MODE"]]) in self.ignoreModes:
                    oldrownum += 1
                    continue
                     
                linename = row[self.colnameToCsvIndex["NAME"]].strip()
                
                # exclude this system?
                (system, vehicletype) = self.capacity.getSystemAndVehicleType(linename, self.timeperiod)
                if len(self.system)>0 and system not in self.system: continue
            
                # Initial table fill: Special stuff for the first time through
                if mode == self.MODES[0]:

                    # ------------ these fields just get used directly
                    for field in self.trnAsgnCopyFields:
                        
                        try:
                            # integer fields
                            if self.trnAsgnFields[field][0] in ['u','b']:
                                if row[self.colnameToCsvIndex[field]]=="":
                                    self.trnAsgnTable[newrownum][field] = 0
                                elif field in ['TIME','DIST']:
                                    # backwards compatibility - dbfs were 100ths of a mile/min
                                    self.trnAsgnTable[newrownum][field] = float(row[self.colnameToCsvIndex[field]])*100.0
                                else:
                                    self.trnAsgnTable[newrownum][field] = int(row[self.colnameToCsvIndex[field]])                               
                            # float fields
                            elif self.trnAsgnFields[field][0] == 'f':
                                if row[self.colnameToCsvIndex[field]]=="":
                                    self.trnAsgnTable[newrownum][field] = 0.0
                                else:
                                    self.trnAsgnTable[newrownum][field] = float(row[self.colnameToCsvIndex[field]])
                            # text fields
                            else:
                                self.trnAsgnTable[newrownum][field] = row[self.colnameToCsvIndex[field]]
                        
                        except:
                            WranglerLogger.fatal("Error interpreting field %s: [%s]" % (field, str(self.colnameToCsvIndex[field])))
                            WranglerLogger.fatal("row=%s" % str(row))
                            WranglerLogger.fatal(sys.exc_info()[0])
                            WranglerLogger.fatal(sys.exc_info()[1])
                            WranglerLogger.fatal(traceback.format_exc())
                            print("Error interpreting field %s: [%s]" % (field, str(self.colnameToCsvIndex[field])))
                            sys.exit(2)  
                    # ------------ these fields come from the dbf because they're missing in the csv (sigh)
                    dbfRow = indbf.__getitem__(oldrownum)
                    if int(row[self.colnameToCsvIndex["A"]])<100000:
                        if dbfRow["A"]!=int(row[self.colnameToCsvIndex["A"]]):
                            raise NetworkException("Assertion error for A on row %d: %s != %s" % (oldrownum, str(dbfRow["A"]), str(row[self.colnameToCsvIndex["A"]])))
                    if int(row[self.colnameToCsvIndex["B"]])<100000:
                        if dbfRow["B"]!=int(row[self.colnameToCsvIndex["B"]]):
                            raise NetworkException("Assertion error for B on row %d: %s != %s" % (oldrownum, str(dbfRow["B"]), str(row[self.colnameToCsvIndex["B"]])))
                    self.trnAsgnTable[newrownum]["FREQ"] = dbfRow["FREQ"]
                    self.trnAsgnTable[newrownum]["SEQ"]  = dbfRow["SEQ"]

                    trySeq = dbfRow["SEQ"]
                    # ------------ special one-time computed fields
                    
                    # ABNameSeq is more complicated because we want it to be unique 
                    AB = row[self.colnameToCsvIndex["A"]] + " " + row[self.colnameToCsvIndex["B"]]
                    self.trnAsgnTable[newrownum]["AB"] = AB
                    
                    ABNameSeq = AB + " " + linename
                    if trySeq>0:
                        tryABNameSeq = ABNameSeq + " " + str(trySeq)
                    
                        # This line seems to be a problem... A/B/NAME/SEQ are not unique
                        if tryABNameSeq in ABNameSeqSet:
                            WranglerLogger.warn("Non-Unique A/B/Name/Seq: " + tryABNameSeq + "; faking SEQ!")
                        # Find one that works
                        while tryABNameSeq in ABNameSeqSet:
                            trySeq += 1
                            tryABNameSeq = ABNameSeq + " " + str(trySeq)
                        ABNameSeq = tryABNameSeq
                    self.trnAsgnTable[newrownum]["ABNAMESEQ"] = ABNameSeq
                    ABNameSeqSet.add(ABNameSeq)
                    # WranglerLogger.debug("AABNAMESEQ={} type={}".format(ABNameSeq, type(ABNameSeq)))
                    
                    ABNameSeq_List.append((int(row[self.colnameToCsvIndex["A"]]),
                                           int(row[self.colnameToCsvIndex["B"]]),
                                           row[self.colnameToCsvIndex["NAME"]],
                                           trySeq))
                                        
                    # ------------ straight lookup FULLNAME, VEHTYPE, VEHCAP; easy calc for PERIODCAP
                    self.trnAsgnTable[newrownum]["SYSTEM"]  = system
                    self.trnAsgnTable[newrownum]["VEHTYPE"] = vehicletype

                    self.trnAsgnTable[newrownum]["FULLNAME"] = self.capacity.getFullname(linename, self.timeperiod)
                        
                    try:
                       (vtype, vehcap) = self.capacity.getVehicleTypeAndCapacity(linename, self.timeperiod)

                       self.trnAsgnTable[newrownum]["VEHCAP"] = vehcap
                       self.trnAsgnTable[newrownum]["PERIODCAP"] = TransitLine.HOURS_PER_TIMEPERIOD[self.modelType][self.timeperiod] * 60.0 * vehcap/self.trnAsgnTable[newrownum]["FREQ"]
                    except:
                       self.trnAsgnTable[newrownum]["VEHCAP"] = 0
                       self.trnAsgnTable[newrownum]["PERIODCAP"] = 0

                    # if we still don't have a system, warn
                    if self.trnAsgnTable[newrownum]["SYSTEM"] == "" and linename not in warnline:
                        WranglerLogger.warning("No default system: " + linename)
                        warnline[linename] =1
                    
                    #---------add in any grouping that may want to use
                    if linename in self.lineToGroup:
                        self.trnAsgnTable[newrownum]["GROUP"] = self.lineToGroup[linename]
                    else:
                        self.trnAsgnTable[newrownum]["GROUP"] = ""
                    
                    # initialize additive fields
                    for field in self.trnAsgnAdditiveFields:
                        if row[self.colnameToCsvIndex[field]]=="":
                            self.trnAsgnTable[newrownum][field] = 0.0
                        else:
                            self.trnAsgnTable[newrownum][field] = float(row[self.colnameToCsvIndex[field]])

                    # end initial table fill
                
                # Add in the subsequent assignment files
                else:
                    
                    # print oldrownum, newrownum, ABNameSeq_List[newrownum]
                    # print row[self.colnameToCsvIndex["NAME"]], ABNameSeq_List[oldrownum][2]
                    if ((int(row[self.colnameToCsvIndex["A"]]) != ABNameSeq_List[newrownum][0]) or
                        (int(row[self.colnameToCsvIndex["B"]]) != ABNameSeq_List[newrownum][1])):
                        WranglerLogger.debug(row)
                        WranglerLogger.debug(ABNameSeq_List[newrownum])
                    assert(int(row[self.colnameToCsvIndex["A"]]) == ABNameSeq_List[newrownum][0])
                    assert(int(row[self.colnameToCsvIndex["B"]]) == ABNameSeq_List[newrownum][1])
                    # these don't nec match, can be *32 in ferry skim rather than the bart vehicle name, for example
                    # assert(  row[self.colnameToCsvIndex["NAME"]] == ABNameSeq_List[newrownum][2])
                    
                    ABNameSeq = row[self.colnameToCsvIndex["A"]] + " " + \
                                row[self.colnameToCsvIndex["B"]] + " " + \
                                row[self.colnameToCsvIndex["NAME"]].rstrip()
                    if ABNameSeq_List[newrownum][3]>0:
                        ABNameSeq += " " + str(ABNameSeq_List[newrownum][3])
                    # convert to bytes - the index in the dataTable is a byte string
                    ABNameSeq = ABNameSeq.encode('utf-8')
                    for field in self.trnAsgnAdditiveFields:
                        if row[self.colnameToCsvIndex[field]] !="":
                            self.trnAsgnTable[ABNameSeq][field] += float(row[self.colnameToCsvIndex[field]])
                        
                newrownum += 1   
                oldrownum += 1

            # we're done with this; free it up
            del filereader
            if indbf: 
                del indbf
            
            # Table is created and filled -- set the index
            if mode == self.MODES[0]: 
                try:
                    self.trnAsgnTable.setIndex(fieldName="ABNAMESEQ")
                except:
                    # failure - try to figure out why
                    ABNameSeqList = []
                    for row in self.trnAsgnTable:
                        ABNameSeqList.append(row["ABNAMESEQ"])
                    ABNameSeqList.sort()
                    for idx in range(len(ABNameSeqList)-1):
                        if ABNameSeqList[idx]==ABNameSeqList[idx+1]:
                            WranglerLogger.fatal("Duplicate ABNAMESEQ at idx %d : [%s]" % (idx,ABNameSeqList[idx]))
                    exit(1)

        # ok the table is all filled in -- fill in the LOAD
        for row in self.trnAsgnTable:
            if row["VEHCAP"] == 0: continue
            tpfactor = self.TIMEPERIOD_FACTOR[self.timeperiod]
            
            # mode-specific peaking factor will over-ride
            if row["MODE"] in self.TIMEPERIOD_FACTOR:
                tpfactor = self.TIMEPERIOD_FACTOR[row["MODE"]][self.timeperiod]
                
            row["LOAD"] = row["AB_VOL"] * tpfactor * row["FREQ"] / (60.0 * row["VEHCAP"])

        # build the aggregate table for key="A B"
        if self.aggregateAll:
            self.buildAggregateTable()
        
    def buildAggregateTable(self):
        # first find how big it is
        ABSet = set()       
        for row in self.trnAsgnTable:
            ABSet.add(row["AB"])
        
        self.aggregateTable = DataTable(numRecords=len(ABSet),
                                        fieldNames=list(self.aggregateFields.keys()),
                                        numpyFieldTypes=list(self.aggregateFields.values()))
        ABtoRowIndex = {}
        rowsUsed = 0
        for row in self.trnAsgnTable:
            if row["AB"] not in ABtoRowIndex:
                rowIndex = rowsUsed
                self.aggregateTable[rowIndex]["AB"]     = row["AB"]
                self.aggregateTable[rowIndex]["A"]      = row["A"]
                self.aggregateTable[rowIndex]["B"]      = row["B"]
                self.aggregateTable[rowIndex]["DIST"]   = row["DIST"]
                self.aggregateTable[rowIndex]["FREQ"]       = 0.0
                self.aggregateTable[rowIndex]["PERIODCAP"]  = 0.0
                self.aggregateTable[rowIndex]["LOAD"]       = 0.0
                self.aggregateTable[rowIndex]["MAXLOAD"]    = 0.0
                for field in self.trnAsgnAdditiveFields:    # sum
                    self.aggregateTable[rowIndex][field] = 0.0
                ABtoRowIndex[row["AB"]] = rowsUsed
                rowsUsed += 1
            else:
                rowIndex = ABtoRowIndex[row["AB"]]
            
            for field in self.trnAsgnAdditiveFields:    # sum
                self.aggregateTable[rowIndex][field] += row[field]
            self.aggregateTable[rowIndex]["AB_VOL"] += row["AB_VOL"]
            self.aggregateTable[rowIndex]["BA_VOL"] += row["BA_VOL"]
            self.aggregateTable[rowIndex]["PERIODCAP"] += row["PERIODCAP"]
            self.aggregateTable[rowIndex]["MAXLOAD"] = max(row["LOAD"], self.aggregateTable[rowIndex]["MAXLOAD"])
            self.aggregateTable[rowIndex]["FREQ"] += 1/row["FREQ"]  # combining -- will take reciprocal later
        
        self.aggregateTable.setIndex(fieldName="AB")

        count=0
        for row in self.aggregateTable:
            count += 1
            if row["FREQ"]>0: 
                row["FREQ"] = 1/row["FREQ"]
            if row["PERIODCAP"]>0:
                row["LOAD"] = float(row["AB_VOL"]) / row["PERIODCAP"]
                # print row["LOAD"]
        WranglerLogger.debug("count "+str(count)+" lines in aggregate table")

    def calculateFleetCharacteristics(self):
        """ Calculates the fleet characteristics - vehicle hours and vehicle miles - by vehicle type
        """
        self.vehicleHours = defaultdict(float)
        self.vehicleMiles = defaultdict(float)
        for key in self.trnAsgnTable._index.keys():
            record = self.trnAsgnTable[key]
            # don't process access, egress and transfer links
            if record["MODE"]>9: continue
            
            # index by system, then by vehicle type
            indexstr = record["SYSTEM"] + "," + record["VEHTYPE"]
            
            # number of vehicles = duration * 60 min/hour / freq
            numveh = TransitLine.HOURS_PER_TIMEPERIOD[self.modelType][self.timeperiod] * 60.0 / record["FREQ"]
            # vehicle hours = (# of vehicles) x time per link, or TIME * 1 hour/6000 hundredths of min
            self.vehicleHours[indexstr] += numveh*(record["TIME"]/6000.0)
            # vehicle miles = (# of vehicles) x dist per link, or DIST * 1 mile/100 hundredths of mile
            self.vehicleMiles[indexstr] += numveh*(record["DIST"]/100.0)

    def readAggregateDbfs(self, asgnFileName, aggregateFileName=None):
        """
        This is essentially the reverse of writeDbfs() below.
        """
        self.initializeFields()  # this may be unnecessary

        self.trnAsgnTable = dbfTableReader(asgnFileName)
        self.trnAsgnTable.setIndex(fieldName="ABNAMESEQ")

        # a little bit of cleanup
        headerTuples = []
        for headerFieldType in self.trnAsgnTable.header:
            headerTuples.append(headerFieldType.toTuple())

        # rstrip spaces off the end of the text fields
        for row in self.trnAsgnTable:
            for headerTuple in headerTuples:
                if headerTuple[1] == 'C': row[headerTuple[0]] = string.rstrip(row[headerTuple[0]])

        # this is the index!
        self.trnAsgnTable.setIndex(fieldName="ABNAMESEQ")

        # the link-level aggregate table
        if not aggregateFileName:
            self.aggregateAll   = False
            self.aggregateTable = False
            return

        self.aggregateAll   = True
        self.aggregateTable = dbfTableReader(aggregateFileName)

        # cleanup again
        headerTuples = []
        for headerFieldType in self.aggregateTable.header:
            headerTuples.append(headerFieldType.toTuple())

        # rstrip spaces off the end of the text fields
        for row in self.aggregateTable:
            for headerTuple in headerTuples:
                if headerTuple[1] == 'C': row[headerTuple[0]] = string.rstrip(row[headerTuple[0]])

    def writePnrDrivers(self, pnrFileName):
        """
        Writes PNR Auto Trips to DBF with fields:
            ZONE 
            PNR
            TO-DEMAND
            FR-DEMAND
        """
        self.pnrFields = {"ZONE": 'u4',
                          "PNR" :  'u4',
                          "TO"  :  'f4',
                          "FROM":  'f4'
                          }
        self.pnrTable = DataTable(fieldNames=self.pnrFields.keys(),
                                  numpyFieldTypes=self.trnAsgnFields.values())
        
        
    def writeDbfs(self, asgnFileName, aggregateFileName=None):
        """
        Writes the line-level (key=A,B,NAME,SEQ) dbf to *asgnFileName*, and
        write the link-level (key=A,B) aggregated dbf to *aggregateFileName*.
        """
        addtype     = "F"
        addlen      = 9
        addnumdec   = 2

        # line-level
        self.trnAsgnTable.header = \
            (FieldType("A",          "N", 7, 0),
             FieldType("B",          "N", 7, 0),
             FieldType("TIME",       "N", 5, 0),
             FieldType("MODE",       "N", 3, 0),
             FieldType("FREQ",       "F", 6, 2),
             FieldType("PLOT",       "N", 1, 0),
             FieldType("COLOR",      "N", 2, 0),
             FieldType("STOP_A",     "N", 1, 0),
             FieldType("STOP_B",     "N", 1, 0),
             FieldType("DIST",       "N", 4, 0),
             FieldType("NAME",       "C", 13,0),
             FieldType("SEQ",        "N", 3, 0),
             FieldType("OWNER",      "C", 10,0),
             FieldType("AB",         "C", 15,0),
             FieldType("ABNAMESEQ",  "C", 30,0),
             FieldType("FULLNAME",   "C", 40,0),
             FieldType("SYSTEM",     "C", 25,0),
             FieldType("GROUP",      "C", 20,0),
             FieldType("VEHTYPE",    "C", 40,0),
             FieldType("VEHCAP",     "F", 8, 2),
             FieldType("PERIODCAP",  "F", 15, 2),
             FieldType("LOAD",       "F", 7, 3),
             FieldType("AB_VOL",     addtype, addlen, addnumdec),
             FieldType("AB_BRDA",    addtype, addlen, addnumdec),
             FieldType("AB_XITA",    addtype, addlen, addnumdec),
             FieldType("AB_BRDB",    addtype, addlen, addnumdec),
             FieldType("AB_XITB",    addtype, addlen, addnumdec),
             FieldType("BA_VOL",     addtype, addlen, addnumdec),
             FieldType("BA_BRDA",    addtype, addlen, addnumdec),
             FieldType("BA_XITA",    addtype, addlen, addnumdec),
             FieldType("BA_BRDB",    addtype, addlen, addnumdec),
             FieldType("BA_XITB",    addtype, addlen, addnumdec)
             )
        self.trnAsgnTable.writeAsDbf(asgnFileName)

        if aggregateFileName==None: return

        if not self.aggregateTable:
            self.buildAggregateTable()

        self.aggregateTable.header = \
            (FieldType("A",         "N", 7, 0),
             FieldType("B",         "N", 7, 0),
             FieldType("AB",        "C", 15,0),
             FieldType("FREQ",      "F", 6, 2),
             FieldType("DIST",      "N", 4, 0),
             FieldType("VEHCAP",    "F", 8, 2),
             FieldType("PERIODCAP", "F", 15, 2),
             FieldType("LOAD",      "F", 7, 3),
             FieldType("MAXLOAD",   "F", 7, 3),
             FieldType("AB_VOL",    addtype, addlen, addnumdec),
             FieldType("AB_BRDA",   addtype, addlen, addnumdec),
             FieldType("AB_XITA",   addtype, addlen, addnumdec),
             FieldType("AB_BRDB",   addtype, addlen, addnumdec),
             FieldType("AB_XITB",   addtype, addlen, addnumdec),
             FieldType("BA_VOL",    addtype, addlen, addnumdec),
             FieldType("BA_BRDA",   addtype, addlen, addnumdec),
             FieldType("BA_XITA",   addtype, addlen, addnumdec),
             FieldType("BA_BRDB",   addtype, addlen, addnumdec),
             FieldType("BA_XITB",   addtype, addlen, addnumdec)
             )
        self.aggregateTable.writeAsDbf(aggregateFileName)
        WranglerLogger.info("Wrote aggregate table as {}".format(aggregateFileName))
    
    def numBoards(self, linename, nodenum, nodenum_next, seq):
        """ linename is something like MUN30I; it includes the direction.
            nodenum is the node in question, nodenum_next is the next node in the line file
            seq is for the sequence of (nodenum,nodenum_next). e.g. seq starts at 1 for the first link and increments
            TODO: what if the line is two-way?
            Returns an int representing number of boards in the whole time period.
            Throws an exception if linename isnt recognized or if nodenum is not part of the line.
        """
        key = "%d %d %s %d" % (nodenum, nodenum_next, linename.upper(), seq)
        if key in self.trnAsgnTable:
            return self.trnAsgnTable[key]["AB_BRDA"]
        raise TransitAssignmentDataException("key [%s] not found in transit assignment data" % key)
    
    def numExits(self, linename, nodenum_prev, nodenum, seq):
        """ See numBoards
        """
        key = "%d %d %s %d" % (nodenum_prev, nodenum, linename.upper(), seq)
        if key in self.trnAsgnTable:
            return self.trnAsgnTable[key]["AB_XITB"]
        raise TransitAssignmentDataException("key [%s] not found in transit assignment data" % key)
    
    def loadFactor(self, linename, a,b, seq):
        """ Returns a fraction: peak hour pax per vehicle / vehicle capacity
            e.g. 1.0 is a packed vehicle
            
            NOTE this assumes a distribution pax over the time period.  For now, we'll use
            the simple peak hour factors that quickboards uses but this could be refined
            in the future.
        """
        key = "%d %d %s %d" % (a, b, linename.upper(), seq)
        if key not in self.trnAsgnTable:
            raise TransitAssignmentDataException("Key [%s] not found in transit assignment data" % key)
        return self.trnAsgnTable[key]["LOAD"]
    
    def linkVolume(self,linename,a,b,seq):
        """Return number of people on a given link a b"""
        key = "%d %d %s %d" % (a, b, linename.upper(), seq)
        if key not in self.trnAsgnTable:
            raise TransitAssignmentDataException("Key [%s] not found in transit assignment data" % key)
        return self.trnAsgnTable[key]["AB_VOL"]
    
    def linkTime(self,linename,a,b,seq): 
        """Return time in minutes on a given link a b"""
        key = "%d %d %s %d" % (a, b, linename.upper(), seq)
        if key not in self.trnAsgnTable:
            raise TransitAssignmentDataException("Key [%s] not found in transit assignment data" % key)
        return self.trnAsgnTable[key]["TIME"]

    
    def linkDistance(self,linename,a,b,seq):
        """Return distance in miles on a given link a b"""
        key = "%d %d %s %d" % (a, b, linename.upper(), seq)
        if key not in self.trnAsgnTable:
            raise TransitAssignmentDataException("Key [%s] not found in transit assignment data" % key)
        return self.trnAsgnTable[key]["DIST"]
        

# Not complete.... TODO if it makes sense....
class DailyTransitAssignmentData:
    
    def __init__(self, tadAM, tadMD, tadPM, tadEV, tadEA):
        """
        For aggregating into a single version!
        """
        keys = set(tadAM.trnAsgnTable._index.keys())
        keys = keys.union(tadMD.trnAsgnTable._index.keys())
        keys = keys.union(tadPM.trnAsgnTable._index.keys())
        keys = keys.union(tadEV.trnAsgnTable._index.keys())
        keys = keys.union(tadEA.trnAsgnTable._index.keys())

        # self.trnAsgnTable = DataTable(numRecords=numrecs,
        #                              fieldNames=self.trnAsgnFields.keys(),
        #                              numpyFieldTypes=self.trnAsgnFields.values())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        datefmt='%Y-%b-%d %H:%M:%S',)

    if False:
        tad1 = TransitAssignmentData(directory=r"X:\Projects\GHGReductionCE\2035",
                                     timeperiod="AM",
                                     tpfactor="constant")
        print("Test1: vol for MUNKO, 13401-13402, 1) is ", tad1.linkVolume("MUNKO", 13401, 13402, 1))
        tad1.writeDbfs(asgnFileName=r"X:\lmz\AM_asgn.dbf", aggregateFileName=r"X:\lmz\AM_agg.dbf")
        tad1 = False

    if False:
        tad2 = TransitAssignmentData(directory=r"X:\Projects\GHGReductionCE\2035",
                                    timeperiod="AM",
                                    tpfactor="constant")
        print("Test2: vol for MUNKO, 13401-13402, 1) is ", tad2.linkVolume("MUNKO", 13401, 13402, 1))
        tad2.writeDbfs(asgnFileName=r"X:\lmz\AM_asgnF.dbf", aggregateFileName=r"X:\lmz\AM_aggF.dbf")
        tad2 = False

    if True:
        tad3 = TransitAssignmentData(timeperiod="AM",
                                     tpfactor="constant",
                                     lineLevelAggregateFilename=r"X:\lmz\AM_asgn.dbf",
                                     linkLevelAggregateFilename=r"X:\lmz\AM_agg.dbf")
        print("Test3: vol for MUNKO, 13401-13402, 1) is ", tad3.linkVolume("MUNKO", 13401, 13402, 1))
        tad3 = False

    if True:
        tad4 = TransitAssignmentData(timeperiod="AM",
                                     tpfactor="constant",
                                     lineLevelAggregateFilename=r"X:\lmz\AM_asgnF.dbf",
                                     linkLevelAggregateFilename=r"X:\lmz\AM_aggF.dbf")
        print("Test4: vol for MUNKO, 13401-13402, 1) is ", tad4.linkVolume("MUNKO", 13401, 13402, 1))
        tad4 = False
