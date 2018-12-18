import argparse,collections,datetime,os,pandas,sys,time
import Wrangler

# Based on NetworkWrangler\scripts\build_network.py
#

USAGE = """

  Builds a network using the specifications in network_specification.py, which should
  define the variables listed below (in this script)

  The [-c configword] is if you want an optional word for your network_specification.py
  (e.g. to have multiple scenarios in one file).  Access it via CONFIG_WORD.

"""

###############################################################################
#                                                                             #
#              Define the following in an input configuration file            #
#                                                                             #
###############################################################################
# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT = None

# MANDATORY. Set this to be the Scenario Name
# e.g. "Base", "Baseline"
SCENARIO = None

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = None

# OPTIONAL. If you are building on top of a previously built network, this
# should be set to the location of those networks.  This should be a directory
# which has "hwy" and "trn" subdirectories.
PIVOT_DIR = None

# OPTIONAL. If PIVOT_DIR is specified, MANDATORY.  Specifies year for PIVOT_DIR.
PIVOT_YEAR = 2015

# MANDATORY. Set this to the directory in which to write your outputs. 
# "hwy" and "trn" subdirectories will be created here.
OUT_DIR = None

# MANDATORY.  Should be a dictionary with keys in NET_MODES
# to a list of projects.  A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}
NETWORK_PROJECTS = None

# OPTIONAL. The default route network project directory is Y:\networks.  If
# projects are stored in another directory, then use this variable to specify it.
# For example: Y:\networks\projects
NETWORK_BASE_DIR       = None
NETWORK_PROJECT_SUBDIR = None
NETWORK_SEED_SUBDIR    = None
NETWORK_PLAN_SUBDIR    = None

# OPTIONAL. A list of project names which have been previously applied in the
# PIVOT_DIR network that projects in this project might rely on.  For example
# if DoyleDrive exists, then Muni_TEP gets applied differently so transit lines
# run on the new Doyle Drive alignment
APPLIED_PROJECTS = None

# OPTIONAL.  A list of project names.  For test mode, these projects won't use
# the TAG.  This is meant for developing a network project.
TEST_PROJECTS = None

TRN_MODES = ['trn']
NET_MODES = ['hwy'] + TRN_MODES

###############################################################################

###############################################################################
#                                                                             #
#              Helper functions                                               #
#                                                                             #
###############################################################################
def getProjectNameAndDir(project):
    if type(project) == type({'this is':'a dict'}):
        name = project['name']
    else:
        name = project
    (path,name) = os.path.split(name)
    return (path,name)

def getNetworkListIndex(project, networks):
    for proj in networks:
        (path,name) = getProjectNameAndDir(proj)
        if project == name or project == os.path.join(path,name):
            return networks.index(proj)
    return None

def getProjectMatchLevel(left, right):
    (left_path,left_name)   = getProjectNameAndDir(left)
    (right_path,right_name) = getProjectNameAndDir(right)
    match = 0
    if os.path.join(left_path,left_name) == os.path.join(right_path,right_name):
        match = 2
    elif left_name == right_name:
        match = 1
    #Wrangler.WranglerLogger.debug("Match level %d for %s and %s" % (match, os.path.join(left_path,left_name), os.path.join(right_path,right_name)))
    return match

def getProjectYear(PROJECTS, my_proj, netmode):
    """
    PROJECTS is an OrderedDict, year -> netmode -> [ project list ]
    Returns first year in which my_proj shows up in the netmode's project list, plus number in list
    e.g. 2020.02 for second project in 2020
    """
    for year in PROJECTS.keys():
        if my_proj in PROJECTS[year][netmode]:
            return year + (PROJECTS[year][netmode].index(my_proj)+1)*0.01
    return -1

def checkRequirements(REQUIREMENTS, PROJECTS, req_type='prereq'):
    if req_type not in ('prereq','coreq','conflict'):
        return (None, None)

    # Wrangler.WranglerLogger.debug("checkRequirements called with requirements=[{}] projects=[{}] req_typ={}".format(REQUIREMENTS, PROJECTS, req_type))

    is_ok = True

    # REQUIREMENTS: netmode -> project -> netmode -> [list of projects]
    for netmode in REQUIREMENTS.keys():
        for project in REQUIREMENTS[netmode].keys():
            project_year = getProjectYear(PROJECTS, project, netmode)
            if project_year == -1:
                Wrangler.WranglerLogger.warn('Cannot find the %s project %s to check its requirements'.format(netmode, project))
                continue  # raise?

            Wrangler.WranglerLogger.info('Checking {} project {} ({}) for {}'.format(netmode, project, project_year, req_type))

            for req_netmode in REQUIREMENTS[netmode][project].keys():

                req_proj_list  = REQUIREMENTS[netmode][project][req_netmode]
                req_proj_years = {}
                for req_proj in req_proj_list:
                    req_project_year = getProjectYear(PROJECTS, req_proj, req_netmode)

                    # prereq
                    if req_type=="prereq":
                        if req_project_year < 0:            is_ok = False  # required project must be found
                        if req_project_year > project_year: is_ok = False  # and implemented before or at the same time as the project

                    # save into proj_years
                    req_proj_years[req_proj] = req_project_year

                # sub out the list info with the project year info
                REQUIREMENTS[netmode][project][req_netmode] = req_proj_years

    return (REQUIREMENTS, is_ok)

def writeRequirements(REQUIREMENTS, PROJECTS, req_type='prereq'):
    if req_type=='prereq':
        print_req = 'Pre-requisite'
    elif req_type=='coreq':
        print_req = 'Co-requisite'
    elif req_type=='conflict':
        print_req = 'Conflict'
    else:
        return None

    Wrangler.WranglerLogger.info("Requirement verification - {}".format(print_req))
    Wrangler.WranglerLogger.info("    Year    {:50}     {:50} Year".format("Project",print_req+" " + "Project"))
    # REQUIREMENTS: netmode -> project -> netmode -> req_proj -> req_proj_year
    for netmode in REQUIREMENTS.keys():
        for project in REQUIREMENTS[netmode].keys():
            project_year = getProjectYear(PROJECTS, project, netmode)
            for req_netmode in REQUIREMENTS[netmode][project].keys():
                for req_project in REQUIREMENTS[netmode][project][req_netmode].keys():
                    Wrangler.WranglerLogger.info("{} {} {:50} {} {:50} {}".format(netmode, project_year, project,
                                                 req_netmode, req_project, REQUIREMENTS[netmode][project][req_netmode][req_project]))

def getProjectAttributes(project):
    # Start with TAG if not build mode, no kwargs
    project_type    = 'project'
    tag             = None
    kwargs          = {}

    # Use project name, tags, kwargs from dictionary
    if type(project)==type({'this is':'a dictionary'}):
        project_name = project['name']
        if 'tag' in project:    tag = project['tag']
        if 'type' in project:   project_type = project['type']
        if 'kwargs' in project: kwargs = project['kwargs']

    # Use Project name directly
    elif type(project)==type("string"):
        project_name = project

    # Other structures not recognized
    else:
         Wrangler.WranglerLogger.fatal("Don't understand project %s" % str(project))

    return (project_name, project_type, tag, kwargs)

def preCheckRequirementsForAllProjects(networks):
    PRE_REQS  = {'hwy':{},'trn':{}}
    CO_REQS   = {'hwy':{},'trn':{}}
    CONFLICTS = {'hwy':{},'trn':{}}

    # Network Loop #1: check out all the projects, check if they're stale, check if they're the head repository.  Build completed
    # project list so we can check pre-reqs, etc, in loop #2.
    for netmode in NET_MODES:
        # Build the networks!
        Wrangler.WranglerLogger.info("Checking out %s networks" % netmode)
        clonedcount = 0
        for model_year in NETWORK_PROJECTS.keys():
            for project in NETWORK_PROJECTS[model_year][netmode]:
                (project_name, projType, tag, kwargs) = getProjectAttributes(project)
                if tag == None: tag = TAG

                # test mode - don't use TAG for TEST_PROJECTS
                if BUILD_MODE=="test" and type(TEST_PROJECTS)==type(['List']):
                    if project_name in TEST_PROJECTS:
                        Wrangler.WranglerLogger.debug("Skipping tag [%s] because test mode and [%s] is in TEST_PROJECTS" % 
                                                      (TAG, project_name))
                        tag = None

                Wrangler.WranglerLogger.debug("Project name = %s" % project_name)

                cloned_SHA1 = None
                # if project = "dir1/dir2" assume dir1 is git, dir2 is the projectsubdir
                (head,tail) = os.path.split(project_name)
                if head:
                    cloned_SHA1 = networks[netmode].cloneProject(networkdir=head, projectsubdir=tail, tag=tag,
                                                                 projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                    (prereqs, coreqs, conflicts) = networks[netmode].getReqs(networkdir=head, projectsubdir=tail, tag=tag,
                                                                             projtype=projType, tempdir=TEMP_SUBDIR)
                else:
                    cloned_SHA1 = networks[netmode].cloneProject(networkdir=project_name, tag=tag,
                                                                 projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                    (prereqs, coreqs, conflicts) = networks[netmode].getReqs(networkdir=project_name, projectsubdir=tail, tag=tag,
                                                                             projtype=projType, tempdir=TEMP_SUBDIR)

                # find out if the applied project is behind HEAD
                # get the HEAD SHA1
                cmd = r"git show-ref --head master"
                if projType=='project':
                    join_subdir = Wrangler.Network.NETWORK_PROJECT_SUBDIR
                if projType=='seed':
                    join_subdir = Wrangler.Network.NETWORK_SEED_SUBDIR

                cmd_dir = os.path.join(Wrangler.Network.NETWORK_BASE_DIR, join_subdir, project_name)
                (retcode, retStdout, retStderr) = networks[netmode]._runAndLog(cmd, run_dir = cmd_dir)
                # Wrangler.WranglerLogger.debug("results of [%s]: %s %s %s" % (cmd, str(retcode), str(retStdout), str(retStderr)))
                if retcode != 0: # this shouldn't happen -- wouldn't cloneAndApply have failed?
                    Wrangler.WranglerLogger.fatal("Couldn't run cmd [%s] in [%s]: stdout=[%s] stderr=[%s]" % \
                                                  (cmd, cmd_dir, str(retStdout), str(retStderr)))
                    sys.exit(2)
                head_SHA1 = retStdout[0].split()[0]
    
                # if they're different, log more information and get approval (if not in test mode)
                if cloned_SHA1 != head_SHA1:
                    Wrangler.WranglerLogger.warn("Using non-head version of project of %s" % project_name)
                    Wrangler.WranglerLogger.warn("  Applying version [%s], Head is [%s]" % (cloned_SHA1, head_SHA1))
    
                    cmd = "git log %s..%s" % (cloned_SHA1, head_SHA1)
                    (retcode, retStdout, retStderr) = networks[netmode]._runAndLog(cmd, run_dir = cmd_dir)
                    Wrangler.WranglerLogger.warn("  The following commits are not included:") 
                    for line in retStdout:
                        Wrangler.WranglerLogger.warn("    %s" % line)
    
                    # test mode => warn is sufficient
                    # non-test mode => get explicit approval
                    if BUILD_MODE !="test":
                        Wrangler.WranglerLogger.warn("  Is this ok? (y/n) ")
                        response = raw_input("")
                        Wrangler.WranglerLogger.debug("  response = [%s]" % response)
                        if response.strip().lower()[0] != "y":
                            sys.exit(2)
    
                # find out if the project is stale
                else:
                    cmd = 'git show -s --format="%%ct" %s' % cloned_SHA1
                    (retcode, retStdout, retStderr) = networks[netmode]._runAndLog(cmd, run_dir = cmd_dir)
                    applied_commit_date = datetime.datetime.fromtimestamp(int(retStdout[0]))
                    applied_commit_age = datetime.datetime.now() - applied_commit_date
    
                    # if older than one year, holler
                    STALE_YEARS = 2
                    if applied_commit_age > datetime.timedelta(days=365*STALE_YEARS):
                        Wrangler.WranglerLogger.warn("  This project was last updated %.1f years ago (over %d), on %s" % \
                                                     (applied_commit_age.days/365.0,
                                                      STALE_YEARS, applied_commit_date.strftime("%x")))
                        if BUILD_MODE !="test":
                            Wrangler.WranglerLogger.warn("  Is this ok? (y/n) ")
                            response = raw_input("")
                            Wrangler.WranglerLogger.debug("  response = [%s]" % response)
                            if response.strip().lower() not in ["y", "yes"]:
                                sys.exit(2)
    
                clonedcount += 1
            
                # format: netmode -> project -> { netmode: [requirements] }
                if len(prereqs  ) > 0: PRE_REQS[ netmode][project_name] = prereqs
                if len(coreqs   ) > 0: CO_REQS[  netmode][project_name] = coreqs
                if len(conflicts) > 0: CONFLICTS[netmode][project_name] = conflicts

    # Check requirements
    prFile = 'prereqs.csv'
    crFile = 'coreqs.csv'
    cfFile = 'conflicts.csv'

    # Check prereqs
    (PRE_REQS, allPrereqsFound) = checkRequirements(PRE_REQS, NETWORK_PROJECTS, req_type='prereq')
    writeRequirements(PRE_REQS, NETWORK_PROJECTS, req_type='prereq')
    if allPrereqsFound:
        Wrangler.WranglerLogger.debug('All PRE-REQUISITES were found. Are the PRE-REQUISITES matches correct? (y/n)')
    else:
        Wrangler.WranglerLogger.debug('!!!WARNING!!! Some PRE-REQUISITES were not found.  Continue anyway? (y/n)')
    response = raw_input("")
    Wrangler.WranglerLogger.debug("  response = [%s]" % response)
    if response.strip().lower() not in ["y", "yes"]:
        sys.exit(2)

    # Check coreqs
    (CO_REQS, allCoreqsFound) = checkRequirements(CO_REQS, NETWORK_PROJECTS, req_type='coreq')
    if len(CO_REQS['trn'])>0 or len(CO_REQS['hwy'])>0:
        writeRequirements(CO_REQS, NETWORK_PROJECTS, req_type='coreq')
        if allCoreqsFound:
            Wrangler.WranglerLogger.debug('All CO-REQUISITES were found. Are the CO-REQUISITE matches correct? (y/n)')
        else:
            Wrangler.WranglerLogger.debug('!!!WARNING!!! Some CO-REQUISITES were not found.  Continue anyway? (y/n)')
        response = raw_input("")
        Wrangler.WranglerLogger.debug("  response = [%s]" % response)
        if response.strip().lower() not in ["y", "yes"]:
            sys.exit(2)

    # Check conflicts
    (CONFLICTS, anyConflictFound) = checkRequirements(CONFLICTS, NETWORK_PROJECTS, req_type='conflict')
    if len(CONFLICTS['trn'])>0 or len(CONFLICTS['hwy'])>0:
        writeRequirements(CONFLICTS, NETWORK_PROJECTS, 'conflict')
        if anyConflictFound:
            Wrangler.WranglerLogger.debug('!!!WARNING!!! Conflicting projects were found.  Continue anyway? (y/n)')
        else:
            Wrangler.WranglerLogger.debug('No conflicting projects were found. Enter \'y\' to continue.')
        response = raw_input("")
        Wrangler.WranglerLogger.debug("  response = [%s]" % response)
        if response.strip().lower() not in ["y", "yes"]:
            sys.exit(2)

    # Wrangler.WranglerLogger.debug("NETWORK_PROJECTS=%s NET_MODES=%s" % (str(NETWORK_PROJECTS), str(NET_MODES)))

###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--configword", help="optional word for network specification script")
    parser.add_argument("--model_type", choices=[Wrangler.Network.MODEL_TYPE_TM1, Wrangler.Network.MODEL_TYPE_TM2],
                        default=Wrangler.Network.MODEL_TYPE_TM1)
    parser.add_argument("net_spec", metavar="network_specification.py", help="Script which defines required variables indicating how to build the network")
    args = parser.parse_args()

    NOW         = time.strftime("%Y%b%d.%H%M%S")
    BUILD_MODE  = None # regular
    if args.model_type == Wrangler.Network.MODEL_TYPE_TM1:
        PIVOT_DIR        = r"M:\\Application\\Model One\\Networks\\TM1_2015_Base_Network"
        TRANSIT_CAPACITY_DIR = os.path.join(PIVOT_DIR, "trn")
        NETWORK_BASE_DIR = r"M:\\Application\\Model One\\NetworkProjects"
        TRN_SUBDIR       = "trn"
        TRN_NET_NAME     = "Transit_Lines"
        HWY_SUBDIR       = "hwy"
        HWY_NET_NAME     = "freeflow.net"
    elif args.model_type == Wrangler.Network.MODEL_TYPE_TM2:
        PIVOT_DIR        = os.path.join(os.environ["USERPROFILE"], "Box","Modeling and Surveys","Development","Travel Model Two Development","Model Inputs","2015_revised_mazs")
        TRANSIT_CAPACITY_DIR = None
        NETWORK_BASE_DIR = r"M:\\Application\\Model Two\\NetworkProjects"
        TRN_SUBDIR       = "trn"
        TRN_NET_NAME     = "transitLines"
        HWY_SUBDIR       = "hwy"
        HWY_NET_NAME     = "mtc_final_network_base.net"

    # Read the configuration
    NETWORK_CONFIG = args.net_spec
    exec(open(NETWORK_CONFIG).read())

    # Verify mandatory fields are set
    if PROJECT==None:
        print("PROJECT not set in %s" % NETWORK_CONFIG)
        sys.exit(2)
    if SCENARIO==None:
        print("SCENARIO not set in %s" % NETWORK_CONFIG)
        sys.exit(2)
    if TAG==None:
        print("TAG not set in %s" % NETWORK_CONFIG)
        sys.exit(2)
    if OUT_DIR==None:
        print("OUT_DIR not set in %s" % NETWORK_CONFIG)
        sys.exit(2)
    if NETWORK_PROJECTS==None:
        print("NETWORK_PROJECTS not set in %s" % NETWORK_CONFIG)
        sys.exit(2)

    LOG_FILENAME = "build%snetwork_%s_%s_%s.info.LOG" % ("TEST" if BUILD_MODE=="test" else "", PROJECT, SCENARIO, NOW)
    Wrangler.setupLogging(LOG_FILENAME, LOG_FILENAME.replace("info", "debug"))
    if TRANSIT_CAPACITY_DIR:
        Wrangler.TransitNetwork.capacity = Wrangler.TransitCapacity(directory=TRANSIT_CAPACITY_DIR)

    # Create a scratch directory to check out project repos into
    SCRATCH_SUBDIR = "scratch"
    TEMP_SUBDIR    = "Wrangler_tmp_" + NOW    
    if not os.path.exists(SCRATCH_SUBDIR): os.mkdir(SCRATCH_SUBDIR)
    os.chdir(SCRATCH_SUBDIR)

    networks = {
        'hwy' :Wrangler.HighwayNetwork(modelType=args.model_type, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR,"hwy") if PIVOT_DIR else "Roads2010",
                                       networkBaseDir=NETWORK_BASE_DIR,
                                       networkProjectSubdir=NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR else False,
                                       tag=TAG,
                                       tempdir=TEMP_SUBDIR,
                                       networkName="hwy",
                                       tierNetworkName=HWY_NET_NAME),
        'trn':Wrangler.TransitNetwork( modelType=args.model_type, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR,"trn") if PIVOT_DIR else None,
                                       networkBaseDir=NETWORK_BASE_DIR,
                                       networkProjectSubdir=NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR else False,
                                       networkName=TRN_NET_NAME)
    }

    # For projects applied in a pivot network (because they won't show up in the current project list)
    if APPLIED_PROJECTS != None:
        for proj in APPLIED_PROJECTS:
            networks['hwy'].appliedProjects[proj]=TAG


    # Wrangler.WranglerLogger.debug("NETWORK_PROJECTS=%s NET_MODES=%s" % (str(NETWORK_PROJECTS), str(NET_MODES)))
    preCheckRequirementsForAllProjects(networks)

    # Network Loop #2: Now that everything has been checked, build the networks.
    for YEAR in NETWORK_PROJECTS.keys():
        projects_for_year = NETWORK_PROJECTS[YEAR]

        appliedcount = 0
        for netmode in NET_MODES:
            Wrangler.WranglerLogger.info("Building {} {} networks".format(YEAR, netmode))
            for project in projects_for_year[netmode]:
                (project_name, projType, tag, kwargs) = getProjectAttributes(project)
                if tag == None: tag = TAG

                Wrangler.WranglerLogger.info("Applying project [%s] of type [%s] with tag [%s]" % (project_name, projType, tag))
                if projType=='plan':
                    continue

                applied_SHA1 = None
                cloned_SHA1 = networks[netmode].cloneProject(networkdir=project_name, tag=tag,
                                                             projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                (parentdir, networkdir, gitdir, projectsubdir) = networks[netmode].getClonedProjectArgs(project_name, None, projType, TEMP_SUBDIR)

                applied_SHA1 = networks[netmode].applyProject(parentdir, networkdir, gitdir, projectsubdir)
                appliedcount += 1

        if appliedcount == 0:
            Wrangler.WranglerLogger.info("No applied projects for this year -- skipping output")
            continue

        # Initialize output subdirectories up a level (not in scratch)
        hwypath=os.path.join("..", OUT_DIR.format(YEAR),HWY_SUBDIR)
        if not os.path.exists(hwypath): os.makedirs(hwypath)
        trnpath = os.path.join("..", OUT_DIR.format(YEAR),TRN_SUBDIR)
        if not os.path.exists(trnpath): os.makedirs(trnpath)

        networks['hwy'].write(path=hwypath,name=HWY_NET_NAME,suppressQuery=True,
                              suppressValidation=True) # MTC TM1 doesn't have turn penalties

        os.environ["CHAMP_node_names"] = os.path.join(PIVOT_DIR,"Node Description.xls")
        hwy_abs_path = os.path.abspath( os.path.join(hwypath, HWY_NET_NAME) )
        networks['trn'].write(path=trnpath,
                              name="transitLines",
                              writeEmptyFiles = False,
                              suppressQuery = True,
                              suppressValidation = False,
                              cubeNetFileForValidation = hwy_abs_path)

        # Write the transit capacity configuration
        Wrangler.TransitNetwork.capacity.writeTransitVehicleToCapacity(directory = trnpath)
        Wrangler.TransitNetwork.capacity.writeTransitLineToVehicle(directory = trnpath)
        Wrangler.TransitNetwork.capacity.writeTransitPrefixToVehicle(directory = trnpath)

    Wrangler.WranglerLogger.debug("Successfully completed running %s" % os.path.abspath(__file__))
