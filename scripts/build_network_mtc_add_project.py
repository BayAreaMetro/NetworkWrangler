import argparse, collections, copy, datetime, os, pandas, re, shutil, sys, time
import Wrangler

USAGE = """

  Builds a network plus project, given a base network and a project and project_short_id.

  Creates PPA_DIR\project_short_id
    with subdirs BASE_DIR_project_short_id

  Alternatively, the user can specify the input directory, output directory and directory with
  the network project.  Default use case is PPA.

"""
PPA_DIR = "L:\\RTP2021_PPA\\Projects"
NODE_NAMES = (
    "M:\\Application\\Model One\\Networks\\TM1_2015_Base_Network\\Node Description.xls"
)
THIS_FILE = os.path.realpath(__file__)

# for transit network validation output
os.environ["CHAMP_node_names"] = NODE_NAMES


def findBaseDirectory(future):
    """
    Returns the highest version base directory for the given future.
    Right now, that just means sorting alphabetically and returning the last one.

    Queries the user which base directory to use and returns the base directory name (not full path)
    """
    dir_list = sorted(os.listdir(PPA_DIR))

    model_id_re = re.compile("^2050_TM151_PPA_(BF|CG|RT)_(.*)")
    return_dirs = []

    for dirname in dir_list:
        match = model_id_re.match(dirname)
        if match == None:
            continue
        future_code = match.group(1)
        run_version = match.group(2)

        if future == "CleanAndGreen" and future_code == "CG":
            return_dirs.append(dirname)
        elif future == "RisingTides" and future_code == "RT":
            return_dirs.append(dirname)
        elif future == "BackToTheFuture" and future_code == "BF":
            return_dirs.append(dirname)

    if len(return_dirs) == 0:
        raise Exception("No base directories found")

    print("The following base directory options were found: ")
    for dirname in return_dirs:
        print(" -> {}".format(dirname))
    print(
        "Which base directory do you want to use? (No response means {}) ".format(
            return_dirs[-1]
        )
    )
    response = raw_input("")
    print("  response = [%s]" % response)

    response = response.strip()
    if response == "":
        return return_dirs[-1]

    if response in return_dirs:
        return response

    raise Exception("Didn't understand response [{}]".format(response))


def determineProjectDirectory(OUTPUT_DIR, BASE_DIR, project_short_id):

    dir_list = sorted(os.listdir(OUTPUT_DIR))
    dir_re_str = r"^{}_{}_(\d\d)$".format(
        re.escape(BASE_DIR), re.escape(project_short_id)
    )
    dir_re = re.compile(dir_re_str)
    existing_suffixes = []

    print(dir_re_str)

    for dirname in dir_list:
        print(dirname)
        match = dir_re.match(dirname)
        if match == None:
            continue
        suffix = match.group(1)
        existing_suffixes.append(int(suffix))

    print(
        "Found existing project directories with suffixes: {}".format(existing_suffixes)
    )
    proposed_suffix = 0
    if len(existing_suffixes) > 0:
        proposed_suffix = existing_suffixes[-1] + 1
    print(
        "Which suffix number do you want to use? (No response means {}) ".format(
            proposed_suffix
        )
    )
    response = input("")
    print("  response = [%s]" % response)

    response_suffix = proposed_suffix
    if response != "":
        response_suffix = int(response.strip())

    if response_suffix in existing_suffixes:
        raise Exception("Cannot use suffix that is already in use")

    project_dir = os.path.join(
        OUTPUT_DIR, "{}_{}_{:02d}".format(BASE_DIR, project_short_id, response_suffix)
    )
    print("OUTPUT_FUTURE_DIR is {}".format(project_dir))

    return project_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "future",
        choices=[
            "CleanAndGreen",
            "RisingTides",
            "BackToTheFuture",
            "all",
            "None",
            "FinalBlueprint",
            "TransitRecovery",
        ],
        help="Specify which Future Scenario for which to create networks",
    )
    parser.add_argument(
        "--hwy",
        dest="hwy",
        action="store_true",
        help="Pass if project is a roadway project",
    )
    parser.add_argument(
        "--trn",
        dest="trn",
        action="store_true",
        help="Pass if project is a transit project",
    )
    parser.add_argument(
        "--input_network",
        dest="input_network",
        help="Pass input network path if desired; otherwise, PPA path is assumed",
    )
    parser.add_argument(
        "--output_network",
        dest="output_network",
        help="Pass output network path if desired; otPherwise, PPA path is assumed",
    )
    parser.add_argument(
        "--input_projects",
        dest="input_projects",
        help="Pass directory for network projects; if none passed, M:\\Application\\Model One\\NetworkProjects is assumed",
    )
    parser.add_argument(
        "--kwarg",
        dest="kwarg",
        help="To pass keyword args to project apply(), pass keyword and value",
        nargs=2,
    )
    parser.add_argument(
        "--kwarg2",
        dest="kwarg2",
        help="To pass keyword args to project apply(), pass keyword and value",
        nargs=2,
    )
    parser.add_argument("--tag", dest="tag", help="tags for project")
    parser.add_argument(
        "project_short_id", help="Short ID of project, to be used for directory"
    )
    parser.add_argument("project", help="Project to add", nargs="+")
    args = parser.parse_args()

    if not args.hwy and not args.trn:
        print(
            "Project must be roadway, transit or both.  Please specify --hwy and/or --trn"
        )
        sys.exit(2)

    PROJECT = "PPA"
    if args.future == "FinalBlueprint":
        PROJECT = "FBP"
    elif args.future == "TransitRecovery":
        PROJECT = "TRR"

    if args.input_projects:
        NETWORK_BASE_DIR = args.input_projects
    else:
        NETWORK_BASE_DIR = r"M:\\Application\\Model One\\NetworkProjects"

    HWY_NET_NAME = "freeflow.net"
    TRN_NET_NAME = "transitLines"

    if args.future == "all":
        FUTURES = ["CleanAndGreen", "RisingTides", "BackToTheFuture"]
    else:
        FUTURES = [args.future]

    for SCENARIO in FUTURES:
        NOW = time.strftime("%Y%b%d.%H%M%S")
        if args.input_network:
            print("Using input network {}".format(args.input_network))
            BASE_DIR = args.input_network
            PIVOT_DIR = args.input_network
        else:
            BASE_DIR = findBaseDirectory(SCENARIO)  # e.g. 2050_TM150_PPA_BF_00
            PIVOT_DIR = os.path.join(
                PPA_DIR, BASE_DIR, "INPUT"
            )  # full path of input network
        TRANSIT_CAPACITY_DIR = os.path.join(PIVOT_DIR, "trn")

        # setup kwargs to pass
        kwargs = {}
        if args.kwarg:
            # assume "all" is special as a kwarg value and should be replaced with the SCENARIO
            if args.kwarg[1] == "all":
                kwargs[args.kwarg[0]] = '"{}"'.format(SCENARIO)
            else:
                kwargs[args.kwarg[0]] = '"{}"'.format(args.kwarg[1])
        # second optional kwarg
        if args.kwarg2:
            kwargs[args.kwarg2[0]] = '"{}"'.format(args.kwarg2[1])

        if args.output_network:
            print("Using output network {}".format(args.output_network))
            OUTPUT_DIR = args.output_network
            # make OUTPUT_DIR
            if not os.path.exists(OUTPUT_DIR):
                os.mkdir(OUTPUT_DIR)
            OUTPUT_FUTURE_DIR = OUTPUT_DIR
            # move into it so the scratch is here
            os.chdir(OUTPUT_DIR)

        else:
            OUTPUT_DIR = os.path.join(PPA_DIR, args.project_short_id)
            # make OUTPUT_DIR
            if not os.path.exists(OUTPUT_DIR):
                os.mkdir(OUTPUT_DIR)

            OUTPUT_FUTURE_DIR = determineProjectDirectory(
                OUTPUT_DIR, BASE_DIR, args.project_short_id
            )
            os.mkdir(OUTPUT_FUTURE_DIR)
            # move into it so the scratch is here
            os.chdir(OUTPUT_DIR)

        # put log file into the run dir
        LOG_FILENAME = "addproject_{}_{}_{}_{}.info.LOG".format(
            PROJECT, SCENARIO, args.project_short_id, NOW
        )
        Wrangler.setupLogging(
            os.path.join(OUTPUT_FUTURE_DIR, LOG_FILENAME),
            os.path.join(OUTPUT_FUTURE_DIR, LOG_FILENAME.replace("info", "debug")),
        )

        Wrangler.WranglerLogger.info("Input args: {}".format(args))
        Wrangler.WranglerLogger.info("Using base directory {}".format(PIVOT_DIR))

        # Create a scratch directory to check out project repos into
        SCRATCH_SUBDIR = "scratch"
        TEMP_SUBDIR = "Wrangler_tmp_" + NOW
        if not os.path.exists(SCRATCH_SUBDIR):
            os.mkdir(SCRATCH_SUBDIR)
        os.chdir(SCRATCH_SUBDIR)

        networks = {
            "hwy": Wrangler.HighwayNetwork(
                modelType=Wrangler.Network.MODEL_TYPE_TM1,
                modelVersion=1.0,
                basenetworkpath=os.path.join(PIVOT_DIR, "hwy"),
                networkBaseDir=NETWORK_BASE_DIR,
                networkProjectSubdir=None,
                networkSeedSubdir=None,
                networkPlanSubdir=None,
                isTiered=True,
                tag=None,
                tempdir=TEMP_SUBDIR,
                networkName="hwy",
                tierNetworkName=HWY_NET_NAME,
            ),
            "trn": Wrangler.TransitNetwork(
                modelType=Wrangler.Network.MODEL_TYPE_TM1,
                modelVersion=1.0,
                basenetworkpath=os.path.join(PIVOT_DIR, "trn"),
                networkBaseDir=NETWORK_BASE_DIR,
                networkProjectSubdir=None,
                networkSeedSubdir=None,
                networkPlanSubdir=None,
                isTiered=True,
                networkName=TRN_NET_NAME,
            ),
        }
        if TRANSIT_CAPACITY_DIR:
            Wrangler.TransitNetwork.capacity = Wrangler.TransitCapacity(
                directory=TRANSIT_CAPACITY_DIR
            )

        for netmode in ["hwy", "trn"]:
            # if applying project
            if (netmode == "hwy" and args.hwy) or (netmode == "trn" and args.trn):

                # iterate through projects specified, since args.project is a list
                for my_project in args.project:

                    Wrangler.WranglerLogger.info(
                        "Applying project [%s] of type [%s]" % (my_project, netmode)
                    )
                    cloned_SHA1 = networks[netmode].cloneProject(
                        networkdir=my_project,
                        tag=args.tag,
                        projtype="project",
                        tempdir=TEMP_SUBDIR,
                        **kwargs
                    )
                    (parentdir, networkdir, gitdir, projectsubdir) = networks[
                        netmode
                    ].getClonedProjectArgs(my_project, None, "project", TEMP_SUBDIR)

                    applied_SHA1 = networks[netmode].applyProject(
                        parentdir, networkdir, gitdir, projectsubdir, **kwargs
                    )

            # write networks
            final_path = os.path.join(OUTPUT_FUTURE_DIR, netmode)
            if not os.path.exists(final_path):
                os.makedirs(final_path)

            if netmode == "hwy":

                # create the subdir for SET_CAPCLASS with set_capclass.job as apply.s
                SET_CAPCLASS = "set_capclass"
                SET_CAPCLASS_DIR = os.path.join(TEMP_SUBDIR, SET_CAPCLASS)
                if not os.path.isdir(SET_CAPCLASS_DIR):
                    os.makedirs(SET_CAPCLASS_DIR)
                source_file = os.path.join(
                    os.path.dirname(THIS_FILE), "set_capclass.job"
                )
                shutil.copyfile(source_file, os.path.join(SET_CAPCLASS_DIR, "apply.s"))

                # if hwy project has set_capclass override, copy it to set_capclass/apply.s
                for my_project in args.project:
                    set_capclass_override = os.path.join(
                        TEMP_SUBDIR, my_project, "set_capclass.job"
                    )
                    if os.path.exists(set_capclass_override):
                        dest_file = os.path.join(SET_CAPCLASS_DIR, "apply.s")
                        shutil.copyfile(set_capclass_override, dest_file)
                        Wrangler.WranglerLogger.info(
                            "Copied override {} to {}".format(
                                set_capclass_override, dest_file
                            )
                        )

                # apply set_capclass before writing any hwy network
                try:
                    applied_SHA1 = networks[netmode].applyProject(
                        parentdir=TEMP_SUBDIR,
                        networkdir=SET_CAPCLASS,
                        gitdir=os.path.join(TEMP_SUBDIR, SET_CAPCLASS),
                    )
                except Wrangler.NetworkException as ne:
                    Wrangler.WranglerLogger.debug(
                        "set_capclass exception: {}".format(ne.args[0])
                    )
                    # this is expected -- since we're using a hack and this isn't a git project
                    if ne.args[0].startswith("Git log failed"):
                        pass
                    else:
                        raise ne

                # create the subdir for ERROR_CHECK with check_for_errors.job as apply.s
                ERROR_CHECK = "check_for_errors"
                ERROR_CHECK_DIR = os.path.join(TEMP_SUBDIR, ERROR_CHECK)
                if not os.path.isdir(ERROR_CHECK_DIR):
                    os.makedirs(ERROR_CHECK_DIR)
                source_file = os.path.join(
                    os.path.dirname(THIS_FILE), "check_for_errors.job"
                )
                shutil.copyfile(source_file, os.path.join(ERROR_CHECK_DIR, "apply.s"))

                # apply check_for_errors before writing any hwy network
                try:
                    applied_SHA1 = networks[netmode].applyProject(
                        parentdir=TEMP_SUBDIR,
                        networkdir=ERROR_CHECK,
                        gitdir=os.path.join(TEMP_SUBDIR, ERROR_CHECK),
                    )
                except Wrangler.NetworkException as ne:
                    Wrangler.WranglerLogger.debug(
                        "check_for_errors exception: {}".format(ne.args[0])
                    )
                    # this is expected -- since we're using a hack and this isn't a git project
                    if ne.args[0].startswith("Git log failed"):
                        pass
                    else:
                        raise ne

                networks["hwy"].write(
                    path=final_path,
                    name=HWY_NET_NAME,
                    suppressQuery=True,
                    suppressValidation=True,
                )  # MTC doesn't have turn penalties
            else:
                networks["trn"].write(
                    path=final_path,
                    name=TRN_NET_NAME,
                    writeEmptyFiles=False,
                    suppressQuery=False,
                    suppressValidation=False,
                    cubeNetFileForValidation=os.path.join(
                        os.path.abspath(OUTPUT_FUTURE_DIR), "hwy", HWY_NET_NAME
                    ),
                )
                # Write the transit capacity configuration
                Wrangler.TransitNetwork.capacity.writeTransitVehicleToCapacity(
                    directory=final_path
                )
                Wrangler.TransitNetwork.capacity.writeTransitLineToVehicle(
                    directory=final_path
                )
                Wrangler.TransitNetwork.capacity.writeTransitPrefixToVehicle(
                    directory=final_path
                )

        Wrangler.WranglerLogger.debug(
            "Successfully completed running %s" % os.path.abspath(__file__)
        )
