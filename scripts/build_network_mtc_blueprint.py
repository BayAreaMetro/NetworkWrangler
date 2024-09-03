import argparse,collections,copy,datetime,os,pandas,pathlib,shutil,sys,tempfile,time
import Wrangler

# Based on NetworkWrangler\scripts\build_network.py
#
# Blueprint scenarios are No Project, Blueprint Basic, Blueprint Plus
# Specify the scenario when building
# Ex python build_network_blueprint.py net_spec_blueprint.py BlueprintBasic

import build_network_mtc

###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=build_network_mtc.USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--configword", help="optional word for network specification script")
    parser.add_argument("--continue_on_warning", help="Don't prompt the user to continue if there are warnings; just warn and continue", action="store_true")
    parser.add_argument("--skip_precheck_requirements", help="Don't precheck network requirements, stale projects, non-HEAD projects, etc", action="store_true", default=True)
    parser.add_argument("--restart_year", help="Pass year to 'restart' building network starting from this rather than from the beginning. e.g., 2025")
    parser.add_argument("--restart_mode", choices=['hwy','trn'], help="If restart_year is passed, this is also required.")
    parser.add_argument("--create_project_diffs", help="Pass this to create project diffs information for EVERY project. NOTE: THIS WILL BE SLOW", action="store_true")
    parser.add_argument("--create_project_diff",  help="Pass a project name to create project diffs information for that project", type=str, default=None)
    parser.add_argument("net_spec", metavar="network_specification.py", help="Script which defines required variables indicating how to build the network")
    parser.add_argument("netvariant", choices=["Baseline", "Blueprint", "Alt1", "Alt2", "NextGenFwy","TIP2023", "TIP2025", "NGFNoProject", "NGFNoProjectNoSFCordon", "NGFround2NoProject"], help="Specify which network variant network to create.")
    args = parser.parse_args()

    NOW              = time.strftime("%Y%b%d.%H%M%S")
    BUILD_MODE       = None # regular
    PIVOT_DIR        = build_network_mtc.PIVOT_DIR
    NETWORK_PROJECTS = build_network_mtc.NETWORK_PROJECTS
    TRANSIT_CAPACITY_DIR = os.path.join(PIVOT_DIR, "trn")
    TRN_NET_NAME     = "Transit_Lines"
    HWY_NET_NAME     = "freeflow.net"

    PROJECT = "Blueprint"
    TAG     = None
    ADDITONAL_ROADWAY_ATTRS = []

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
    if NET_VARIANT=="NGFround2NoProject":
       TAG = "NGF_R2_NoProject"

    # Verify mandatory fields are set
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

        ALL_NETWORK_YEARS = list(NETWORK_PROJECTS.keys())
        restart_year_index = ALL_NETWORK_YEARS.index(int(args.restart_year))
        trn_network_year = ALL_NETWORK_YEARS[restart_year_index-1]
        hwy_network_year = ALL_NETWORK_YEARS[restart_year_index] if args.restart_mode == "trn" else ALL_NETWORK_YEARS[restart_year_index-1]

        PIVOT_DIR_HWY = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(hwy_network_year, NET_VARIANT))
        PIVOT_DIR_TRN = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(trn_network_year, NET_VARIANT))
        TRN_NET_NAME  = "transitLines"

        Wrangler.WranglerLogger.info("Using PIVOT_DIR_HWY: {}".format(PIVOT_DIR_HWY))
        Wrangler.WranglerLogger.info("Using PIVOT_DIR_TRN: {}".format(PIVOT_DIR_TRN))

    networks = {
        'hwy' :Wrangler.HighwayNetwork(modelType=Wrangler.Network.MODEL_TYPE_TM1, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR_HWY,"hwy"),
                                       networkBaseDir=build_network_mtc.NETWORK_BASE_DIR,
                                       networkProjectSubdir=build_network_mtc.NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=build_network_mtc.NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=build_network_mtc.NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR_HWY else False,
                                       tag=TAG,
                                       tempdir=TEMP_SUBDIR,
                                       networkName="hwy",
                                       tierNetworkName=HWY_NET_NAME),
        'trn':Wrangler.TransitNetwork( modelType=Wrangler.Network.MODEL_TYPE_TM1, modelVersion=1.0,
                                       basenetworkpath=os.path.join(PIVOT_DIR_TRN,"trn"),
                                       networkBaseDir=build_network_mtc.NETWORK_BASE_DIR,
                                       networkProjectSubdir=build_network_mtc.NETWORK_PROJECT_SUBDIR,
                                       networkSeedSubdir=build_network_mtc.NETWORK_SEED_SUBDIR,
                                       networkPlanSubdir=build_network_mtc.NETWORK_PLAN_SUBDIR,
                                       isTiered=True if PIVOT_DIR_TRN else False,
                                       networkName=TRN_NET_NAME)
    }

    # For projects applied in a pivot network (because they won't show up in the current project list)
    if build_network_mtc.APPLIED_PROJECTS != None:
        for proj in build_network_mtc.APPLIED_PROJECTS:
            networks['hwy'].appliedProjects[proj]=TAG


    # Wrangler.WranglerLogger.debug("NETWORK_PROJECTS=%s NET_MODES=%s" % (str(NETWORK_PROJECTS), str(build_network_mtc.NET_MODES)))
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
        if args.restart_year and YEAR < int(args.restart_year):
            Wrangler.WranglerLogger.info("Restart year {} specified; skipping {}".format(args.restart_year, YEAR))
            continue

        projects_for_year = NETWORK_PROJECTS[YEAR]

        appliedcount = 0
        for netmode in build_network_mtc.NET_MODES:
            if args.restart_mode == "trn" and netmode == "hwy" and YEAR == int(args.restart_year):
                Wrangler.WranglerLogger.info("Restart mode {} specified; skipping {}".format(args.restart_mode, netmode))
                continue

            Wrangler.WranglerLogger.info("Building {} {} networks".format(YEAR, netmode))
            project_diff_report_num = 1

            for project in projects_for_year[netmode]:
                (project_name, projType, tag, branch, kwargs) = build_network_mtc.getProjectAttributes(project)
                if tag == None: tag = TAG

                Wrangler.WranglerLogger.info(f"Applying project [{project_name=}] [{projType=}] on [{branch=}] with [{tag=}] and [{kwargs=}]")
                if projType=='plan':
                    continue

                # save a copy of this network instance for comparison
                network_without_project = None
                if (args.create_project_diffs and (project not in build_network_mtc.SKIP_PROJ_DIFFS)) or (args.create_project_diff == project_name):
                    if netmode == "trn":
                        network_without_project = copy.deepcopy(networks[netmode])
                    elif netmode == 'hwy':
                        # the network state is not in the object, but in the files in scratch. write these to tempdir
                        network_without_project = pathlib.Path(tempfile.mkdtemp())
                        Wrangler.WranglerLogger.debug(f"Saving previous network into tempdir {network_without_project}")
                        networks[netmode].writeShapefile(network_without_project, suffix="_prev",additional_roadway_attrs=ADDITONAL_ROADWAY_ATTRS)

                applied_SHA1 = None
                cloned_SHA1 = networks[netmode].cloneProject(networkdir=project_name, tag=tag,branch=branch,
                                                             projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                (parentdir, networkdir, gitdir, projectsubdir) = networks[netmode].getClonedProjectArgs(project_name, None, projType, TEMP_SUBDIR)

                applied_SHA1 = networks[netmode].applyProject(parentdir, networkdir, gitdir, projectsubdir, **kwargs)
                appliedcount += 1

                # Create difference report for this project
                if (args.create_project_diffs and (project not in build_network_mtc.SKIP_PROJ_DIFFS)) or (args.create_project_diff == project_name):
                    # difference information to be store in network_dir netmode_projectname
                    # e.g. BlueprintNetworks\net_2050_Blueprint\01_trn_BP_Transbay_Crossing
                    project_diff_folder = pathlib.Path.cwd().parent / "BlueprintNetworks" / f"ProjectDiffs_{NET_VARIANT}" / \
                         f"net_{YEAR}_{project_diff_report_num:02}_{build_network_mtc.HWY_SUBDIR if netmode == 'hwy' else build_network_mtc.TRN_SUBDIR}_{project_name}"

                    # the project may get applied multiple times -- e.g., for different phases
                    suffix_num = 1
                    project_diff_folder_with_suffix = project_diff_folder
                    while project_diff_folder_with_suffix.exists():
                        suffix_num += 1
                        project_diff_folder_with_suffix = pathlib.Path(f"{str(project_diff_folder)}_{suffix_num}")

                    Wrangler.WranglerLogger.debug(f"Creating project_diff_folder: {project_diff_folder_with_suffix}")
                    
                    reported_diff_ret = networks[netmode].reportDiff(netmode, other_network=network_without_project, 
                                                 directory=project_diff_folder_with_suffix, project_gitdir=gitdir, 
                                                 report_description=project_name, additional_roadway_attrs=ADDITONAL_ROADWAY_ATTRS)
                    del network_without_project

                    if reported_diff_ret:
                        project_diff_report_num += 1

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

            hwypath=os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), build_network_mtc.HWY_SUBDIR)
            if not os.path.exists(hwypath): os.makedirs(hwypath)
            trnpath = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), build_network_mtc.TRN_SUBDIR)
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
                SLR_PROJECT = {'name':"RTP25_Sea_Level_Rise_Inundation", 'kwargs':{'MODELYEAR':'2035'}}
            if YEAR == 2050:
                SLR_PROJECT = {'name':"RTP25_Sea_Level_Rise_Inundation", 'kwargs':{'MODELYEAR':'2050'}}

            # it would be nice if this were more automatic...
            networks['hwy'].saveNetworkFiles(suffix="_pre_SLR", to_suffix=True)

            networks_bp_baseline = {}
            networks_bp_baseline['hwy'] = copy.deepcopy(networks['hwy'])
            networks_bp_baseline['trn'] = copy.deepcopy(networks['trn'])

            for netmode in build_network_mtc.NET_MODES:
                (project_name, projType, tag, branch, kwargs) = build_network_mtc.getProjectAttributes(SLR_PROJECT)
                # Wrangler.WranglerLogger.debug("SLR Project {} has project_name=[{}] projType=[{}] tag=[{}] kwargs=[{}]".format(SLR_PROJECT,
                #                                project_name, projType, tag, kwargs))
                applied_SHA1 = None
                copyloned_SHA1 = networks_bp_baseline[netmode].cloneProject(networkdir=project_name, tag=tag, branch=branch,
                                                                         projtype=projType, tempdir=TEMP_SUBDIR, **kwargs)
                (parentdir, networkdir, gitdir, projectsubdir) = networks_bp_baseline[netmode].getClonedProjectArgs(project_name, None, projType, TEMP_SUBDIR)
                applied_SHA1 = networks_bp_baseline[netmode].applyProject(parentdir, networkdir, gitdir, projectsubdir, **kwargs)

                hwypath=os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), build_network_mtc.HWY_SUBDIR)
                if not os.path.exists(hwypath): os.makedirs(hwypath)
                trnpath = os.path.join("..", "BlueprintNetworks", "net_{}_{}".format(YEAR, NET_VARIANT), build_network_mtc.TRN_SUBDIR)
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
