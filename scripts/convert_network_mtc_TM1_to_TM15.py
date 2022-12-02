import argparse, collections, datetime, os, pandas, shutil, sys, time
import Wrangler

USAGE = """

  Converts a TM1.0 network (pre MTC use of NetworkWrangler) to a TM1.5 network (post MTC use of NetworkWrangler)

  e.g. python convert_network_mtc_TM1_to_TM15.py "M:\Application\Model One\RTP2017\Scenarios\2005_05_003\INPUT_fullcopy" net_2005_05_003_TM151

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "INPUT_dir", help="Input directory containing hwy and trn files"
    )
    parser.add_argument(
        "OUTPUT_dir", help="Output directory containing hwy and trn files"
    )
    args = parser.parse_args()

    NOW = time.strftime("%Y%b%d.%H%M%S")
    THIS_FILE = os.path.realpath(__file__)

    NETWORK_BASE_DIR = r"M:\\Application\\Model One\\NetworkProjects"
    TRN_SUBDIR = "trn"
    TRN_NET_NAME = "Transit_Lines"
    HWY_SUBDIR = "hwy"
    HWY_NET_NAME = "freeflow.net"
    TRANSIT_CAPACITY_DIR = None  # doesn't exist in TM1

    LOG_FILENAME = "convert_network_TM1to15_{}_{}.info.LOG".format(args.OUTPUT_dir, NOW)
    Wrangler.setupLogging(LOG_FILENAME, LOG_FILENAME.replace("info", "debug"))
    if TRANSIT_CAPACITY_DIR:
        Wrangler.TransitNetwork.capacity = Wrangler.TransitCapacity(
            directory=TRANSIT_CAPACITY_DIR
        )

    # Create a scratch directory to check out project repos into
    SCRATCH_SUBDIR = "scratch"
    TEMP_SUBDIR = "Wrangler_tmp_" + NOW
    if not os.path.exists(SCRATCH_SUBDIR):
        os.mkdir(SCRATCH_SUBDIR)
    os.chdir(SCRATCH_SUBDIR)
    if not os.path.exists(TEMP_SUBDIR):
        os.mkdir(TEMP_SUBDIR)

    networks = {}
    try:
        networks["hwy"] = Wrangler.HighwayNetwork(
            modelType=Wrangler.Network.MODEL_TYPE_TM1,
            modelVersion=1.0,
            basenetworkpath=os.path.join(args.INPUT_dir, "hwy"),
            networkBaseDir=NETWORK_BASE_DIR,
            networkProjectSubdir=None,
            networkSeedSubdir=None,
            networkPlanSubdir=None,
            isTiered=True,
            tag=None,
            tempdir=TEMP_SUBDIR,
            networkName="hwy",
            tierNetworkName=HWY_NET_NAME,
        )
        networks["trn"] = Wrangler.TransitNetwork(
            modelType=Wrangler.Network.MODEL_TYPE_TM1,
            modelVersion=1.0,
            basenetworkpath=os.path.join(args.INPUT_dir, "trn"),
            networkBaseDir=NETWORK_BASE_DIR,
            networkProjectSubdir=None,
            networkSeedSubdir=None,
            networkPlanSubdir=None,
            isTiered=True,
            networkName=TRN_NET_NAME,
        )
    except Wrangler.NetworkException as e:
        Wrangler.WranglerLogger.fatal(e)
        sys.exit()

    # create the subdir for SET_CAPCLASS with set_capclass.job as apply.s
    SET_CAPCLASS = "set_capclass"
    SET_CAPCLASS_DIR = os.path.join(TEMP_SUBDIR, SET_CAPCLASS)
    os.mkdir(SET_CAPCLASS_DIR)
    source_file = os.path.join(os.path.dirname(THIS_FILE), "set_capclass.job")
    shutil.copyfile(source_file, os.path.join(SET_CAPCLASS_DIR, "apply.s"))

    # apply set_capclass before writing any hwy network
    applied_SHA1 = networks["hwy"].applyProject(
        parentdir=TEMP_SUBDIR,
        networkdir=SET_CAPCLASS,
        gitdir=os.path.join(TEMP_SUBDIR, SET_CAPCLASS),
    )

    # Initialize output subdirectories up a level (not in scratch)
    hwypath = os.path.join("..", args.OUTPUT_dir, HWY_SUBDIR)
    if not os.path.exists(hwypath):
        os.makedirs(hwypath)
    trnpath = os.path.join("..", args.OUTPUT_dir, TRN_SUBDIR)
    if not os.path.exists(trnpath):
        os.makedirs(trnpath)

    networks["hwy"].write(
        path=hwypath, name=HWY_NET_NAME, suppressQuery=True, suppressValidation=True
    )  # MTC TM1 doesn't have turn penalties

    os.environ[
        "CHAMP_node_names"
    ] = r"M:\\Application\\Model One\\Networks\\TM1_2015_Base_Network\\Node Description.xls"
    hwy_abs_path = os.path.abspath(os.path.join(hwypath, HWY_NET_NAME))
    try:
        networks["trn"].write(
            path=trnpath,
            name="transitLines",
            writeEmptyFiles=False,
            suppressQuery=True,
            suppressValidation=False,
            cubeNetFileForValidation=hwy_abs_path,
        )
    except Exception as e:
        Wrangler.WranglerLogger.warn(
            "Transit network validation failed, writing anyway"
        )
        networks["trn"].write(
            path=trnpath,
            name="transitLines",
            writeEmptyFiles=False,
            suppressQuery=True,
            suppressValidation=True,
            cubeNetFileForValidation=hwy_abs_path,
        )

    # Write the transit capacity configuration
    # create default capacity configuration?
    # Wrangler.TransitNetwork.capacity.writeTransitVehicleToCapacity(directory = trnpath)
    # Wrangler.TransitNetwork.capacity.writeTransitLineToVehicle(directory = trnpath)
    # Wrangler.TransitNetwork.capacity.writeTransitPrefixToVehicle(directory = trnpath)

    Wrangler.WranglerLogger.debug(
        "Successfully completed running %s" % os.path.abspath(__file__)
    )
