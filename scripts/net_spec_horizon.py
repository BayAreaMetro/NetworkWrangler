import os

# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
# PROJECT = "FU1" or "PPA", set by build_network_mtc_futures.py based on argument
# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "HEAD"
# MANDATORY. Set this to the directory in which to write your outputs.
# "hwy" and "trn" subdirectories will be created here.
OUT_DIR = "network_{}"  # YEAR
# MANDATORY.  Should be a dictionary with keys "hwy", "trn"
# to a list of projects.  A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}

###########################################################
# For Round 1 and Project Performance Assessment Base both
COMMITTED_PROJECTS = collections.OrderedDict(
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
                    "ALA130026_Shattuck_Complete_Streets",
                    "ALA170049_Central_AVE_Safety_Improvements",
                    "ALA170052_Fruitvale_Ave_ped_improvements",
                    "ALA150004_EastBay_BRT",
                    "CC_130001_BaileyRd_SR4",
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
                    "SM_110047_SR92_ElCam_Ramp_Mod",
                    "SCL190002_280_Foothill_improvement",
                    "SCL190006_101SB_offramp_improvement",
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
                    "EXP_680C1",
                    "EXP_85C",
                    "EXP_101C",
                    "ALA150001_I680_SR84_Int_Wid",
                    "ALA150043_Claremont_road_diet",
                    "CC_070009_Slatten_Ranch_Rd_Extension",
                    "SF_070004_Geary_BRT_Phase1",
                    "SON070004_101_MarinSonNarrows_Phase2",
                    "SOL110006_Jepson_1B_1C",
                    "SCL190008_US101_DLC_Int_Imp",
                    "I880_US101_AdaptiveRampMetering",
                    "MAJ_SCL050009_VTA_Eastridge_Extension",
                    "SOL070020_I80_I680_SR12_Int_1_2A",
                ],
                "trn": [
                    "SF_010028_Caltrain_Modernization",
                    "SON090002_SMART_to_Windsor",
                    "MAJ_SCL050009_VTA_Eastridge_Extension",
                    "REG090037_New_BART_Trains",
                    "SOL070020_I80_I680_SR12_Int_1_2A",
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
                    },
                    "EXP_880A",
                ],
                "trn": ["BART_NoProject"],
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
        (
            2040,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2040"},
                    }
                ],
                "trn": [],
            },
        ),
        (
            2045,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2045"},
                    }
                ],
                "trn": [],
            },
        ),
        (
            2050,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_2_2pct",
                        "kwargs": {"MODELYEAR": "2050"},
                    }
                ],
                "trn": [],
            },
        ),
    ]
)

###########################################################
# Round1 and Round2 Major Projects
MAJOR_PROJECTS = collections.OrderedDict(
    [
        (
            2015,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2015"},
                    }
                ],
                "trn": [],
            },
        ),
        (
            2020,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2020"},
                    }
                ],
                "trn": ["MAJ_Sonoma_Frequency_Increase"],
            },
        ),
        (
            2025,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2025"},
                    },
                    "MAJ_Geary_BRT_Phase2",
                    "MAJ_SF_Congestion_Pricing",
                    "MAJ_SOL070020_I80_I680_SR12_Int_2B_7",
                    "MAJ_Bay_Area_Forward_committed",
                ],
                "trn": [
                    "MAJ_Geary_BRT_Phase2",
                    "MAJ_SOL070020_I80_I680_SR12_Int_2B_7",
                    "MAJ_SF_Congestion_Pricing",
                ],
            },
        ),
        (
            2030,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2030"},
                    },
                    "MAJ_SanPablo_BRT",
                    "MAJ_ElCaminoReal_BRT",
                    "MAJ_I680_SR4_Int_Widening_Phases_3_5",
                    "MAJ_SR4_Operational_Improvements",
                    "MAJ_Better_Market_St",
                ],
                "trn": [
                    "MAJ_BRT030001_BART_to_SanJose",
                    "MAJ_SF_050002_Caltrain_Ext_TransbayTerminal",
                    "MAJ_WETA_Service_Frequency_Increase",
                    "MAJ_Alameda_Point_SF_Ferry",
                    "MAJ_MissionBay_SF_Ferry",
                    "MAJ_RedwoodCity_SF_Ferry",
                    "MAJ_MTC050027_Berkeley_Ferry",
                    "MAJ_Better_Market_St",
                    "MAJ_REG090037_BART_Core_Cap",
                ],
            },
        ),
        (
            2035,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2035"},
                    },
                    "MAJ_Treasure_Island_Congestion_Pricing",
                ],
                "trn": [
                    "MAJ_MuniForward_Uncommitted",
                    "MAJ_Vasona_LRT_Extension",
                    "MAJ_Treasure_Island_Congestion_Pricing",
                ],
            },
        ),
        (
            2040,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2040"},
                    }
                ],
                "trn": [],
            },
        ),
        (
            2045,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2045"},
                    }
                ],
                "trn": [],
            },
        ),
        (
            2050,
            {
                "hwy": [
                    {
                        "name": "Bridge_Toll_Updates_3pct",
                        "kwargs": {"MODELYEAR": "2050"},
                    }
                ],
                "trn": [],
            },
        ),
    ]
)

###########################################################
# Round2 Transformative Projects -- Note that some are not included in Rising Tides, Falling Fortunes
# RAWG June 2019 Agenda Item 3: Horizon - Futures Round 2: Final Strategies for Round 2 Analysis
# https://mtc.legistar.com/View.ashx?M=F&ID=7281685&GUID=82EACC9C-82E9-4895-85CF-29F8C3CD9EF0
TRANSFORM_PROJECTS = collections.OrderedDict(
    [
        (
            2015,
            {  # all futures
                "hwy_all": [],
                "trn_all": [],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": [],
                "trn_cgbf": [],
            },
        ),
        (
            2020,
            {  # all futures
                "hwy_all": [],
                "trn_all": [],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": [],
                "trn_cgbf": [],
            },
        ),
        (
            2025,
            {  # all futures
                "hwy_all": [
                    {"name": "EXP_uncommitted_all", "kwargs": {"FUTURE": SCENARIO}},
                    "Futures_H10_Vision_Zero",
                ],
                "trn_all": [
                    {
                        "name": "EXP_uncommitted_all",
                        "kwargs": {"FUTURE": '"{}"'.format(SCENARIO)},
                    },  # pass as quoted string
                    "Futures_H10_Vision_Zero",
                ],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": ["Transform_Valley_Link"],
                "trn_cgbf": ["Transform_Valley_Link"],
            },
        ),
        (
            2030,
            {  # all futures
                "hwy_all": ["EXP_gapclosure", "Futures_C4_ReX_Express"],
                "trn_all": ["EXP_gapclosure", "Futures_C4_ReX_Express"],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": ["Transform_Dumbarton_Rail"],
                "trn_cgbf": [
                    "MAJ_SanJose_LRT_Subway",
                    "Transform_Muni_Southwest_Subway",
                    "MAJ_EBart_Extension_Brentwood",
                    "Futures_SMART_to_Healdsburg",
                    "Transform_Dumbarton_Rail",
                ],
            },
        ),
        (
            2035,
            {  # all futures
                "hwy_all": [],
                "trn_all": [],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": [],
                "trn_cgbf": [],
            },
        ),
        (
            2040,
            {  # all futures
                "hwy_all": [],
                "trn_all": [],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": [
                    "Transform_Richmond_Bridge_Replacement",
                    "Transform_SMART_To_Richmond",
                ],
                "trn_cgbf": [
                    "Transform_VTA_NorthSJ_Subway",
                    "Transform_SMART_To_Richmond",
                    "Transform_VTA_LRT_FullGradeSep",
                ],
            },
        ),
        (
            2045,
            {  # all futures
                "hwy_all": [],
                "trn_all": [],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": [],
                "trn_cgbf": ["Transform_VTA_LRT_Automation"],
            },
        ),
        (
            2050,
            {  # all futures
                "hwy_all": ["Futures_PBA5_HOT_to_HOV3", "Futures_C6_Tolls_on_Freeways"],
                "trn_all": ["Futures_PBA5_HOT_to_HOV3", "Futures_C6_Tolls_on_Freeways"],
                # CleanAndGreen, BackToTheFuture only
                "hwy_cgbf": ["Crossings3"],
                "trn_cgbf": ["Crossings3"],
            },
        ),
    ]
)

# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS = collections.OrderedDict()
for YEAR in COMMITTED_PROJECTS.keys():
    # Future Round1 includes major projects
    if PROJECT == "FU1":
        NETWORK_PROJECTS[YEAR] = {
            "hwy": COMMITTED_PROJECTS[YEAR]["hwy"] + MAJOR_PROJECTS[YEAR]["hwy"],
            "trn": COMMITTED_PROJECTS[YEAR]["trn"] + MAJOR_PROJECTS[YEAR]["trn"],
        }
    elif PROJECT == "FU2":
        # only use those marked hwy_all, trn_all
        if SCENARIO == "RisingTides":
            NETWORK_PROJECTS[YEAR] = {
                "hwy": COMMITTED_PROJECTS[YEAR]["hwy"]
                + MAJOR_PROJECTS[YEAR]["hwy"]
                + TRANSFORM_PROJECTS[YEAR]["hwy_all"],
                "trn": COMMITTED_PROJECTS[YEAR]["trn"]
                + MAJOR_PROJECTS[YEAR]["trn"]
                + TRANSFORM_PROJECTS[YEAR]["trn_all"],
            }
        elif SCENARIO in ["CleanAndGreen", "BackToTheFuture"]:
            NETWORK_PROJECTS[YEAR] = {
                "hwy": COMMITTED_PROJECTS[YEAR]["hwy"]
                + MAJOR_PROJECTS[YEAR]["hwy"]
                + TRANSFORM_PROJECTS[YEAR]["hwy_all"]
                + TRANSFORM_PROJECTS[YEAR]["hwy_cgbf"],
                "trn": COMMITTED_PROJECTS[YEAR]["trn"]
                + MAJOR_PROJECTS[YEAR]["trn"]
                + TRANSFORM_PROJECTS[YEAR]["trn_all"]
                + TRANSFORM_PROJECTS[YEAR]["trn_cgbf"],
            }
    elif PROJECT in ["PPA", "PPA_NoSLR"]:
        # Project Performance Assessment baseline does not include major projects
        NETWORK_PROJECTS[YEAR] = {
            "hwy": COMMITTED_PROJECTS[YEAR]["hwy"],
            "trn": COMMITTED_PROJECTS[YEAR]["trn"],
        }

# done at the end in case they need to remove transit project links
# remove "False and" clauses when these are coded
if SCENARIO == "CleanAndGreen":
    if PROJECT == "FU1":
        # High Speed Rail is only included in Round1, not Project Performance Baseline nor Round2
        NETWORK_PROJECTS[2030]["trn"].append("HSR")

    elif PROJECT == "FU2":
        # this needs to be added before Earthquake or it's lost
        NETWORK_PROJECTS[2035]["trn"].append("Caltrain_PCBB10_HSR")

    # NOTE: Earthquake is assumed in Round1 2035 but since the effect doesn't stay; this is handled in build_network_mtc_futures.py
    if PROJECT in ["FU1", "FU2"]:
        # Haywired Earthquake in 2035
        NETWORK_PROJECTS[2035]["hwy"].append("Earthquake")
        NETWORK_PROJECTS[2035]["trn"].append("Earthquake")

    # Sea Level Rise in FU1 and PPA (but not PPA_NoSLR)
    if PROJECT in ["FU1", "PPA"]:
        # Sea Level Rise in 2045
        NETWORK_PROJECTS[2045]["hwy"].append("SeaLevelRise_1foot")
        NETWORK_PROJECTS[2045]["trn"].append("SeaLevelRise_1foot")
    # But we've adapted in FU2 (also add caltrain PCBB project without HSR)
    elif PROJECT == "FU2":
        NETWORK_PROJECTS[2045]["hwy"].append("SeaLevelRise_HighAdaptation")
        NETWORK_PROJECTS[2045]["trn"].append("SeaLevelRise_HighAdaptation")

elif SCENARIO == "RisingTides":

    # Sea Level Rise in FU1 and PPA (but not PPA_NoSLR)
    if PROJECT in ["FU1", "PPA"]:
        # Sea Level Rise in 2030
        NETWORK_PROJECTS[2030]["hwy"].append("SeaLevelRise_1foot")
        NETWORK_PROJECTS[2030]["trn"].append("SeaLevelRise_1foot")
    # But we've adapted in FU2
    elif PROJECT == "FU2":
        NETWORK_PROJECTS[2030]["hwy"].append("SeaLevelRise_LowAdaptation")
        NETWORK_PROJECTS[2030]["trn"].append("SeaLevelRise_LowAdaptation")

        NETWORK_PROJECTS[2030]["hwy"].append("SeaLevelRise_HighAdaptation")
        NETWORK_PROJECTS[2030]["trn"].append("SeaLevelRise_HighAdaptation")

    if PROJECT in ["FU1", "FU2"]:
        # Haywired Earthquake in 2035
        NETWORK_PROJECTS[2035]["hwy"].append("Earthquake")
        NETWORK_PROJECTS[2035]["trn"].append("Earthquake")

    # Sea Level Rise in FU1 and PPA (but not PPA_NoSLR)
    if PROJECT in ["FU1", "PPA"]:
        # Sea Level Rise in 2040
        NETWORK_PROJECTS[2040]["hwy"].append("SeaLevelRise_2feet")
        NETWORK_PROJECTS[2040]["trn"].append("SeaLevelRise_2feet")
        # Sea Level Rise in 2050
        NETWORK_PROJECTS[2050]["hwy"].append("SeaLevelRise_3feet")
        NETWORK_PROJECTS[2050]["trn"].append("SeaLevelRise_3feet")
    # In FU2, adaptation still holds but no need to reapply
    elif PROJECT == "FU2":
        pass

elif SCENARIO == "BackToTheFuture":
    # Sea Level Rise in FU1 and PPA (but not PPA_NoSLR)
    if PROJECT in ["FU1", "PPA"]:
        NETWORK_PROJECTS[2035]["hwy"].append("SeaLevelRise_1foot")
        NETWORK_PROJECTS[2035]["trn"].append("SeaLevelRise_1foot")
    # But we've adapted in FU2 (also add caltrain PCBB without HSR)
    elif PROJECT == "FU2":
        NETWORK_PROJECTS[2035]["hwy"].append("SeaLevelRise_HighAdaptation")
        NETWORK_PROJECTS[2035]["trn"].append("SeaLevelRise_HighAdaptation")
        NETWORK_PROJECTS[2035]["trn"].append("Caltrain_PCBB10_NoHSR")

    # NOTE: Earthquake is assumed in Round1 2035 but since the effect doesn't stay; this is handled in build_network_mtc_futures.py
    if PROJECT in ["FU1", "FU2"]:
        # Haywired Earthquake in 2035
        NETWORK_PROJECTS[2035]["hwy"].append("Earthquake")
        NETWORK_PROJECTS[2035]["trn"].append("Earthquake")

    # Sea Level Rise in FU1 and PPA (but not PPA_NoSLR)
    if PROJECT in ["FU1", "PPA"]:
        NETWORK_PROJECTS[2050]["hwy"].append("SeaLevelRise_2feet")
        NETWORK_PROJECTS[2050]["trn"].append("SeaLevelRise_2feet")
    # In FU2, adaptation still holds but no need to reapply
    elif PROJECT == "FU2":
        pass

#
# For every year where a project is applied do the following:
# Convert all zero-length links to 0.01
# Move buses to HOV/Express lanes at the end
#
for YEAR in NETWORK_PROJECTS.keys():
    # if anything is applied
    if (len(NETWORK_PROJECTS[YEAR]["hwy"]) > 0) or (
        len(NETWORK_PROJECTS[YEAR]["trn"]) > 0
    ):
        NETWORK_PROJECTS[YEAR]["hwy"].append("No_zero_length_links")

    if (len(NETWORK_PROJECTS[YEAR]["hwy"]) > 0) or (
        len(NETWORK_PROJECTS[YEAR]["trn"]) > 0
    ):
        NETWORK_PROJECTS[YEAR]["trn"].append("Move_buses_to_HOV_EXP_lanes")


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
