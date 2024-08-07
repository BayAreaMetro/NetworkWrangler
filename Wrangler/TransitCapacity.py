import copy,csv,os,re,string
from .Logger import WranglerLogger
from .NetworkException import NetworkException

__all__ = ['TransitCapacity']


class TransitCapacity:
    """
    Simple class for accessing and mutating (and reading and writing)
    Transit Capacity information
    """
    
    TIMEPERIOD_TO_VEHTYPIDX = { "AM":2, "MD": 4, "PM":3, "EV":4, "EA":4 }

    # for self.linenameToAttributes
    # linename -> [ system, full name, AM vehicletype, PM vehiceltype, OP vehicle type ]
    ATTR_SYSTEM     = 0
    ATTR_FULLNAME   = 1
    ATTR_AMVEHTYPE  = 2
    ATTR_PMVEHTYPE  = 3
    ATTR_OPVEHTYPE  = 4

    # for self.vehicleTypeToDelays
    DELAY_SIMPLE    = 0
    DELAY_CONST     = 1
    DELAY_PERBOARD  = 2
    DELAY_PERALIGHT = 3

    def __init__(self, directory=".",
                 transitLineToVehicle="transitLineToVehicle.csv",
                 transitVehicleToCapacity="transitVehicleToCapacity.csv",
                 transitPrefixToVehicle="transitPrefixToVehicle.csv"):
        """
        Uses *transitLineToVehicle* and *transitVehicleToCapacity* to map transit lines to vehicle types, 
        and vehicle types to capacities.
        """
        self.vehicleTypeToCapacity  = {}
        self.vehicleTypeToDelays    = {}
        self.linenameToAttributes   = {}
        self.linenameToSimple       = {}
        self.prefixToVehicleType    = {}

        self.readTransitLineToVehicle(directory, filename=transitLineToVehicle)
        self.readTransitVehicleToCapacity(directory, filename=transitVehicleToCapacity)
        self.readTransitPrefixToVehicle(directory, filename=transitPrefixToVehicle)

    def readTransitVehicleToCapacity(self, directory=".", filename="transitVehicleToCapacity.csv"):
        """
        Populate a self.vehicleTypeToCapacity from *filename*:
            vehicletype -> 100% capacity (a float)
            e.g. "LRV2" -> 238.0
            
        Also populate a self.vehicleTypeToDelays:
            vehicletype -> [ simple delay, 
                             complex delay const,
                             complex delay per board,
                             complex delay per alight ]
        """
        f = open(os.path.join(directory,filename), 'r')
        lines = f.readlines()
        f.close()
        
        for line in lines:
            tokens = line.split(",")
            if tokens[0]=="VehicleType": continue # header
            vtype = tokens[0]
            self.vehicleTypeToCapacity[vtype] = float(tokens[1])
            
            if len(tokens) > 4:
                self.vehicleTypeToDelays[vtype] = [0, 0, 0, 0]
                self.vehicleTypeToDelays[vtype][TransitCapacity.DELAY_SIMPLE   ] = float(tokens[4])
                self.vehicleTypeToDelays[vtype][TransitCapacity.DELAY_CONST    ] = float(tokens[5])
                self.vehicleTypeToDelays[vtype][TransitCapacity.DELAY_PERBOARD ] = float(tokens[6])
                self.vehicleTypeToDelays[vtype][TransitCapacity.DELAY_PERALIGHT] = float(tokens[7])
            
        # print "vehicleTypeToCapacity = " + str(self.vehicleTypeToCapacity)
        # print "vehicleTypeToDelays = " + str(self.vehicleTypeToDelays)

    def writeTransitVehicleToCapacity(self, directory=".", filename="transitVehicleToCapacity.csv"):
        """
        Writes it out in the same format
        """
        f = open(os.path.join(directory,filename), 'w')
        f.write("VehicleType,100%Capacity,85%Capacity,VehicleCategory,SimpleDelayPerStop,ConstDelayPerStop,DelayPerBoard,DelayPerAlight\n")
        for vehicleType in sorted(self.vehicleTypeToCapacity.keys()):
            f.write(vehicleType+",")
            f.write("%d,%d" % (self.vehicleTypeToCapacity[vehicleType],
                               0.85*self.vehicleTypeToCapacity[vehicleType]))
            if vehicleType in self.vehicleTypeToDelays:
                f.write(",%s" % vehicleType) # this is supposed to be vehicle category but we didn't keep that around since we don't use it
                f.write(",%.3f,%.3f,%.3f,%.3f" % (self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_SIMPLE   ],
                                                  self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_CONST    ],
                                                  self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_PERBOARD ],
                                                  self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_PERALIGHT]))
            f.write("\n")
        f.close()
    
    def readTransitLineToVehicle(self, directory=".", filename="transitLineToVehicle.csv"):
        """
        Populate self.linenameToAttributes from *filename*:
           linename -> [ system, full name, AM vehicletype, PM vehicletype, OP vehicle type ]
           e.g. "MUNTI" -> [ "SF MUNI", "T - THIRD STREET", "LRV2", "LRV2", "LRV2" ]
        Also self.linenameToSimple, but it's currently unused...
           linename -> [ stripped, simplename ]
           e.g. "MUN91I" -> [ "91I", "91" ]
        """
        l2vReader = csv.reader(open(os.path.join(directory,filename)))
        for name,system,stripped,simplename,fullLineName,vehicleTypeAM,vehicleTypePM,vehicleTypeOP in l2vReader:
            self.linenameToAttributes[name.upper()] = [system, fullLineName, vehicleTypeAM,vehicleTypePM,vehicleTypeOP]
            self.linenameToSimple[name.upper()] = [stripped, simplename]
        # print "linenameToAttributes = " + str(self.linenameToAttributes)

    def writeTransitLineToVehicle(self, directory=".", filename="transitLineToVehicle.csv"):
        """
        Writes it out in the same format
        """
        f = open(os.path.join(directory,filename), 'w')
        f.write("Name,System,Stripped,Line,FullLineName,AM VehicleType,PM VehicleType,OP Vehicle Type\n")
        for linename in sorted(self.linenameToAttributes.keys()):
            f.write(linename + ",")
            f.write(self.linenameToAttributes[linename][TransitCapacity.ATTR_SYSTEM] + ",")
            f.write(self.linenameToSimple[linename][0] + ",")       # stripped
            f.write(self.linenameToSimple[linename][1] + ",")       # simplename
            f.write(self.linenameToAttributes[linename][TransitCapacity.ATTR_FULLNAME]+",")
            f.write(self.linenameToAttributes[linename][TransitCapacity.ATTR_AMVEHTYPE]+",")
            f.write(self.linenameToAttributes[linename][TransitCapacity.ATTR_PMVEHTYPE]+",")
            f.write(self.linenameToAttributes[linename][TransitCapacity.ATTR_OPVEHTYPE]+"\n")
        f.close()

    def readTransitPrefixToVehicle(self, directory=".", filename="transitPrefixToVehicle.csv"):
        """
        Populate self.prefixToVehicleType from *filename*:
            prefix -> [ system, vehicletype ]
        """
        p2vReader = csv.reader(open(os.path.join(directory,filename)))
        for prefix, system, vehicleType in p2vReader:
            self.prefixToVehicleType[prefix] = [system, vehicleType]

    def writeTransitPrefixToVehicle(self, directory=".", filename="transitPrefixToVehicle.csv"):
        """
        Writes it out in the same format
        """
        f = open(os.path.join(directory,filename), 'w')
        f.write("Prefix,System,VehicleType\n")
        for prefix in sorted(self.prefixToVehicleType.keys()):
            f.write(prefix + ",")
            f.write(self.prefixToVehicleType[prefix][0] + ",")      # system
            f.write(self.prefixToVehicleType[prefix][1] + "\n")   # vehicleType
        f.close()
        
    def getSystemAndVehicleType(self, linename, timeperiod):
        """
        Convenience function.  Returns tuple: best guess of (system, vehicletype)
        """
        linenameU = linename.upper()
        if linenameU in self.linenameToAttributes:
            return (self.linenameToAttributes[linenameU][TransitCapacity.ATTR_SYSTEM], 
                    self.linenameToAttributes[linenameU][TransitCapacity.TIMEPERIOD_TO_VEHTYPIDX[timeperiod]])

        if linename[:4] in self.prefixToVehicleType:
            return ( self.prefixToVehicleType[linenameU[:4]][0], self.prefixToVehicleType[linenameU[:4]][1])

        if linename[:3] in self.prefixToVehicleType:
            return ( self.prefixToVehicleType[linenameU[:3]][0], self.prefixToVehicleType[linenameU[:3]][1])

        return ("", "")


    def getVehicleTypeAndCapacity(self, linename, timeperiod):
        """ returns (vehicletype, vehiclecapacity)
        """        
        (system, vehicleType) = self.getSystemAndVehicleType(linename, timeperiod)
        
        if vehicleType not in self.vehicleTypeToCapacity:
            raise NetworkException("Vehicle type [%s] of system [%s] characteristics unknown; line name = [%s]" % (vehicleType, system, linename.upper()))

        capacity = self.vehicleTypeToCapacity[vehicleType]
        return (vehicleType, capacity)

    def getFullname(self, linename, timeperiod):
        """
        Returns best guess of fullname, or empty string if unknown
        """
        linenameU = linename.upper()
        if linenameU in self.linenameToAttributes:
            return self.linenameToAttributes[linenameU][TransitCapacity.ATTR_FULLNAME]
        else:
            return ""

    def getSimpleDwell(self, linename, timeperiod):
        """
        Returns a number
        """
        (system, vehicleType) = self.getSystemAndVehicleType(linename, timeperiod)
        if vehicleType not in self.vehicleTypeToDelays:
            raise NetworkException("Vehicle type [%s] of system [%s] simple dwell unknown; line name = [%s]" % (vehicleType, system, linename.upper()))

        return self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_SIMPLE]

    def getComplexDwells(self, linename, timeperiod):
        """
        Returns (constant, perboard, peralight), all three are numbers
        """
        (system, vehicleType) = self.getSystemAndVehicleType(linename, timeperiod)
        if vehicleType not in self.vehicleTypeToDelays:
            raise NetworkException("Vehicle type [%s] of system [%s] complex dwell unknown; line name = [%s]" % (vehicleType, system, linename.upper()))

        return (self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_CONST],
                self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_PERBOARD],
                self.vehicleTypeToDelays[vehicleType][TransitCapacity.DELAY_PERALIGHT])        

    def addVehicleType(self, newVehicleType, newVehicleCapacity):
        """
        Self explanatory
        """
        self.vehicleTypeToCapacity[newVehicleType] = newVehicleCapacity
        if newVehicleType not in self.vehicleTypeToDelays:
            self.vehicleTypeToDelays[newVehicleType] = [0, 0, 0, 0]

    def addLinenameFromTemplate(self, newLine, templateLine):
        """
        Dupe the entry in self.linenameToAttributes for template into newline
        """
        if templateLine not in self.linenameToAttributes:
            raise NetworkException("addLinename with unknown templateLine %s for %s" % (templateLine, newLine))

        self.linenameToAttributes[newLine] = copy.deepcopy(self.linenameToAttributes[templateLine])
        self.linenameToSimple[newLine]     = copy.deepcopy(self.linenameToSimple[templateLine])

    def addLineName(self, newLine, system, fullname, vehicletype_AM, vehicletype_PM, vehicletype_OP):
        """
        Adds a new line with the given vehicle type information
        """
        self.linenameToAttributes[newLine] = [system, fullname, vehicletype_AM, vehicletype_PM, vehicletype_OP]
        self.linenameToSimple[newLine]     = [fullname, fullname]

    def setAllVehicleTypes(self, linename, vehicleType, lineNameIsRegex = False):
        """
        Simple method to set the vehicle types for this line name.
        *linename* is a string; pass *lineNameIsRegex* to interpret it as a regex
        """
        self.setVehicleTypes(linename,
                             vehicleType_AM=vehicleType, 
                             vehicleType_PM=vehicleType,
                             vehicleType_OP=vehicleType,
                             lineNameIsRegex=lineNameIsRegex)
    
    def setVehicleTypeForPrefix(self, prefix, system, vehicleType):
        """
        Sets the vehicle type for the given prefix.
        """
        if vehicleType not in self.vehicleTypeToCapacity:
            WranglerLogger.warn("Setting vehicle type for prefix {} but vehicleType {} unknown" % (prefix, vehicleType))

        if prefix in self.prefixToVehicleType.keys():
            WranglerLogger.debug("Overwriting system/vehicle type for prefix {}.  Was {}/{}, setting to {}/{}".format(prefix, 
                                 self.prefixToVehicleType[prefix][0], self.prefixToVehicleType[prefix][1], system, vehicleType))
        # prefix -> [ system, vehicletype ]
        self.prefixToVehicleType[prefix] = [system, vehicleType]

    def setVehicleTypes(self, linename, vehicleType_AM, vehicleType_PM, vehicleType_OP, lineNameIsRegex = False):
        """
        Sets the vehicle types for this line name.
        *linename* is a string; pass *lineNameIsRegex* to interpret it as a regex
        """
        if vehicleType_AM not in self.vehicleTypeToCapacity:
            WranglerLogger.warn("Setting vehicle type for line %s but vehicleType %s unknown" % (linename, vehicleType_AM))
        if vehicleType_PM not in self.vehicleTypeToCapacity:
            WranglerLogger.warn("Setting vehicle type for line %s but vehicleType %s unknown" % (linename, vehicleType_PM))
        if vehicleType_OP not in self.vehicleTypeToCapacity:
            WranglerLogger.warn("Setting vehicle type for line %s but vehicleType %s unknown" % (linename, vehicleType_OP))
       

        if lineNameIsRegex:
            num_updated = 0
            linename_re = re.compile(linename, flags=re.IGNORECASE)
            for name in self.linenameToAttributes.keys():
                if re.search(linename_re, name):
                    self.linenameToAttributes[name][TransitCapacity.ATTR_AMVEHTYPE] = vehicleType_AM
                    self.linenameToAttributes[name][TransitCapacity.ATTR_PMVEHTYPE] = vehicleType_PM
                    self.linenameToAttributes[name][TransitCapacity.ATTR_OPVEHTYPE] = vehicleType_OP
                    num_updated += 1

            if num_updated==0:
                WranglerLogger.warn("setVehicleTypes called with lineNameIsRegex and no matching configuration for line name {}".format(linename))
        else:
            if linename.upper() not in self.linenameToAttributes:
                raise NetworkException("TransitCapacity: setAllVehicleTypes for unknown linename %s" % linename)
                
            self.linenameToAttributes[linename.upper()][TransitCapacity.ATTR_AMVEHTYPE] = vehicleType_AM
            self.linenameToAttributes[linename.upper()][TransitCapacity.ATTR_PMVEHTYPE] = vehicleType_PM
            self.linenameToAttributes[linename.upper()][TransitCapacity.ATTR_OPVEHTYPE] = vehicleType_OP
    