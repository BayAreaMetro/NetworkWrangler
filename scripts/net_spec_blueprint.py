import os
# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT  = "PBA50"
SCENARIO = "Blueprint Basic"

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "HEAD"
# MANDATORY. Set this to the directory in which to write your outputs.
# "hwy" and "trn" subdirectories will be created here.
OUT_DIR = SCENARIO + " network_{}"   # YEAR
# MANDATORY.  Should be a dictionary with keys "hwy", "trn"
# to a list of projects.  A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}

###########################################################
COMMITTED_PROJECTS = collections.OrderedDict([
    (2015, {
        'hwy':['PROJ_attributes',  # adds PROJ attributes to NODE and LINK
               {'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2015'}}],
        'trn':[]
    }),
    (2020, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2020'}},
               {'name':'EXP_237B',                   'kwargs':{'FUTURE':SCENARIO}},
               'EXP_580C',
               'EXP_680D',
               'EXP_680F',
               'SCL130001_237_101_MAT_Int_Mod',
               'REG090003_SCLARA_FIP',
               'ALA130005_Dougherty_road_widening',
               'ALA130006_Dublin_Blvd_widening',
               'ALA130014_7th_St_road_diet',
               'ALA130026_Shattuck_Complete_Streets',
               'ALA170049_Central_AVE_Safety_Improvements',
               'ALA170052_Fruitvale_Ave_ped_improvements',
               'ALA150004_EastBay_BRT',
               'CC_130001_BaileyRd_SR4',
               'CC_130046_I680_SR4_Int_Rec',
               'CC_070035_I80_SPDamRd_Int_Phase1',
               'CC_070011_Brentwood_Blvd_Widening',
               'CC_070075_Kirker_Pass_Truck_Lane',
               'CC_090019_Bollinger_Canyon_Widening',
               'CC_130006_Concord_BART_road_diets',
               'CC_170001_SanRamonValleyBlvd_Lane_Addition',
               'CC_170061_Bus_On_Shoulder_680BRT',
               'MRN150009_San_Rafael_Bridge_Improvements',
               'SF_070027_Yerba_Buena_Ramp_Imp',
               'SF_070005_VanNess_BRT',
               'SF_130011_2ndSt_Road_Diet',
# Not ready yet               'SF_Market_Street_Closure',
               'SM_110047_SR92_ElCam_Ramp_Mod',
               'SOL110005_Jepson_Van_to_Com',
               'SON070004_101_MarinSonNarrows_Phase1',
               'ALA050014_SR84_Widening',
               'ALA170011_BayBridge_HOV_Connectors',
               'ALA150047_TelegraphAve_Complete_Streets',
               'SM_110047_SR92_ElCam_Ramp_Mod',
               'SCL190002_280_Foothill_improvement',
               'SCL190006_101SB_offramp_improvement',
               'I80_AdaptiveRampMetering',
               'VAR170021_Freeway_Performance_I880',
               'SonomaCounty_Transit_NoBuild2050',
               'SF_MuniForward_Committed'],
        'trn':['ALA050015_BART_to_WarmSprings',
               'ACGo',
               'CC_050025_EBart_to_Antioch',
               'SCL110005_BART_to_Berryessa',
               'SF_010015_Transbay_Terminal',
               'SF_010037_Muni_Central_Subway',
               'SF_070027_Yerba_Buena_Ramp_Imp',
               'SOL030002_FairfieldVacaville_Stn',
               'SON090002_SMART',
               'SON090002_SMART_to_Larkspur',
               'CC_070062_Richmond_Ferry',
               'SF_MuniForward_Committed',
               'VTA_Next',
               'SCL130001_237_101_MAT_Int_Mod',
               'SonomaCounty_Transit_NoBuild2050',
               'SMART_Novato',
               'Xfare_update_2020',
               'ACTransit_Committed',
               'ferry_update_2019',
               'SamTrans_ECR_Rapid'],
    }),
    (2025, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2025'}},
               'EXP_CC_050028_I680_SB_HOV_Completion',
               'EXP_101B1',
               'EXP_101B2',
               'EXP_680C1',
               'EXP_85C',
               'EXP_101C',
               'ALA150001_I680_SR84_Int_Wid',
               'ALA150043_Claremont_road_diet',
               'CC_070009_Slatten_Ranch_Rd_Extension',
               'SF_070004_Geary_BRT_Phase1',
               'SON070004_101_MarinSonNarrows_Phase2',
               'SOL110006_Jepson_1B_1C',
               'SCL190008_US101_DLC_Int_Imp',
               'I880_US101_AdaptiveRampMetering',
               'MAJ_SCL050009_VTA_Eastridge_Extension',
               'SOL070020_I80_I680_SR12_Int_1_2A'],
        'trn':['SF_010028_Caltrain_Modernization',
               'SON090002_SMART_to_Windsor',
               'MAJ_SCL050009_VTA_Eastridge_Extension',
               'REG090037_New_BART_Trains',
               'SOL070020_I80_I680_SR12_Int_1_2A']
    }),
    (2030, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2030'}},
               'EXP_880A'],
        'trn':['BART_NoProject']
    }),
    (2035, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2035'}}],
        'trn':[]
    }),
    (2040, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2040'}}],
        'trn':[]
    }),
    (2045, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2045'}}],
        'trn':[]
    }),
    (2050, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2050'}}],
        'trn':[]
    })
])

###########################################################
# Blueprint projects
BLUEPRINT_PROJECTS = collections.OrderedDict([
        (2015, {'hwy':[],
                'trn':[]
        }),
        (2020, {'hwy':['MAJ_AC_Frequency_Improvement',
                       'RRSP_Alameda_Point_Transit_Improvements'],
                'trn':['MAJ_AC_Frequency_Improvement',
                       'RRSP_Alameda_Point_Transit_Improvements']
        }),
        (2025, {'hwy':['RRSP_E14_Mission_Corridor'],
                'trn':['RRSP_E14_Mission_Corridor']
        }),
        (2030, {'hwy':['MAJ_SanPablo_BRT'],
                'trn':['MAJ_BRT030001_BART_to_SanJose',
                       'BART_Irvington_Infill',
                       'MAJ_REG090037_BART_Core_Cap',
                       'MAJ_SanPablo_BRT',
                       'BP_PDA_Transit_Enhancements']
        }),
        (2035, {'hwy':['MAJ_MuniForward_Uncommitted',
                       'MAJ_Treasure_Island_Congestion_Pricing'],
                'trn':['MAJ_MuniForward_Uncommitted',
                       'RRSP_South_East_Waterfront_Transit_Imp',
                       'MAJ_Treasure_Island_Congestion_Pricing']
        }),
        (2040, {'hwy':[],
                'trn':[]
        }),
        (2045, {'hwy':[],
                'trn':[]
        }),
        (2050, {'hwy':[],
                'trn':[]
        })
    ])

###########################################################
# Blueprint Plus projects
BLUEPRINTPLUS_PROJECTS = collections.OrderedDict([
        (2015, {'hwy':[],
                'trn':[]
        }),
        (2020, {'hwy':[],
                'trn':[]
        }),
        (2025, {'hwy':[],
                'trn':[]
        }),
        (2030, {'hwy':[],
                'trn':[]
        }),
        (2035, {'hwy':[],
                'trn':[]
        }),
        (2040, {'hwy':[],
                'trn':[]
        }),
        (2045, {'hwy':[],
                'trn':[]
        }),
        (2050, {'hwy':[],
                'trn':[]
        })
    ])

# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS = collections.OrderedDict()
for YEAR in COMMITTED_PROJECTS.keys():
    # BLueprint includes Commited projects
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'] + BLUEPRINT_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn'] + BLUEPRINT_PROJECTS[YEAR]['trn']
        }
#    elif PROJECT == "Blueprint Plus":
#          NETWORK_PROJECTS[YEAR] = {
#              'hwy':COMMITTED_PROJECTS[YEAR]['hwy'] + BLUEPRINT_PROJECTS[YEAR]['hwy'] + BLUEPRINTPLUS_PROJECTS[YEAR]['hwy'],
#              'trn':COMMITTED_PROJECTS[YEAR]['trn'] + BLUEPRINT_PROJECTS[YEAR]['trn'] + BLUEPRINTPLUS_PROJECTS[YEAR]['trn']
#            }

#
# For every year where a project is applied do the following:
# Convert all zero-length links to 0.01
# Move buses to HOV/Express lanes at the end
#
for YEAR in NETWORK_PROJECTS.keys():
    # if anything is applied
    if ((len(NETWORK_PROJECTS[YEAR]['hwy']) > 0) or (len(NETWORK_PROJECTS[YEAR]['trn']) > 0)):
        NETWORK_PROJECTS[YEAR]['hwy'].append('No_zero_length_links')

    if ((len(NETWORK_PROJECTS[YEAR]['hwy']) > 0) or (len(NETWORK_PROJECTS[YEAR]['trn']) > 0)):
        NETWORK_PROJECTS[YEAR]['trn'].append('Move_buses_to_HOV_EXP_lanes')


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