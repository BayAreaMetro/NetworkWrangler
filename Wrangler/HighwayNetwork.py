import collections, csv, os, re, shutil, subprocess, time
import copy
from socket         import gethostname, getfqdn

from .HwySpecsRTP import HwySpecsRTP
from .Logger import WranglerLogger
from .Network import Network
from .NetworkException import NetworkException

__all__ = ['HighwayNetwork']

class HighwayNetwork(Network):
    """
    Representation of a roadway network.
    """
    cube_hostnames = None

    @staticmethod
    def getCubeHostnames():
        """
        Cube hostnames in Y:\COMMPATH\HostnamesWithCube.txt
        """
        # got them already
        if HighwayNetwork.cube_hostnames: return HighwayNetwork.cube_hostnames

        fqdn = getfqdn().lower() # fully qualified domain name

        # at mtc, assume cube license is available
        if fqdn.endswith("mtc.ca.gov"):
            HighwayNetwork.cube_hostnames = [ gethostname().lower() ]
            return HighwayNetwork.cube_hostnames

        # read them
        HighwayNetwork.cube_hostnames = []
        env = copy.copy(os.environ)
        f = open(env['CUBE_HOST_FILE'])
        for line in f:
            if line[0] == "#": continue
            HighwayNetwork.cube_hostnames.append(line.split()[0])  # use the first token of non-comment lines
        f.close()
        return HighwayNetwork.cube_hostnames

    def __init__(self, modelType, modelVersion, basenetworkpath, networkBaseDir=None, networkProjectSubdir=None,
                 networkSeedSubdir=None, networkPlanSubdir=None, isTiered=False, tag=None,
                 hwyspecsdir=None, hwyspecs=None, tempdir=None, networkName=None, tierNetworkName=None):
        """
        *basenetworkpath* should be a starting point for this network, and include a ``FREEFLOW.net``,
        as well as ``turns[am,pm,op].pen`` files.
        Also a shapefile export: FREEFLOW.[dbf,prj,shp] and FREEFLOW_nodes.[dbf,prj,shp]

        *isTiered*: when False, checks out the *basenetworkpath* from Y:\networks.  When True,
        expects the basenetwork path to be a fullpath and uses that.  Can optionally specify tierNetworkName
        (an alternative to `FREEFLOW.net`.)

        *tag*: when not *isTiered*, a tag can optionally be used for cloning the base network
        
        *hwyspecs*, if passed in, should be an instance of :py:class:`HwySpecsRTP`.  It
        is only used for logging.
        """
        Network.__init__(self, modelType, modelVersion, networkBaseDir, networkProjectSubdir, networkSeedSubdir,
                         networkPlanSubdir, networkName)
        
        if isTiered:
            (head,tail) = os.path.split(basenetworkpath)
            self.applyBasenetwork(head,tail,None, tierNetworkName)
        else:
            self.applyingBasenetwork = True
            self.cloneAndApplyProject(networkdir=basenetworkpath,tempdir=tempdir, projtype='seed', tag=tag)

        # keep a reference of the hwyspecsrtp for logging
        self.hwyspecsdir = hwyspecsdir
        self.hwyspecs = hwyspecs
        
    def applyBasenetwork(self, parentdir, networkdir, gitdir, tierNetworkName):
        
        # copy the base network file to my workspace
        tierNetwork = os.path.join(parentdir,networkdir,tierNetworkName if tierNetworkName else "FREEFLOW.net")
        WranglerLogger.debug("Using tier network %s" % tierNetwork)
        shutil.copyfile(tierNetwork,"FREEFLOW.BLD")
        for filename in ["turnsam.pen",         "turnspm.pen",          "turnsop.pen",    "tolls.csv"]:
            try:
                shutil.copyfile(os.path.join(parentdir,networkdir,filename), filename)
            except:
                WranglerLogger.warn("Couldn't find file {} -- Touching an empty file".format(filename))
                # touch a blank file
                with open(filename, 'a'): os.utime(filename, None)

        # done
        self.applyingBasenetwork = False

    def saveNetworkFiles(self, suffix, to_suffix):
        """
        Since roadway networks are not stored in memory but in files, this is useful
        for when the network builder is doing something tricky.
        """
        for filename in ["FREEFLOW.BLD", "turnsam.pen", "turnspm.pen", "turnsop.pen", "tolls.csv"]:
            if to_suffix:
                shutil.copy2(src=filename, dst="{}{}".format(filename, suffix))
                WranglerLogger.debug("Copying {:20} to {}{}".format(filename, filename, suffix))
            else:
                shutil.copy2(src="{}{}".format(filename, suffix), dst=filename)
                WranglerLogger.debug("Copying {:20} to {}".format(filename+suffix, filename))

    def applyProject(self, parentdir, networkdir, gitdir, projectsubdir=None, **kwargs):
        """
        Applies a roadway project by calling ``runtpp`` on the ``apply.s`` script.
        By convention, the input to ``apply.s`` is ``FREEFLOW.BLD`` and the output is 
        ``FREEFLOW.BLDOUT`` which is copied to ``FREEFLOW.BLD`` at the end of ``apply.s``

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        # special case: base network
        if self.applyingBasenetwork:
            self.applyBasenetwork(parentdir, networkdir, gitdir, tierNetworkName=None)
            self.logProject(gitdir=gitdir,
                            projectname=(networkdir + "\\" + projectsubdir if projectsubdir else networkdir),
                            projectdesc="Base network")            
            return
        
        if projectsubdir:
            applyDir      = os.path.join(parentdir, networkdir, projectsubdir)
            applyScript   = "apply.s"
            descfilename  = os.path.join(parentdir, networkdir, projectsubdir, "desc.txt")
            turnsfilename = os.path.join(parentdir, networkdir, projectsubdir, "turns.pen")
            tollsfilename = os.path.join(parentdir, networkdir, projectsubdir, "tolls.csv")
        else:
            applyDir      = os.path.join(parentdir, networkdir)
            applyScript   = "apply.s"
            descfilename  = os.path.join(parentdir, networkdir, "desc.txt")
            turnsfilename = os.path.join(parentdir, networkdir, "turns.pen")
            tollsfilename = os.path.join(parentdir, networkdir, "tolls.csv")

        # read the description
        desc = None
        try:
            desc = open(descfilename,'r').read()
        except:
            pass
        
        # move the FREEFLOW.BLD into place
        shutil.move("FREEFLOW.BLD", os.path.join(applyDir,"FREEFLOW.BLD"))

        # WranglerLogger.debug("HighwayNetwork.applyProject() received kwargs:{}".format(kwargs))

        # retry in case of a license error
        NUM_RETRIES = 5
        for attempt in range(1,NUM_RETRIES+1):

            # dispatch it, cube license
            hostname = gethostname().lower()
            if False: #hostname not in HighwayNetwork.getCubeHostnames():
                print("Dispatching cube script to taraval from %s".format(hostname))
                f = open(os.path.join(applyDir,'runtpp_dispatch.tmp'), 'w')
                f.write("runtpp " + applyScript + "\n")
                f.close()
                (cuberet, cubeStdout, cubeStderr) = self._runAndLog("Y:/champ/util/bin/dispatch.bat runtpp_dispatch.tmp taraval", run_dir=applyDir, logStdoutAndStderr=True, env=kwargs) 
            else:
                (cuberet, cubeStdout, cubeStderr) = self._runAndLog(cmd="runtpp "+applyScript, run_dir=applyDir, env=kwargs)
            

            nodemerge = re.compile("NODEMERGE: \d+")
            linkmerge = re.compile("LINKMERGE: \d+-\d+")
            cube_success = re.compile("\s*(VOYAGER)\s+(ReturnCode)\s*=\s*([01])\s+")
            license_error = False
            for line in cubeStdout:
                line = line.rstrip()
                if re.match(nodemerge,line): continue
                if re.match(linkmerge,line): continue
                if line=="RUNTPP: Licensing error": license_error = True
                WranglerLogger.debug(line)
            
            # retry on license error
            if license_error:
                WranglerLogger.warn("Received license error")
                if attempt == NUM_RETRIES:
                    WranglerLogger.fatal("Out of retry attempts")
                    raise NetworkException("HighwayNetwork applyProject failed from Licensing error")

                # retry
                WranglerLogger.debug("Retrying {} ...".format(attempt))
                time.sleep(1)
                continue

            if cuberet != 0 and cuberet != 1 and len(cubeStdout) > 1:

                # cuberet may be wrong -- check last stdout
                WranglerLogger.debug("checking cubeStdout[-1]: {}".format(cubeStdout[-1]))
                # WranglerLogger.debug("match: {}".format(re.match(cube_success,cubeStdout[-1])))
                if re.match(cube_success,cubeStdout[-1]):
                    WranglerLogger.debug("Overriding cuberet {} with 0 due to last cubeStdout line".format(cuberet))
                    cuberet = 0

            if cuberet != 0 and cuberet != 1:
                WranglerLogger.debug("cubeStdout: {}".format(cubeStdout))
                WranglerLogger.fatal("FAIL! Project: {}  cuberet={}".format(applyScript, cuberet))
                raise NetworkException("HighwayNetwork applyProject failed; see log file")

            else:
                # success
                break

        # move it back
        shutil.move(os.path.join(applyDir,"FREEFLOW.BLD"), "FREEFLOW.BLD")

        # append new turn penalty file to mine
        if os.path.exists(turnsfilename):
            for filename in ["turnsam.pen", "turnspm.pen", "turnsop.pen"]:
                newturnpens = open(turnsfilename, 'r').read()
                turnfile = open(filename, 'a')
                turnfile.write(newturnpens)
                turnfile.close()
                WranglerLogger.debug("Appending turn penalties from "+turnsfilename)

        # merge tolls.csv
        if os.path.exists(tollsfilename):
            self.mergeTolls("tolls.csv", tollsfilename)

        WranglerLogger.debug("")
        WranglerLogger.debug("")

        year    = None
        county  = None
        if (networkdir==self.hwyspecsdir and
            self.hwyspecs and
            projectsubdir in self.hwyspecs.projectdict):
            year    = self.hwyspecs.projectdict[projectsubdir]["MOD YEAR"]
            county  = self.hwyspecs.projectdict[projectsubdir]["County"]
            desc    = (self.hwyspecs.projectdict[projectsubdir]["Facility"] + ", " +
                       self.hwyspecs.projectdict[projectsubdir]["Action"] + ", " +
                       self.hwyspecs.projectdict[projectsubdir]["Span"])

        return self.logProject(gitdir=gitdir,
                               projectname=(networkdir + "\\" + projectsubdir if projectsubdir else networkdir),
                               year=year, projectdesc=desc, county=county)

    def mergeTolls(self, tollsfile, newtollsfile):
        """
        Merge the given tolls file with the existing.
        """
        WranglerLogger.debug("mergeTolls({},{}) called".format(tollsfile, newtollsfile))     

        # read the original file -- fac_index is the key
        tolls_config = collections.OrderedDict()
        tolls        = open(tollsfile, 'r')
        tolls_reader = csv.reader(tolls, skipinitialspace=True)
        fieldnames   = next(tolls_reader)
        # not using csv.DictReader because in python2, it doesn't read an ordered dict :(
        for row in tolls_reader:
            row_dict = collections.OrderedDict(zip(fieldnames, row))
            WranglerLogger.debug("row_dict: {}".format(row_dict))
            tolls_config[row_dict["fac_index"]] = row_dict
        tolls.close()

        # read the new file -- replace if fac_index matches
        newtolls       = open(newtollsfile, 'r')
        new_reader     = csv.reader(newtolls, skipinitialspace=True)
        new_fieldnames = next(new_reader)
        # they need to match, or fieldnames can be longer
        if fieldnames == new_fieldnames:
            # excellent
            pass
        elif len(new_fieldnames) < len(fieldnames) and fieldnames[:len(new_fieldnames)] == new_fieldnames:
            # ok -- some columns at end can be blank
            pass
        else:
            raise NetworkException("Toll file {} has different fieldnames ({}) than expected ({})".format(newtollsfile, new_fieldnames, fieldnames))

        for row in new_reader:
            row_dict = collections.OrderedDict(zip(fieldnames, row))
            tolls_config[row_dict["fac_index"]] = row_dict
        newtolls.close()

        # write it out
        tolls = open(tollsfile, mode='w', newline='')  # newline arg passed because of https://docs.python.org/3/library/csv.html#id3
        tolls_writer = csv.writer(tolls)
        tolls_writer.writerow(fieldnames)
        for fac_index, row in tolls_config.items():
            tolls_writer.writerow(row.values())
        tolls.close()

    def validateTurnPens(self, CubeNetFile, turnPenReportFile=None, suggestCorrectLink=True):
        import Cube
        turnpens_files = ['turnsam.pen','turnsop.pen','turnspm.pen']
        pen_regex = r'^\s*(?P<frnode>\d+)\s+(?P<thnode>\d+)\s+(?P<tonode>\d+)\s+\d+\s+(?P<pen>-[\d+])'
        if turnPenReportFile:
            outfile = open(turnPenReportFile,'w')
            outfile.write('file,old_from,old_through,old_to,on_street,at_street,new_from,new_through,new_to,note\n')
            
        (nodes_dict, links_dict) = Cube.import_cube_nodes_links_from_csvs(CubeNetFile,
                                                                          extra_link_vars=['LANE_AM', 'LANE_OP','LANE_PM',
                                                                                           'BUSLANE_AM', 'BUSLANE_OP', 'BUSLANE_PM'],
                                                                          extra_node_vars=[],
                                                                          links_csv=os.path.join(os.getcwd(),"cubenet_validate_links.csv"),
                                                                          nodes_csv=os.path.join(os.getcwd(),"cubenet_validate_nodes.csv"),
                                                                          exportIfExists=True)
        found_matches = {}
        
        for file_name in turnpens_files:
            f = open(file_name,'r')
            for line in f:
                text = line.split(';')[0]
                m = re.match(pen_regex, text)
                if m:
                    new_fr = None
                    new_th = None
                    new_to = None
                    from_street = 'missing'
                    to_street = 'missing'
                    fr_node = int(m.groupdict()['frnode'])
                    th_node = int(m.groupdict()['thnode'])
                    to_node = int(m.groupdict()['tonode'])
                    pen     = int(m.groupdict()['pen'])
                    if not (fr_node,th_node) in links_dict:
                        WranglerLogger.debug("HighwayNetwork.validateTurnPens: (%d, %d) not in the roadway network for %s (%d, %d, %d)" % (fr_node,th_node,file_name,fr_node,th_node,to_node))
                        
                        if suggestCorrectLink:
                            new_fr = -1
                            new_th = th_node
                            match_links_fr = []
                            match_links_th = []
                            # if we already found a match for this, don't keep looking.
                            if (fr_node,th_node) in found_matches.keys():
                                match = found_matches[(fr_node,th_node)]
                                new_fr = match[0][1]
                            else:
                                #catch the links matching fr_node on the from end
                                for (a,b) in links_dict.keys():
                                    if a == fr_node:
                                        match_links_fr.append((a,b))
                                    # and links matching th_node on the to end
                                    if b == th_node:
                                        match_links_th.append((a,b))
                                # now take matched links and look for match_links_fr node b to match match_links_th node a
                                for (a1,b1) in match_links_fr:
                                    for (a2,b2) in match_links_th:
                                        if b1 == a2:
                                            #WranglerLogger.info("For link1 (%d, %d) and link2 (%d, %d): %d == %d" % (a1,b1,a2,b2,b1,a2))
                                            found_matches[(fr_node,th_node)] = [(a1,b1),(a2,b2)]
                                            new_fr = a2
                                            # index 1 is streetname
                                            from_street = links_dict[(a2,b2)][1]
                                            break
                    else:
                        new_fr = fr_node
                        from_street = links_dict[(fr_node,th_node)][1]
        
                            
                    if not (th_node,to_node) in links_dict:
                        WranglerLogger.debug("HighwayNetwork.validateTurnPens: (%d, %d) not in the roadway network for %s (%d, %d, %d)" % (th_node,to_node,file_name,fr_node,th_node,to_node))
                        #if turnPenReportFile: outfile.write("%s,%d,%d,outbound link missing from, %d, %d, %d\n" %(file_name,th_node,to_node,fr_node,th_node,to_node))
                        if suggestCorrectLink:
                            new_th = th_node
                            new_to = -1
                            match_links_th = []
                            match_links_to = []
                            # if we already found a match for this, don't keep looking.
                            if (th_node,to_node) in found_matches.keys():
                                match = found_matches[(th_node,to_node)]
                                new_to = match[0][1]
                            else:
                                #catch the links matching fr_node on the from end
                                for (a,b) in links_dict.keys():
                                    if a == th_node:
                                        match_links_th.append((a,b))
                                    # and links matching th_node on the to end
                                    if b == to_node:
                                        match_links_to.append((a,b))
                                # now take matched links and look for match_links_fr node b to match match_links_th node a
                                for (a1,b1) in match_links_th:
                                    for (a2,b2) in match_links_to:
                                        if b1 == a2:
                                            #WranglerLogger.info("For link1 (%d, %d) and link2 (%d, %d): %d == %d" % (a1,b1,a2,b2,b1,a2))
                                            found_matches[(th_node,to_node)] = [(a1,b1),(a2,b2)]
                                            new_to = a2
                                            to_street = links_dict[(a2,b2)][1]
                                            break
                    else:
                        new_to = to_node
                        to_street = links_dict[(th_node,to_node)][1]
                    
                    if new_th != None:
                        #outfile.write('file,old_from,old_through,old_to,on_street,at_street,new_from,new_through,new_to,note\n')
                        print(file_name,fr_node,th_node,to_node,from_street,to_street,new_fr,new_th,new_to)
                        outfile.write('%s,%d,%d,%d,%s,%s,%d,%d,%d,note\n' % (file_name,fr_node,th_node,to_node,from_street,to_street,new_fr if new_fr else -1,new_th,new_to if new_to else -1))
                
    def write(self, path='.', name='FREEFLOW.NET', writeEmptyFiles=True, suppressQuery=False, suppressValidation=False):
        if not os.path.exists(path):
            WranglerLogger.debug("\nPath [%s] doesn't exist; creating." % path)
            os.mkdir(path)

        else:
            netfile = os.path.join(path,"FREEFLOW.net")
            if os.path.exists(netfile) and not suppressQuery:
                print("File [{}] exists already.  Overwrite contents? (y/n/s) ".format(netfile))
                response = raw_input("")
                WranglerLogger.debug("response = [%s]" % response)
                if response == "s" or response == "S":
                    WranglerLogger.debug("Skipping!")
                    return

                if response != "Y" and response != "y":
                    exit(0)

        shutil.copyfile("FREEFLOW.BLD",os.path.join(path,name))
        WranglerLogger.info("Writing into %s\\%s" % (path, name))
        WranglerLogger.info("")

        for filename in ["turnsam.pen",         "turnspm.pen",          "turnsop.pen", "tolls.csv"]:
            shutil.copyfile(filename, os.path.join(path, filename))
            
        if not suppressValidation: self.validateTurnPens(netfile,'turnPenValidations.csv')

    def writeShapefile(self, path: str, links_file='roadway_links.shp', nodes_file='roadway_nodes.shp'):
        """ Writes the roadway network as shape files for links and nodes.

        Args:
            path (str): The directory in which to write the shapefile.
            links_file (str, optional): Name of the roadway links shapefile. Defaults to 'roadway_links.shp'.
            nodes_file (str, optional): Name of the roadway nodes shapefile. Defaults to 'roadway_nodes.shp'.

        Returns:
            nodes_dict: nodenum -> [X,Y]

        NOTE: this imports pandas, geopandas and shapely

        """
        # Export as csvs
        import tempfile
        tempdir = tempfile.mkdtemp()
        WranglerLogger.debug("Writing roadway network to tempdir {}".format(tempdir))

        Network.allNetworks['hwy'].write(path=tempdir, name="freeflow.net", writeEmptyFiles=False, suppressQuery=True, suppressValidation=True)
        tempnet = os.path.join(tempdir, "freeflow.net")

        # read the roadway network csvs
        import Cube
        link_vars = ['LANES','USE','FT','TOLLCLASS','ROUTENUM','ROUTEDIR','PROJ']
        (nodes_dict, links_dict) = Cube.import_cube_nodes_links_from_csvs(tempnet, extra_link_vars=link_vars,
                                        links_csv=os.path.join(tempdir,"cubenet_links.csv"),
                                        nodes_csv=os.path.join(tempdir,"cubenet_nodes.csv"),
                                        exportIfExists=True)
        WranglerLogger.debug("Have {} nodes and {} links".format(len(nodes_dict), len(links_dict)))

        ## create node GeoDataFrame and write shapefile
        import pandas
        import geopandas
        import shapely
        node_data = []
        for node_num in sorted(nodes_dict.keys()):
            node_data.append([node_num, nodes_dict[node_num][0], nodes_dict[node_num][1]])
        nodes_df = pandas.DataFrame(data=node_data, columns=["N","X","Y"])
        nodes_gdf = geopandas.GeoDataFrame(nodes_df, geometry=geopandas.points_from_xy(nodes_df.X, nodes_df.Y),
                                           crs="EPSG:26910") # https://epsg.io/26910
        nodes_gdf.to_file(filename=os.path.join(path, nodes_file))
        WranglerLogger.debug("Wrote {} nodes to {}".format(len(nodes_gdf), os.path.join(path, nodes_file)))

        ## create link GeoDataFrame and write shapefile
        link_data = []
        link_geometry = []
        for link_a_b in links_dict.keys():
            link_data.append([link_a_b[0], link_a_b[1]] + links_dict[link_a_b])
            link_geometry.append(shapely.LineString([
                shapely.Point(nodes_dict[link_a_b[0]][0],
                              nodes_dict[link_a_b[0]][1]),
                shapely.Point(nodes_dict[link_a_b[1]][0],
                              nodes_dict[link_a_b[1]][1])
            ]))
        links_df = pandas.DataFrame(data=link_data, columns=["A","B","DISTANCE"] + link_vars)
        links_df = links_df.astype({'LANES':'int8', 'USE':'int8', 'FT':'int8', 'TOLLCLASS':int, 'ROUTENUM':'int8'})
        links_gdf = geopandas.GeoDataFrame(links_df, geometry=link_geometry, crs="EPSG:26910")
        links_gdf.to_file(filename=os.path.join(path, links_file))
        WranglerLogger.debug("Wrote {} links to {}".format(len(links_gdf), os.path.join(path, links_file)))

        return nodes_dict
