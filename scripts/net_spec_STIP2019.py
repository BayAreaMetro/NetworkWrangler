import os

# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT = "STIP 2019"

# MANDATORY. Set this to be the Scenario Name
# e.g. "Base", "Baseline"
SCENARIO = "Baseline"

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "HEAD"

# MANDATORY. Set this to the directory in which to write your outputs.
# "hwy" and "trn" subdirectories will be created here.
OUT_DIR = SCENARIO + "_network_{}"  # YEAR

# MANDATORY.  Should be a dictionary with keys "hwy", "muni", "rail", "bus"
# to a list of projects.  A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}
NETWORK_PROJECTS = collections.OrderedDict(
    [
        (
            2015,
            {
                "hwy": [
                    "PROJ_attributes",  # adds PROJ attributes to NODE and LINK
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2015"},
                    },
                ],
                "trn": [],
            },
        ),
        (
            2020,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2020"},
                    },
                    {"name": "EXP_237B", "kwargs": {"FUTURE": SCENARIO}},
                    "EXP_580C",
                    "EXP_680D",
                    "EXP_680F",
                    "SCL130001_237_101_MAT_Int_Mod",
                    "REG090003_SCLARA_FIP",
                    "ALA130005_Dougherty_road_widening",
                    "ALA130006_Dublin_Blvd_widening",
                    "ALA130014_7th_St_road_diet",
                    "ALA150004_EastBay_BRT",
                    "CC_130046_I680_SR4_Int_Rec",
                    "CC_070035_I80_SPDamRd_Int_Phase1",
                    "CC_070011_Brentwood_Blvd_Widening",
                    "CC_070075_Kirker_Pass_Truck_Lane",
                    "CC_090019_Bollinger_Canyon_Widening",
                    "CC_130006_Concord_BART_road_diets",
                    "CC_170001_SanRamonValleyBlvd_Lane_Addition",
                    "CC_170061_Bus_On_Shoulder_680BRT",
                    "MRN150009_San_Rafael_Bridge_Improvements",
                    "SF_070027_Yerba_Buena_Ramp_Imp",
                    "SF_070005_VanNess_BRT",
                    "SF_130011_2ndSt_Road_Diet",
                    "SM_110047_SR92_ElCam_Ramp_Mod",
                    "SOL110005_Jepson_Van_to_Com",
                    "SON070004_101_MarinSonNarrows_Phase1",
                    "ALA050014_SR84_Widening",
                    "ALA170011_BayBridge_HOV_Connectors",
                    "ALA150047_TelegraphAve_Complete_Streets",
                    "SCL190002_280_Foothill_improvement",
                    "I80_AdaptiveRampMetering",
                    "VAR170021_Freeway_Performance_I880",
                    "SonomaCounty_Transit_NoBuild2050",
                    "SF_MuniForward_Committed",
                ],
                "trn": [
                    "ALA050015_BART_to_WarmSprings",
                    "ACGo",
                    "CC_050025_EBart_to_Antioch",
                    "SCL110005_BART_to_Berryessa",
                    "SF_010015_Transbay_Terminal",
                    "SF_010037_Muni_Central_Subway",
                    "SF_070027_Yerba_Buena_Ramp_Imp",
                    "SOL030002_FairfieldVacaville_Stn",
                    "SON090002_SMART",
                    "SON090002_SMART_to_Larkspur",
                    "CC_070062_Richmond_Ferry",
                    "SF_MuniForward_Committed",
                    "VTA_Next",
                    "SCL130001_237_101_MAT_Int_Mod",
                    "SonomaCounty_Transit_NoBuild2050",
                    "SMART_Novato",
                    "Xfare_update_2020",
                    "ACTransit_Committed",
                    "ferry_update_2019",
                    "SamTrans_ECR_Rapid",
                ],
            },
        ),
        (
            2025,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2025"},
                    },
                    "EXP_CC_050028_I680_SB_HOV_Completion",
                    "EXP_101B1",
                    "EXP_101B2",
                    "EXP_101C",
                ],
                "trn": [
                    "SF_010028_Caltrain_Modernization",
                    "REG090037_New_BART_Trains",
                ],
            },
        ),
        (
            2030,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2030"},
                    }
                ],
                "trn": [],
            },
        ),
        (
            2035,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2035"},
                    }
                ],
                "trn": [],
            },
        ),
        # every project in the STIP 2040 baseline are loaded on or before 2035
        (
            2040,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2040"},
                    },
                    "EXP_STIP_NoProject",
                ],  # this is not a real project - it sets the toll rates for express lanes
                "trn": ["Move_buses_to_HOV_EXP_lanes"],
            },
        ),
        # note that this is not really the 2045 network, it's really the STIP project set to build the STIP 2040 with Project
        (
            2045,
            {
                "hwy": [
                    "SOL110006_Jepson_1B_1C",
                    "STIP_US101_Managed_Lanes_I80_Solano",
                    "STIP_US101_Managed_Lanes_NI380",
                    "STIP_US101_ManagedLanes_Whipple_I380",
                    "STIP_US101_ExpLanes_Phase5",
                    "MAJ_SR4_Operational_Improvements",
                    "STIP_17_06_0010_WoodsideRd",
                    "STIP_ProduceAve",
                    "STIP_ITS_SoSF",
                    "STIP_ITS_SM",
                    "STIP_FairgroundsDr",
                    "EXP_STIP_Project",
                ],  # this project is not a real project - it sets the toll rates for express lanes
                "trn": ["MAJ_BRT030001_BART_to_SanJose", "Move_buses_to_HOV_EXP_lanes"],
            },
        ),
    ]
)

# OPTIONAL. The default route network project directory is Y:\networks.  If
# projects are stored in another directory, then use this variable to specify it.
# For example: Y:\networks\projects
# NETWORK_BASE_DIR = None
# NETWORK_PROJECT_SUBDIR = None
# NETWORK_SEED_SUBDIR = None
# NETWORK_PLAN_SUBDIR = None

# OPTIONAL. A list of project names which have been previously applied in the
# PIVOT_DIR network that projects in this project might rely on.  For example
# if DoyleDrive exists, then Muni_TEP gets applied differently so transit lines
# run on the new Doyle Drive alignment
APPLIED_PROJECTS = None

# OPTIONAL.  A list of project names.  For test mode, these projects won't use
# the TAG.  This is meant for developing a network project.
TEST_PROJECTS = []
