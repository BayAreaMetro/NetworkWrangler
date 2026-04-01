import os, pathlib
# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT  = "BaseNetwork"

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "HEAD"              # Use this tag if you want NetworkWrangler to use the latest version in the local repo to build the network
# TAG = "PBA50_Blueprint"    # This is the default tag since this is the netspec for the Blueprint 

# roadway attributes to include; used by HighwayNetwork.writeShapefile() and HighwayNetwork.reportDiff()
ADDITONAL_ROADWAY_ATTRS = [
    'PROJ',           # added by PROJ_attributes
]

# A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}
###########################################################
COMMITTED_PROJECTS = collections.OrderedDict([
    (2015, {
        'hwy':['PROJ_attributes',  # adds PROJ attributes to NODE and LINK
               'PBA2050_RTP_ID_attributes', # adds PBA2050_RTP_ID to NODE and LINK
               {'name':'Bridge_Toll_Updates_rtp2025', 'kwargs':{'MODELYEAR':'2015'}}],
        'trn':[]
    }),
    (2020, {
        'hwy':[{'name':'Bridge_Toll_Updates_rtp2025', 'kwargs':{'MODELYEAR':'2020'}},
               {'name':'EXP_237B',                   'kwargs':{'FUTURE':"PBA50"}}, # todo: update this to support PBA50
               'EXP_580C',
               'EXP_680D',
               'EXP_880A',
               'HOV_680F',
               'SCL130001_237_101_MAT_Int_Mod',
               'REG090003_SCLARA_FIP',
               'ALA130005_Dougherty_road_widening',
               'ALA130006_Dublin_Blvd_widening',
               'ALA130014_7th_St_road_diet',
               'ALA130026_Shattuck_Complete_Streets',
               'ALA150004_EastBay_BRT',
               'CC_130001_BaileyRd_SR4',
               'CC_130046_I680_SR4_Int_Rec',
               'CC_070035_I80_SPDamRd_Int_Phase1',
               'CC_070075_Kirker_Pass_Truck_Lane',
               'CC_090019_Bollinger_Canyon_Widening',
               'CC_130006_Concord_BART_road_diets',
               'CC_170001_SanRamonValleyBlvd_Lane_Addition',
               'MRN150009_San_Rafael_Bridge_Improvements',
               'SF_130011_2ndSt_Road_Diet',
               'SF_Market_Street_Closure',
               'SM_110047_SR92_ElCam_Ramp_Mod',
               'SOL110005_Jepson_Van_to_Com',
               'FBP_SL_042_Jepson_2A',
               'SON070004_101_MarinSonNarrows_Phase1',
               'ALA050014_SR84_Widening',
               'ALA170011_BayBridge_HOV_Connectors',
               'ALA150047_TelegraphAve_Complete_Streets',
               'SCL190002_280_Foothill_improvement',
               'SCL190006_101SB_offramp_improvement',
               'I80_AdaptiveRampMetering',
               'VAR170021_Freeway_Performance_I880',
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2020'}},  # This applies for multiple years on the roadway side
               'FBP_MU_029_Broadway_Transit_Only_Lanes',
               'EXP_Blueprint_NoProject',
               'FBP_AL_067_Rte84Wide',
               'FBP_AL_065_Bancroft_Bus_Only',
               'FBP_SM_032_US101_Willow_Interchange',
               ],
        'trn':['ALA050015_BART_to_WarmSprings',
               'ACGo',
               'CC_050025_EBart_to_Antioch',
               'GGTransit_Committed',
               'GGT_remove_access_restrictions',
               'SCL110005_BART_to_Berryessa',
               'SF_010015_Transbay_Terminal',
               'SOL030002_FairfieldVacaville_Stn',
               'SON090002_SMART',
               'SON090002_SMART_to_Larkspur',
               'CC_070062_Richmond_Ferry',
               'SF_MuniForward_Committed',
               'VTA_Next',
               'SCL130001_237_101_MAT_Int_Mod',
               'SMART_Novato',
               'Xfare_update_2020',
               'ACTransit_Committed',
               'ferry_update_2019',
               'Napa_Solano_Updates_2020',
               'FBP_Beale_Transit_Only_Lane',
               'SamTrans_ECR_Rapid',
               'ALA150004_EastBay_BRT',
               {'name':'FBP_SL_026_SolExpressBus', 'kwargs':{'MODELYEAR':'2020'}},
                ],
    }),
    (2023, {
        'hwy':[{'name':'Bridge_Toll_Updates_rtp2025', 'kwargs':{'MODELYEAR':'2023'}},
               'SF_070027_Yerba_Buena_Ramp_Imp_Completed',
               'EXP_CC_050028_I680_SB_HOV_Completion',
               'EXP_101B1',
               'EXP_101B2',
               'EXP_680C1',
               'EXP_680F',
               'EXP_85D',
               'EXP_101C',
               'ALA150043_Claremont_road_diet',
               'CC_070009_Slatten_Ranch_Rd_Extension',
               'SF_070004_Geary_BRT_Phase1',
               'SON070004_101_MarinSonNarrows_Phase2',
               'SOL070020_I80_I680_SR12_Int_1_2A',
               'FBP_NP_036_SR29_Imola_PNR',
               'ALA170052_Fruitvale_Ave_ped_improvements',
               'SF_070005_VanNess_BRT',
               {'name':'I880_US101_AdaptiveRampMetering', 'kwargs':{'MODELYEAR':'2023'}}, # this is a component of Bay Area Forward
               {'name':'MAJ_Bay_Area_Forward_all', 'kwargs':{'MODELYEAR':'2023'}},  # Adaptive Ramp Metering in 2023
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2023'}},  # This applies for multiple years on the roadway side
               'EXP_Blueprint_NoProject',
               'EXP_ObservedPrices_2023'
               ],
        'trn':['MAJ_Alameda_Point_SF_Ferry',
               'FBP_NP_036_SR29_Imola_PNR',
               'REG090037_New_BART_Trains',
               'SOL070020_I80_I680_SR12_Int_1_2A',
               'SF_010037_Muni_Central_Subway',
               'REG_Caltrain_2023',
               'SF_070027_Yerba_Buena_Ramp_Imp_Completed',
               'GTFS2023_SF_Muni',
               'GTFS2023_SC_VTA',
               'GTFS2023_AC_ACTransit',
               'GTFS2023_SM_SamTrans',
               'GTFS2023_Other_Operators',
               # Transit_Frequency_Updates_Using_511
               # Update transit frequency for BART and Caltrain using 511 2023-09 data due to big service update in Sept 2023
               # Asana task: https://app.asana.com/0/1204085012544660/1205493838123328/f  
               # Update transit frequency for other operators using 511 2023-09 data 
               # Asana task: https://app.asana.com/0/1204085012544660/1205943132254853/f
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"',
                          'operator':'"Bay Area Rapid Transit"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"',
                          'operator':'"Altamont Corridor Express"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"',
                          'operator':'"Capitol Corridor Joint Powers Authority"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"',
                          'operator':'"San Francisco Municipal Transportation Agency"'}},                   
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Caltrain"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"VTA"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Golden Gate Ferry"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"AC TRANSIT"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"SamTrans"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Union City Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Marin Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Tri Delta Transit"'}},  
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Sonoma Marin Area Rail Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Petaluma"'}},  
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"County Connection"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"FAST"'}},
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Golden Gate Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"SolTrans"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"VINE Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Sonoma County Transit"'}},
                # Santa Rosa CityBus implementation isn't used since their GTFS data is inaccurate
                #  https://app.asana.com/0/0/1206596966483061/f
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"WestCat (Western Contra Costa)"'}}, 
                # no model routes for Rio Vista Delta Breeze
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Dumbarton Express Consortium"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"', 
                          'operator':'"Emery Go-Round"'}},
                {'name':'Transit_Frequency_Updates_Using_511',
                'kwargs':{'regional_gtfs_zip':'"2023-09.zip"',
                          'operator':'"Vacaville City Coach"'}},
                # San Francisco Bay Ferry is updated via `GTFS2023_SB_SFBayFerry` rather than Sep2023 GTFS default method
                'GTFS2023_SB_SFBayFerry',
                # Treasure Island Ferry is added via 'MAJ_Treasure_Island_Ferry' rather than Sep2023 GTFS
                # https://app.asana.com/0/0/1206560526595918/1208653731926585/f
                'MAJ_Treasure_Island_Ferry',
        ]
    }),
])


# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS   = collections.OrderedDict()


for YEAR in COMMITTED_PROJECTS.keys():
    if NET_VARIANT == "Baseline":
        # baseline: just committed
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn']
        }
        continue

#
# For every year where a project is applied do the following:
# Convert all zero-length links to 0.01
# Check tolls exist for tolls links
# Move buses to HOV/Express lanes at the end
#
for YEAR in NETWORK_PROJECTS.keys():
    # if anything is applied
    if ((len(NETWORK_PROJECTS[YEAR]['hwy']) > 0) or (len(NETWORK_PROJECTS[YEAR]['trn']) > 0)):
        NETWORK_PROJECTS[YEAR]['hwy'].append('No_zero_length_links')
        # check the tolls file using the same file used in the model
        NETWORK_PROJECTS[YEAR]['hwy'].append({
            'name':'No_missing_tolls',
            'kwargs':{
                'TM1_CODE_DIR':build_network_mtc.TM1_CODE_DIR,
                'WRANGLER_SCRIPTS_DIR':str(pathlib.Path(__file__).parent),
            }
        })
 
    if ((len(NETWORK_PROJECTS[YEAR]['hwy']) > 0) or (len(NETWORK_PROJECTS[YEAR]['trn']) > 0)):
        NETWORK_PROJECTS[YEAR]['trn'].append('Move_buses_to_HOV_EXP_lanes')

Wrangler.WranglerLogger.info(f"======== NETWORK_PROJECTS for {NET_VARIANT} ========")
# since this is complicated, log it
for YEAR in NETWORK_PROJECTS.keys():
    Wrangler.WranglerLogger.info(f"  {YEAR}")
    for netmode in ['hwy','trn']:
        for project in NETWORK_PROJECTS[YEAR][netmode]:
            Wrangler.WranglerLogger.info(f"        {netmode}: {project}")

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
