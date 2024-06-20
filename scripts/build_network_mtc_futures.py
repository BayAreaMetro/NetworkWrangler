import argparse,collections,copy,datetime,os,pandas,shutil,sys,time
import Wrangler

# Based on NetworkWrangler\scripts\build_network.py
#
# Builds 3 futures networks.  Use with net_spec_horizon.py
#


import build_network_mtc

###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=build_network_mtc.USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--configword", help="optional word for network specification script")
    parser.add_argument("--analysis", choices=["Round1","Round2","PPA","PPA_NoSLR"], help="Specify which set of analysis are relevant for these networks.", default="Round1")
    parser.add_argument("--continue_on_warning", help="Don't prompt the user to continue if there are warnings; just warn and continue", action="store_true")
    parser.add_argument("--skip_precheck_requirements", help="Don't precheck network requirements, stale projects, non-HEAD projects, etc", action="store_true")
    parser.add_argument("--create_project_diffs", help="Pass this to create proejct diffs information for each project. NOTE: THIS WILL BE SLOW", action="store_true")
    parser.add_argument("net_spec", metavar="network_specification.py", help="Script which defines required variables indicating how to build the network")
    parser.add_argument("future", choices=["CleanAndGreen", "RisingTides", "BackToTheFuture"], help="Specify which Future Scenario for which to create networks")
    args = parser.parse_args()

    NOW         = time.strftime("%Y%b%d.%H%M%S")
    BUILD_MODE  = None # regular
    PIVOT_DIR        = build_network_mtc.PIVOT_DIR
    NETWORK_PROJECTS = build_network_mtc.NETWORK_PROJECTS
    TRANSIT_CAPACITY_DIR = os.path.join(PIVOT_DIR, "trn")
    TRN_NET_NAME     = "Transit_Lines"
    HWY_NET_NAME     = "freeflow.net"
    OUT_DIR          = "network_{}"  # YEAR

    TAG = 'HEAD'  # 'PPA' tag isn't propogated yet

    if args.analysis == "Round1":
        PROJECT = "FU1"
    elif args.analysis == "Round2":
        PROJECT = "FU2"   
    elif args.analysis in ["PPA","PPA_NoSLR"]:
        PROJECT = args.analysis

    # Read the configuration
    NETWORK_CONFIG = args.net_spec
    SCENARIO       = args.future

    LOG_FILENAME = "build%snetwork_%s_%s_%s.info.LOG" % ("TEST" if BUILD_MODE=="test" else "", PROJECT, SCENARIO, NOW)
    Wrangler.setupLogging(LOG_FILENAME, LOG_FILENAME.replace("info", "debug"))
    exec(open(NETWORK_CONFIG).read())

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

    networks = {
        'hwy' :Wrangler.HighwayNetwork(modelType=Wrangler.Network.MODEL_TYPE_TM1, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR,"hwy"),
                                       networkBaseDir=build_network_mtc.NETWORK_BASE_DIR,
                                       networkProjectSubdir=build_network_mtc.NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=build_network_mtc.NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=build_network_mtc.NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR else False,
                                       tag=TAG,
                                       tempdir=TEMP_SUBDIR,
                                       networkName="hwy",
                                       tierNetworkName=HWY_NET_NAME),
        'trn':Wrangler.TransitNetwork( modelType=Wrangler.Network.MODEL_TYPE_TM1, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR,"trn"),
                                       networkBaseDir=build_network_mtc.NETWORK_BASE_DIR,
                                       networkProjectSubdir=build_network_mtc.NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=build_network_mtc.NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=build_network_mtc.NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR else False,
                                       networkName=TRN_NET_NAME)
    }

    # For projects applied in a pivot network (because they won't show up in the current project list)
    if build_network_mtc.APPLIED_PROJECTS != None:
        for proj in build_network_mtc.APPLIED_PROJECTS:
            networks['hwy'].appliedProjects[proj]=TAG


    # Wrangler.WranglerLogger.debug("NETWORK_PROJECTS=%s NET_MODES=%s" % (str(NETWORK_PROJECTS), str(NET_MODES)))
    if args.skip_precheck_requirements:
        Wrangler.WranglerLogger.info("skip_precheck_requirements passed so skipping preCheckRequirementsForAllProjects()")
    else:
        build_network_mtc.preCheckRequirementsForAllProjects(NETWORK_PROJECTS, TEMP_SUBDIR, networks, args.continue_on_warning)

    # create the subdir for SET_CAPCLASS with set_capclass.job as apply.s
    SET_CAPCLASS     = "set_capclass"
    SET_CAPCLASS_DIR = os.path.join(TEMP_SUBDIR, SET_CAPCLASS)
    os.makedirs(SET_CAPCLASS_DIR)
    source_file      = os.path.join(os.path.dirname(build_network_mtc.THIS_FILE), "set_capclass.job")
    shutil.copyfile( source_file, os.path.join(SET_CAPCLASS_DIR, "apply.s"))

    networks_without_earthquake = {}

    # Network Loop #2: Now that everything has been checked, build the networks.
    for YEAR in NETWORK_PROJECTS.keys():
        projects_for_year = NETWORK_PROJECTS[YEAR]

        appliedcount = 0
        for netmode in build_network_mtc.NET_MODES:
            Wrangler.WranglerLogger.info("Building {} {} networks".format(YEAR, netmode))

            # restore version without earthquake
            if netmode in networks_without_earthquake:
                Wrangler.WranglerLogger.info("Restoring version without earthquake")
                networks[netmode] = networks_without_earthquake[netmode]
                appliedcount += 1 # increment to trigger writing this out
                del networks_without_earthquake[netmode]

                if netmode == "hwy":
                    shutil.move(os.path.join("FREEFLOW_WITHOUT_EARTHQUAKE.BLD"),
                                os.path.join("FREEFLOW.BLD"))

            for project in projects_for_year[netmode]:
                (project_name, projType, tag, branch, kwargs) = build_network_mtc.getProjectAttributes(project)
                if tag == None: tag = TAG

                Wrangler.WranglerLogger.info("Applying project [{}] of type [{}] with tag [{}] and kwargs[{}]".format(project_name, projType, tag, kwargs))
                if projType=='plan':
                    continue

                # save a copy of this network instance for comparison
                if args.create_project_diffs:
                    network_without_project = copy.deepcopy(networks[netmode])

                applied_SHA1 = None
                cloned_SHA1 = networks[netmode].cloneProject(networkdir=project_name, tag=tag, branch=branch,
                                                             projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                (parentdir, networkdir, gitdir, projectsubdir) = networks[netmode].getClonedProjectArgs(project_name, None, projType, TEMP_SUBDIR)

                if ((project_name == "Earthquake") and ((PROJECT == "FU1" and args.future in ["CleanAndGreen","BackToTheFuture"]) or (PROJECT == "FU2"))):
                    # Then this "project" is only temporary, so save aside a deepcopy of the network PRIOR
                    # to the apply to restore after we write it
                    networks_without_earthquake[netmode] = copy.deepcopy(networks[netmode])
                    if netmode == "hwy":
                        shutil.copyfile(os.path.join("FREEFLOW.BLD"),
                                        os.path.join("FREEFLOW_WITHOUT_EARTHQUAKE.BLD"))

                applied_SHA1 = networks[netmode].applyProject(parentdir, networkdir, gitdir, projectsubdir, **kwargs)
                appliedcount += 1

                # Create difference report for this project
                # TODO: roadway not supported yet
                if args.create_project_diffs and netmode!="hwy":
                    # difference information to be store in network_dir netmode_projectname
                    # e.g. BlueprintNetworks\net_2050_Blueprint\trn_BP_Transbay_Crossing
                    project_diff_folder = os.path.join("..", "BlueprintNetworks", 
                                                       "net_{}_{}".format(YEAR, NET_VARIANT), 
                                                       "{}_{}".format(build_network_mtc.HWY_SUBDIR if netmode == "hwy" else build_network_mtc.TRN_SUBDIR, project_name))
                    hwypath=os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), build_network_mtc.HWY_SUBDIR)

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


            # apply set_capclass before writing any hwy network
            if netmode == "hwy" and appliedcount > 0:
                applied_SHA1 = networks[netmode].applyProject(parentdir=TEMP_SUBDIR, networkdir=SET_CAPCLASS,
                                                              gitdir=os.path.join(TEMP_SUBDIR, SET_CAPCLASS))

        if appliedcount == 0:
            Wrangler.WranglerLogger.info("No applied projects for this year -- skipping output")
            continue

        # Initialize output subdirectories up a level (not in scratch)
        hwypath=os.path.join("..", SCENARIO, OUT_DIR.format(YEAR),build_network_mtc.HWY_SUBDIR)
        if not os.path.exists(hwypath): os.makedirs(hwypath)
        trnpath = os.path.join("..", SCENARIO, OUT_DIR.format(YEAR),build_network_mtc.TRN_SUBDIR)
        if not os.path.exists(trnpath): os.makedirs(trnpath)

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

    Wrangler.WranglerLogger.debug("Successfully completed running %s" % os.path.abspath(__file__))
