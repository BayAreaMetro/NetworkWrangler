import argparse,collections,copy,datetime,os,pandas,shutil,sys,time
import Wrangler

# Based on NetworkWrangler\scripts\build_network.py
#
# Blueprint scenarios are No Project, Blueprint Basic, Blueprint Plus
# Specify the scenario when building
# Ex python build_network_blueprint.py net_spec_blueprint.py BlueprintBasic

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

# MANDATORY. The network you are buliding on top of.
# This should be a clone of https://github.com/BayAreaMetro/TM1_2015_Base_Network
PIVOT_DIR = os.environ['TM1_2015_Base_Network']

# OPTIONAL. If PIVOT_DIR is specified, MANDATORY.  Specifies year for PIVOT_DIR.
PIVOT_YEAR = 2015

# MANDATORY.  Should be a dictionary with keys in NET_MODES
# to a list of projects.  A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}
NETWORK_PROJECTS = None

# MANDATORY. This is the folder where the NetworkProjects (each of which is a
# local git repo) are stored.
# As of 2023 July, this is now on Box: https://mtcdrive.box.com/s/cs0dmr987kaasmi83a6irru6ts6g4y1x
NETWORK_BASE_DIR       =  os.environ['TM1_NetworkProjects']

# unused & vestigial (I think)
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
THIS_FILE = os.path.realpath(__file__)

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
    Returns first year in which my_proj shows up in the netmode's project list, plus netmode, plus number in list
    e.g. 2020.hwy.02 for second hwy project in 2020
    Returns -1 if the project is not found
    """
    for year in PROJECTS.keys():
        for proj_idx in range(len(PROJECTS[year][netmode])):
            proj = PROJECTS[year][netmode][proj_idx]
            if type(proj) is dict and my_proj == proj['name']:
                return "{}.{}.{:0>2d}".format(year,netmode,proj_idx+1)
            elif proj == my_proj:
                return "{}.{}.{:0>2d}".format(year,netmode,proj_idx+1)
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
            if (type(project_year) == int) and (project_year == -1):
                Wrangler.WranglerLogger.warning('Cannot find the {} project {} to check its requirements'.format(netmode, project))
                continue  # raise?

            Wrangler.WranglerLogger.info('Checking {} project {} ({}) for {}'.format(netmode, project, project_year, req_type))

            for req_netmode in REQUIREMENTS[netmode][project].keys():

                req_proj_list  = REQUIREMENTS[netmode][project][req_netmode]
                req_proj_years = {}
                for req_proj in req_proj_list:
                    req_project_year = getProjectYear(PROJECTS, req_proj, req_netmode)
                    # req_project_year is a string, YYYY.[trn|hwy].[number]
                    # prereq
                    if req_type=="prereq":
                        if (type(req_project_year) == int) and (req_project_year < 0):
                            is_ok = False  # required project must be found
                            Wrangler.WranglerLogger.warning("required project not found")
                        elif req_project_year > project_year:
                            is_ok = False  # and implemented before or at the same time as the project
                            Wrangler.WranglerLogger.warning("required project year {} > project year {}".format(req_project_year, project_year))

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

def preCheckRequirementsForAllProjects(networks, continue_on_warning):
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
                    Wrangler.WranglerLogger.warning("Using non-head version of project of %s" % project_name)
                    Wrangler.WranglerLogger.warning("  Applying version [%s], Head is [%s]" % (cloned_SHA1, head_SHA1))

                    cmd = "git log %s..%s" % (cloned_SHA1, head_SHA1)
                    (retcode, retStdout, retStderr) = networks[netmode]._runAndLog(cmd, run_dir = cmd_dir)
                    Wrangler.WranglerLogger.warning("  The following commits are not included:")
                    for line in retStdout:
                        Wrangler.WranglerLogger.warning("    %s" % line)

                    # test mode => warn is sufficient
                    # non-test mode => get explicit approval
                    if continue_on_warning:
                            Wrangler.WranglerLogger.warning("Continuing (continue_on_warning)")
                    elif BUILD_MODE !="test" and not continue_on_warning:
                        Wrangler.WranglerLogger.warning("  Is this ok? (y/n) ")
                        response = input("")
                        Wrangler.WranglerLogger.debug("  response = [%s]" % response)
                        if response.strip().lower()[0] != "y":
                            sys.exit(2)

                # find out if the project is stale
                else:
                    cmd = 'git show -s --format="%%ct" %s' % cloned_SHA1
                    (retcode, retStdout, retStderr) = networks[netmode]._runAndLog(cmd, run_dir = cmd_dir)
                    applied_commit_date = datetime.datetime.fromtimestamp(int(retStdout[0]))
                    applied_commit_age = datetime.datetime.now() - applied_commit_date

                    # if older than STALE_YEARS year, holler
                    STALE_YEARS = 5
                    if applied_commit_age > datetime.timedelta(days=365*STALE_YEARS):
                        Wrangler.WranglerLogger.warning("  This project was last updated %.1f years ago (over %d), on %s" % \
                                                     (applied_commit_age.days/365.0,
                                                      STALE_YEARS, applied_commit_date.strftime("%x")))
                        if continue_on_warning:
                            Wrangler.WranglerLogger.warning("Continuing (continue_on_warning)")
                        elif BUILD_MODE !="test":
                            Wrangler.WranglerLogger.warning("  Is this ok? (y/n) ")
                            response = input("")
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
    if len(PRE_REQS['trn'])>0 or len(PRE_REQS['hwy'])>0:
        writeRequirements(PRE_REQS, NETWORK_PROJECTS, req_type='prereq')
        if allPrereqsFound:
            Wrangler.WranglerLogger.debug('All PRE-REQUISITES were found. Are the PRE-REQUISITES matches correct? (y/n)')
        else:
            Wrangler.WranglerLogger.debug('!!!WARNING!!! Some PRE-REQUISITES were not found or ordered correctly.  Continue anyway? (y/n)')
        response = input("")
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
        response = input("")
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
        response = input("")
        Wrangler.WranglerLogger.debug("  response = [%s]" % response)
        if response.strip().lower() not in ["y", "yes"]:
            sys.exit(2)

    # Wrangler.WranglerLogger.debug("NETWORK_PROJECTS=%s NET_MODES=%s" % (str(NETWORK_PROJECTS), str(NET_MODES)))

###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--configword", help="optional word for network specification script")
    parser.add_argument("--continue_on_warning", help="Don't prompt the user to continue if there are warnings; just warn and continue", action="store_true")
    parser.add_argument("--skip_precheck_requirements", help="Don't precheck network requirements, stale projects, non-HEAD projects, etc", action="store_true")
    parser.add_argument("--restart_year", help="Pass year to 'restart' building network starting from this rather than from the beginning. e.g., 2025")
    parser.add_argument("--restart_mode", choices=['hwy','trn'], help="If restart_year is passed, this is also required.")
    parser.add_argument("--create_project_diffs", help="Pass this to create proejct diffs information for each project. NOTE: THIS WILL BE SLOW", action="store_true")
    parser.add_argument("net_spec", metavar="network_specification.py", help="Script which defines required variables indicating how to build the network")
    parser.add_argument("netvariant", choices=["Baseline", "Blueprint", "Alt1", "Alt2", "NextGenFwy","TIP2023", "NGFNoProject", "NGFNoProjectNoSFCordon"], help="Specify which network variant network to create.")
    args = parser.parse_args()

    NOW         = time.strftime("%Y%b%d.%H%M%S")
    BUILD_MODE  = None # regular
    TRANSIT_CAPACITY_DIR = os.path.join(PIVOT_DIR, "trn")
    TRN_SUBDIR       = "trn"
    TRN_NET_NAME     = "Transit_Lines"
    HWY_SUBDIR       = "hwy"
    HWY_NET_NAME     = "freeflow.net"


    PROJECT = "Blueprint"

    # Read the configuration
    NETWORK_CONFIG = args.net_spec
    NET_VARIANT    = args.netvariant

    # networks and log file will be in BlueprintNetworks
    if not os.path.exists("BlueprintNetworks"):
        os.mkdir("BlueprintNetworks")

    LOG_FILENAME = "build%snetwork_%s_%s_%s.info.LOG" % ("TEST" if BUILD_MODE=="test" else "", PROJECT, NET_VARIANT, NOW)
    Wrangler.setupLogging(os.path.join("BlueprintNetworks",LOG_FILENAME),
                          os.path.join("BlueprintNetworks",LOG_FILENAME.replace("info", "debug")))
    Wrangler.WranglerLogger.debug("Args: {}".format(args))

    exec(open(NETWORK_CONFIG).read())

    # Use the NGF_NoProject git tag when building a Next Gen Freeways No Project variant
    if NET_VARIANT=="NGFNoProject" or NET_VARIANT=="NGFNoProjectNoSFCordon":
       TAG = "NGF_NoProject"

    # Verify mandatory fields are set
    if PROJECT==None:
        print("PROJECT not set in %s" % NETWORK_CONFIG)
        sys.exit(2)
    if TAG==None:
        print("TAG not set in %s" % NETWORK_CONFIG)
        sys.exit(2)
    if NETWORK_PROJECTS==None:
        print("NETWORK_PROJECTS not set in %s" % NETWORK_CONFIG)
        sys.exit(2)

    if TRANSIT_CAPACITY_DIR:
        Wrangler.TransitNetwork.capacity = Wrangler.TransitCapacity(directory=TRANSIT_CAPACITY_DIR)

    # Create a scratch directory to check out project repos into
    SCRATCH_SUBDIR = "scratch"
    TEMP_SUBDIR    = "Wrangler_tmp_" + NOW
    if not os.path.exists(SCRATCH_SUBDIR): os.mkdir(SCRATCH_SUBDIR)
    os.chdir(SCRATCH_SUBDIR)

    os.environ["CHAMP_node_names"] = os.path.join(PIVOT_DIR,"Node Description.xls")

    PIVOT_DIR_HWY = PIVOT_DIR
    PIVOT_DIR_TRN = PIVOT_DIR

    # restart means we want to start with that year/mode
    # e.g., for restart=2020 trn, start applying 2020 transit projects, using 2020 hwy and 2015 transit
    #       for restart=2020 hwy, start applying 2020 hwy projects, using 2015 hwy and 2015 transit
    #
    if args.restart_year or args.restart_mode:
        # both are required
        if not args.restart_year or not args.restart_mode:
            Wrangler.WranglerLogger.fatal("Both args.restart_year and args.restart_mode are required if one is supplied; args={}".format(args))
            sys.exit(-1)
        
        trn_network_year = int(args.restart_year) - 5
        hwy_network_year = int(args.restart_year) if args.restart_mode == "trn" else int(args.restart_year) - 5

        PIVOT_DIR_HWY = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(hwy_network_year, NET_VARIANT))
        PIVOT_DIR_TRN = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(trn_network_year, NET_VARIANT))
        TRN_NET_NAME  = "transitLines"

        Wrangler.WranglerLogger.info("Using PIVOT_DIR_HWY: {}".format(PIVOT_DIR_HWY))
        Wrangler.WranglerLogger.info("Using PIVOT_DIR_TRN: {}".format(PIVOT_DIR_TRN))

    networks = {
        'hwy' :Wrangler.HighwayNetwork(modelType=args.model_type, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR_HWY,"hwy"),
                                       networkBaseDir=NETWORK_BASE_DIR,
                                       networkProjectSubdir=NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR_HWY else False,
                                       tag=TAG,
                                       tempdir=TEMP_SUBDIR,
                                       networkName="hwy",
                                       tierNetworkName=HWY_NET_NAME),
        'trn':Wrangler.TransitNetwork( modelType=args.model_type, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR_TRN,"trn"),
                                       networkBaseDir=NETWORK_BASE_DIR,
                                       networkProjectSubdir=NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR_TRN else False,
                                       networkName=TRN_NET_NAME)
    }

    # For projects applied in a pivot network (because they won't show up in the current project list)
    if APPLIED_PROJECTS != None:
        for proj in APPLIED_PROJECTS:
            networks['hwy'].appliedProjects[proj]=TAG


    # Wrangler.WranglerLogger.debug("NETWORK_PROJECTS=%s NET_MODES=%s" % (str(NETWORK_PROJECTS), str(NET_MODES)))
    if args.skip_precheck_requirements:
        Wrangler.WranglerLogger.info("skip_precheck_requirements passed so skipping preCheckRequirementsForAllProjects()")
    else:
        preCheckRequirementsForAllProjects(networks, args.continue_on_warning)

    # create the subdir for SET_CAPCLASS with set_capclass.job as apply.s
    SET_CAPCLASS     = "set_capclass"
    SET_CAPCLASS_DIR = os.path.join(TEMP_SUBDIR, SET_CAPCLASS)
    os.makedirs(SET_CAPCLASS_DIR)
    source_file      = os.path.join(os.path.dirname(THIS_FILE), "set_capclass.job")
    shutil.copyfile( source_file, os.path.join(SET_CAPCLASS_DIR, "apply.s"))

    networks_without_earthquake = {}

    # Network Loop #2: Now that everything has been checked, build the networks.
    for YEAR in NETWORK_PROJECTS.keys():
        if args.restart_year and YEAR < int(args.restart_year):
            Wrangler.WranglerLogger.info("Restart year {} specified; skipping {}".format(args.restart_year, YEAR))
            continue

        projects_for_year = NETWORK_PROJECTS[YEAR]

        appliedcount = 0
        for netmode in NET_MODES:
            if args.restart_mode == "trn" and netmode == "hwy" and YEAR == int(args.restart_year):
                Wrangler.WranglerLogger.info("Restart mode {} specified; skipping {}".format(args.restart_mode, netmode))
                continue

            Wrangler.WranglerLogger.info("Building {} {} networks".format(YEAR, netmode))

            for project in projects_for_year[netmode]:
                (project_name, projType, tag, kwargs) = getProjectAttributes(project)
                if tag == None: tag = TAG

                Wrangler.WranglerLogger.info("Applying project [{}] of type [{}] with tag [{}] and kwargs[{}]".format(project_name, projType, tag, kwargs))
                if projType=='plan':
                    continue

                # save a copy of this network instance for comparison
                if args.create_project_diffs:
                    network_without_project = copy.deepcopy(networks[netmode])

                applied_SHA1 = None
                cloned_SHA1 = networks[netmode].cloneProject(networkdir=project_name, tag=tag,
                                                             projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                (parentdir, networkdir, gitdir, projectsubdir) = networks[netmode].getClonedProjectArgs(project_name, None, projType, TEMP_SUBDIR)

                applied_SHA1 = networks[netmode].applyProject(parentdir, networkdir, gitdir, projectsubdir, **kwargs)
                appliedcount += 1

                # Create difference report for this project
                # TODO: roadway not supported yet
                if args.create_project_diffs and netmode!="hwy":
                    # difference information to be store in network_dir netmode_projectname
                    # e.g. BlueprintNetworks\net_2050_Blueprint\trn_BP_Transbay_Crossing
                    project_diff_folder = os.path.join("..", "BlueprintNetworks", 
                                                       "net_{}_{}".format(YEAR, NET_VARIANT), 
                                                       "{}_{}".format(HWY_SUBDIR if netmode == "hwy" else TRN_SUBDIR, project_name))
                    hwypath=os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), HWY_SUBDIR)

                    # the project may get applied multiple times -- e.g., for different phases
                    suffix_num = 1
                    project_diff_folder_with_suffix = project_diff_folder
                    while os.path.exists(project_diff_folder_with_suffix):
                        suffix_num += 1
                        project_diff_folder_with_suffix = "{}_{}".format(project_diff_folder, suffix_num)

                    Wrangler.WranglerLogger.debug("Creating project_diff_folder: {}".format(project_diff_folder_with_suffix))
                    
                    # new!
                    networks[netmode].reportDiff(network_without_project, project_diff_folder_with_suffix, project_name,
                                                 roadwayNetworkFile=os.path.join(os.path.abspath(hwypath), HWY_NET_NAME))

                # if hwy project has set_capclass override, copy it to set_capclass/apply.s
                set_capclass_override = os.path.join(TEMP_SUBDIR, project_name, "set_capclass.job")
                if os.path.exists(set_capclass_override):
                    dest_file = os.path.join(SET_CAPCLASS_DIR, "apply.s")
                    shutil.copyfile(set_capclass_override, dest_file)
                    Wrangler.WranglerLogger.info("Copied override {} to {}".format(set_capclass_override, dest_file))


        if appliedcount == 0:
            Wrangler.WranglerLogger.info("No applied projects for this year -- skipping output")
            continue

        # Baseline AND YEAR >= 2035 get SLR, covered in next clause
        if NET_VARIANT!="Baseline" or YEAR<2035:

            hwypath=os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), HWY_SUBDIR)
            if not os.path.exists(hwypath): os.makedirs(hwypath)
            trnpath = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), TRN_SUBDIR)
            if not os.path.exists(trnpath): os.makedirs(trnpath)

            # apply set_capclass before writing any hwy network
            applied_SHA1 = networks['hwy'].applyProject(parentdir=TEMP_SUBDIR, networkdir=SET_CAPCLASS,
                                                    gitdir=os.path.join(TEMP_SUBDIR, SET_CAPCLASS), **kwargs)

            networks['hwy'].write(path=hwypath,name=HWY_NET_NAME,suppressQuery=True,
                              suppressValidation=True) # MTC doesn't have turn penalties

            networks['trn'].write(path=trnpath,
                              name="transitLines",
                              writeEmptyFiles = False,
                              suppressQuery = True if BUILD_MODE=="test" else False,
                              suppressValidation = False,
                              cubeNetFileForValidation = os.path.join(os.path.abspath(hwypath), HWY_NET_NAME))


            # Write the transit capacity configuration
            Wrangler.TransitNetwork.capacity.writeTransitVehicleToCapacity(directory = trnpath)
            Wrangler.TransitNetwork.capacity.writeTransitLineToVehicle(directory = trnpath)
            Wrangler.TransitNetwork.capacity.writeTransitPrefixToVehicle(directory = trnpath)

        # build the Baseline, with Sea Level Rise effects
        if NET_VARIANT=="Baseline" and YEAR>=2035:

            # Sea Level Rise effects
            # no inundation prior to 2035
            # 1 foot between 2035 and 2045
            # 2 foot in 2050
            if YEAR >= 2035 and YEAR < 2050:
                BP_SLR_PROJECT = {'name':"BP_Sea_Level_Rise_Inundation", 'kwargs':{'MODELYEAR':'2035'}}
            if YEAR == 2050:
                BP_SLR_PROJECT = {'name':"BP_Sea_Level_Rise_Inundation", 'kwargs':{'MODELYEAR':'2050'}}

            # it would be nice if this were more automatic...
            networks['hwy'].saveNetworkFiles(suffix="_pre_SLR", to_suffix=True)

            networks_bp_baseline = {}
            networks_bp_baseline['hwy'] = copy.deepcopy(networks['hwy'])
            networks_bp_baseline['trn'] = copy.deepcopy(networks['trn'])

            for netmode in NET_MODES:
                (project_name, projType, tag, kwargs) = getProjectAttributes(BP_SLR_PROJECT)
                # Wrangler.WranglerLogger.debug("BP SLR Project {} has project_name=[{}] projType=[{}] tag=[{}] kwargs=[{}]".format(BP_SLR_PROJECT,
                #                                project_name, projType, tag, kwargs))
                applied_SHA1 = None
                copyloned_SHA1 = networks_bp_baseline[netmode].cloneProject(networkdir=project_name, tag=tag,
                                                                         projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                (parentdir, networkdir, gitdir, projectsubdir) = networks_bp_baseline[netmode].getClonedProjectArgs(project_name, None, projType, TEMP_SUBDIR)
                applied_SHA1 = networks_bp_baseline[netmode].applyProject(parentdir, networkdir, gitdir, projectsubdir, **kwargs)

                hwypath=os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), HWY_SUBDIR)
                if not os.path.exists(hwypath): os.makedirs(hwypath)
                trnpath = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), TRN_SUBDIR)
                if not os.path.exists(trnpath): os.makedirs(trnpath)

            applied_SHA1 = networks_bp_baseline['hwy'].applyProject(parentdir=TEMP_SUBDIR, networkdir=SET_CAPCLASS,
                                                                 gitdir=os.path.join(TEMP_SUBDIR, SET_CAPCLASS))

            networks_bp_baseline['hwy'].write(path=hwypath,name=HWY_NET_NAME,suppressQuery=True,
                                           suppressValidation=True) # MTC doesn't have turn penalties

            networks_bp_baseline['trn'].write(path=trnpath,
                                           name="transitLines",
                                           writeEmptyFiles = False,
                                           suppressQuery = True if BUILD_MODE=="test" else False,
                                           suppressValidation = False,
                                           cubeNetFileForValidation = os.path.join(os.path.abspath(hwypath), HWY_NET_NAME))


            # Write the transit capacity configuration
            Wrangler.TransitNetwork.capacity.writeTransitVehicleToCapacity(directory = trnpath)
            Wrangler.TransitNetwork.capacity.writeTransitLineToVehicle(directory = trnpath)
            Wrangler.TransitNetwork.capacity.writeTransitPrefixToVehicle(directory = trnpath)

            # revert back to the plus rowadway network without BP_Sea_Level_Rise_Inundation
            networks['hwy'].saveNetworkFiles(suffix="_pre_SLR", to_suffix=False)


    Wrangler.WranglerLogger.debug("Successfully completed running %s" % os.path.abspath(__file__))
