import os

# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT = "TIP2027"

# MANDATORY. Set this to be the Scenario Name e.g. "NoProject","Project"
# for TIP2023, we only have to build the Project network
SCENARIO = "Project"

# MANDATORY. Set this to be the git tag for checking out network projects.
# TAG = "TIP_2027"
TAG = "HEAD"

# roadway attributes to include; used by HighwayNetwork.writeShapefile() and HighwayNetwork.reportDiff()
ADDITONAL_ROADWAY_ATTRS = [
    'PROJ',           # added by PROJ_attributes
]
# MANDATORY. Set this to the directory in which to write your outputs.
# "hwy" and "trn" subdirectories will be created here.
# OUT_DIR = PROJECT + "_" + SCENARIO + "_network_{}"  # YEAR
# OUT_DIR = PROJECT + "_" + "_network_{}"  # YEAR

# MANDATORY.  Should be a dictionary with keys "hwy", "muni", "rail", "bus"
# to a list of projects.  A project can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}

###########################################################
COMMITTED_PROJECTS = collections.OrderedDict([
    (2015, {
        'hwy':['PROJ_attributes',  # adds PROJ attributes to NODE and LINK
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
    (2025, {
        'hwy':[{'name':'Bridge_Toll_Updates_rtp2025', 'kwargs':{'MODELYEAR':'2025'}},             
               'ALA150001_I680_SR84_Int_Wid',
               'SCL190008_US101_DLC_Int_Imp',
               'CC_170061_Bus_On_Shoulder_680BRT',
               'MAJ_SCL050009_VTA_Eastridge_Extension',
               'MAJ_Geary_BRT_Phase2',
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2025'}},  # This applies for multiple years on the roadway side
               'MRN050034_101_MarinSonNarrows_Phase2',
               'EXP_Blueprint_NoProject',
               'EXP_SL030_I80_RedTopRd_to_I505',
               'EXP_AL025_I680_SR84_to_Alcosta',
               'FBP_NP_044_Soscol_Junction',
               'ALA170011_BayBridge_HOV_Connectors_phase2',
               'FBP_CC_030_OakleyAmtrak',
               ],
        'trn':['SF_010028_Caltrain_Modernization',
               'SON090002_SMART_to_Windsor',
               'SON090002_SMART_NorthPetaluma',
               'MAJ_SCL050009_VTA_Eastridge_Extension',
               'MAJ_Geary_BRT_Phase2',
               'SamTrans_2024_restore_expand_services',
               'FBP_NP_044_Soscol_Junction',
               'MAJ_MissionBay_SF_Ferry',
               'FBP_CC_030_OakleyAmtrak',  
               ]
    }),
    (2030, {
        'hwy':[{'name':'Bridge_Toll_Updates_rtp2025', 'kwargs':{'MODELYEAR':'2030'}},
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2030'}},  # This applies for multiple years on the roadway side
               'EXP_Blueprint_NoProject',
               'FBP_SM_035_Peninsula_101_OnOffRamps',
               'FBP_SC_082_US101_25_Interchang_committed',
               'SOL110006_Jepson_1B_1C',
               'ALA210028_I80_HOV_Bus_Lane_Ext',
               'ALA170049_Central_AVE_Safety_Improvements',
               {'name':'I880_US101_AdaptiveRampMetering',  'kwargs':{'MODELYEAR':'2030'}}, # this is a component of Bay Area Forward 
               ],
        'trn':[
            ]
    }),
    (2035, {
        'hwy':[
               'EXP_Blueprint_NoProject',
               'SCL190011_I280_Wolfe_Interchange'
            ],
        'trn':[]
    }),
    (2040, {
        'hwy':[
               'EXP_Blueprint_NoProject'],
        'trn':[]
    }),
    (2045, {
        'hwy':[
               'EXP_Blueprint_NoProject',
               'FBP_SCL_SR35_BRT_between_US101_SR87',
               ],
        'trn':[
               'FBP_SCL_SR35_BRT_between_US101_SR87',
        ]
    }),
    (2050, {
        'hwy':[
               'EXP_Blueprint_NoProject'],
        'trn':[]
    })
])

###########################################################
# TIP projects
TIP_PROJECTS = collections.OrderedDict([
        (2015, {'hwy':[],
                'trn':[]
        }),
        (2020, {'hwy':[],
                'trn':[]
        }),
        (2023, {'hwy':[],
                'trn':[]
        }),
        (2025, {'hwy':[
                        # 'SF_130017_SF_Congestion_Pricing',
                        # 'FBP_MU_029_ACRapid_2025',
                        # {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2025'}},
                        # {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2025'}},
                        # {'name':'BP_Vision_Zero',                'variants_exclude':['Alt1']},
                       ],
                'trn':[
                        # 'SF_130017_SF_Congestion_Pricing',
                        #  {'name':'GGT_Service_Imp',                                                         'kwargs':{'MODELYEAR':'2025'}},
                        # 'FBP_MU_029_ACRapid_2025',  
                        # {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2025'}},
                       ]
        }),
        (2030, {'hwy':[
                        # 'FBP_AL_021_South_Bay_Connect',
                        # 'FBP_SF_Caltrain_Bayview',
                        # 'FBP_NP_040_VINE_Exp_Bus_Enhancements',
                        # 'FBP_AL_045_Oak_Ala_Access_Pr',
                        # 'FBP_MR_018_US101_BOS',
                        # {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'1'"},  'variants_exclude':['Alt1']},
                        # {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'2'"},  'variants_exclude':['Alt1']},
                        # {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'4'"},  'variants_exclude':['Alt1']},
                        # {'name':'I880_US101_AdaptiveRampMetering',  'kwargs':{'MODELYEAR':'2030'}}, # this is a component of Bay Area Forward
                        # {'name':'MAJ_Bay_Area_Forward_all',         'kwargs':{'MODELYEAR':'2030'}},
                        # {'name':'FBP_AL_044_I880_Whipple_Imps',                        'variants_exclude':['Alt1']}, 
                        # {'name':'ALA110002_I880_Industrial_Interchange',               'variants_exclude':['Alt1']},
                        # {'name':'FBP_SC_054_SR17_Corridor_Relief',                     'variants_exclude':['Alt1']},
                        # 'FBP_SM_042_Hwy1_ManorDrive',
                        # 'FBP_SM_027_US101_92',
                        # {'name':'FBP_AL_062_TassajaraWide',                            'variants_exclude':['Alt1']},
                        # 'Dumbarton_Bridge_Bus_Service',
                        # 'SCL210026_Julian_James_Conversion',
                        # {'name':'EXP_CC_I680NB_Livorna_to_Arthur',                     'variants_exclude':['Alt1']},
                        # {'name':'EXP_AL_I680NB_SR84_to_Alcosta',                       'variants_exclude':['Alt1']},
                        # {'name':'EXP_SM_US101_I380_to_SFcounty',                       'variants_exclude':['Alt1']},
                        # 'EXP_SC_SR85_SR87_to_US101_Phase4',
                        # {'name':'EXP_SC_US101_SR237_to_I880_Phase5',                   'variants_exclude':['Alt1']},
                        # {'name':'EXP_SC_US101_I880_to_SR85_Phase6',                    'variants_exclude':['Alt1']},
                        # 'FBP_CC_028_Hercules_Station',
                        # {'name':'FBP_CC_054_CrowCanyonWide',                           'variants_exclude':['Alt1']},
                        # {'name':'FBP_SC_103_MontagueWide',                             'variants_exclude':['Alt1']},
                        # {'name':'CC_070011_170015_Brentwood_Blvd_Widening',            'variants_exclude':['Alt1']},
                        # 'FBP_SM_033_US101_Holly_Interchange',
                        # 'FBP_SF_090004_Harney_Wide',
                        # 'STIP_17_06_0010_WoodsideRd',
                        # 'FBP_SC_082_US101_25_Interchange',
                        # {'name':'SOL110004_Jepson_Walters_Extension',                  'variants_exclude':['Alt1']},
                        # 'FBP_ALA_I800_42nd_High_Interchange',
                        # {'name':'FBP_CC_050_SR4_Operation_Improvements_EB',            'variants_exclude':['Alt1']},
                        # {'name':'MAJ_SC_VTAVisionaryNetwork', 'kwargs':{'MODELYEAR': '2030'}},
                        # 'SCL230001_SR237_Middlefield_interchange',
                        # {'name':'Transform_SR37_Widening_Interim',                     'variants_exclude':['Alt1']},
                        # 'FBP_SC_041_Envision_Highway_Minor',
                        # 'ALA170002_I80_Ashby_Int',
                        # 'BP_Vision_Zero',                                    
                       ],
                'trn':[
                    #    'BP_PDA_Transit_Enhancements',
                    #    {'name':'FBP_MU_046_ACE_Freq_Inc',          'kwargs':{'MODELYEAR':'2030'}},
                    #    'MAJ_REG090037_BART_Core_Cap',
                    #    'FBP_AL_021_South_Bay_Connect',
                    #    'MAJ_WETA_Service_Frequency_Increase',
                    #    'FBP_NP_040_VINE_Exp_Bus_Enhancements',
                    #    'FBP_CC_019_CCCTA_Freq_Increase',
                    #     'FBP_AL_045_Oak_Ala_Access_Pr',
                    #     'FBP_CC_028_Hercules_Station',
                    #     'MAJ_MTC050027_Berkeley_Ferry',
                    #     'Dumbarton_Bridge_Bus_Service',
                    #     {'name':'MAJ_SC_VTAVisionaryNetwork',      'kwargs':{'MODELYEAR':'2030'}},
                    #     {'name':'MAJ_Sonoma_Frequency_Increase',   'kwargs':{'MODELYEAR':'2030'}},
                    #     'SON_SMART_to_Healdsburg',
                    #     {'name':'GGT_Service_Imp',                 'kwargs':{'MODELYEAR':'2030'}},
                    #     'FBP_MU_049_Caltrain_6TPHPD',
                    #     'FBP_SF_Caltrain_Bayview',
                    #     {'name':'Transform_SR37_Widening_Interim',                 'variants_exclude':['Alt1']},
                    #     'FBP_NP_NapaVine_Serv_Freq_Boost',
                       ]
        }),
        (2035, {'hwy':[
                        'FBP_AL_043_A_StreetWide',
                    #     'MAJ_SanPablo_BRT',
                    #     'MAJ_MuniForward_Uncommitted',
                    #     'SF_110049_Treasure_Island_Congestion_Pricing',
                    #    {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"3"'}},
                    #    {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"4"'}},
                    #    {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"5"'}},
                    #     'FBP_SM_027_US101_92_directConnector',
                    #     'FBP_T5_All_Lane_Tolling',
                    #     'FBP_CC_045_SanPabloDam_Interchange_Phase2',
                    #     'BP_Vision_Zero',
                       ],
                'trn':[
                    #     'MAJ_MuniForward_Uncommitted',
                    #     'MAJ_AC_Frequency_Improvement',
                    #     'MAJ_SanPablo_BRT',
                    #     'SF_110049_Treasure_Island_Congestion_Pricing',
                    #    {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"3"'}},
                    #    {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"4"'}},
                    #    {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"5"'}},
                    #    {'name':'FBP_SL_026_SolExpressBus',             'kwargs':{'MODELYEAR':'2035'}},
                    #    {'name':'MAJ_Sonoma_Frequency_Increase',        'kwargs':{'MODELYEAR':'2035'}},
                    #     'SON_SMART_to_Cloverdale',
                    #     {'name':'GGT_Service_Imp',                     'kwargs':{'MODELYEAR':'2035'}},
                    #     'Transform_SeamlessTransit',
                    #     {'name':'EIR_ALT1_IncreaseTransitService',      'kwargs':{'MODELYEAR':'2035', 'min_load':'0.5', 'freq_min': '15', 'freq_fac': '0.5'}, 'variants_include':['Alt1']}
                       ]
        }),
        (2040, {'hwy':[
                        # {'name':'FBP_AL_055_DubBlvd_NCanyons_Ext',                     'variants_exclude':['Alt1']},
                        # 'FBP_MU_029_ACRapid_2040',
                        # 'FBP_NP_074_SoscolWide',
                        # {'name':'FBP_CC_057_LoneTreeWide',                             'variants_exclude':['Alt1']},
                        # {'name':'FBP_CC_059_PittAntiochWide',                          'variants_exclude':['Alt1']},
                        # {'name':'FBP_SL_053_PeabodyWide',                              'variants_exclude':['Alt1']},
                        # 'Transform_I680_Multimodal_Imp',
                        # {'name':'MAJ_SR_239',                                          'variants_exclude':['Alt1']},
                        # 'FBP_CC_018_BRT_Brentwood',
                        # 'MAJ_ElCaminoReal_BRT',
                        # {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'1'}},
                        # 'FBP_AL_042_I680_Stoneridge_Widening',
                        # {'name':'FBP_SC_102_CalaverasWide',                            'variants_exclude':['Alt1']},
                        # 'FBP_NP_066_Newell_Dr',
                        # {'name':'FBP_AL_052_AutoMallWide',                             'variants_exclude':['Alt1']},
                        # 'FBP_SC_047_I280_Winchester_OffRamp',
                        # 'FBP_SC_076_US101_Taylor_Interchange',
                        # 'FBP_NP_051_Airport_Junction',
                        # {'name':'FBP_SC_101_BrokawBridgeWide',                         'variants_exclude':['Alt1']},
                        # {'name':'FBP_SC_088_Envision_Expwy',                           'variants_exclude':['Alt1']},
                        # 'Transform_Valley_Link',
                        # 'SCL210002_US101_SR152_Interchange',
                        # {'name':'FBP_CC_067_WillowPassWide',                           'variants_exclude':['Alt1']},
                        # 'FBP_SL_033_FairgroundsWide',
                        # {'name':'FBP_SC_104_OaklandWide',                              'variants_exclude':['Alt1']},
                        # {'name':'FBP_CC_064_CaminoTassajaraWide',                      'variants_exclude':['Alt1']},
                        # {'name':'FBP_SL_042_Jepson_2B_2C',                             'variants_exclude':['Alt1']},
                        # {'name':'FBP_CC_061_062_West_Leland_Ext_Phases1_2',            'variants_exclude':['Alt1']},
                        # {'name':'FBP_SON_Caulfield_Extension',                         'variants_exclude':['Alt1']},
                        # 'SCL250204_10thBridge_Ext',
                        # 'SM110003_US101_ProduceAve',
                        # {'name':'ALA090020_I880_Industrial_Parkway_AuxLanes',          'variants_exclude':['Alt1']},
                        # {'name':'SCL190012_US101_SanAntonio_Charleston_Rengstroff_Int','variants_exclude':['Alt1']},
                        # 'ALA230222_I580_Vasco',
                        # 'ALA090016_SR92_Clawiter_Whitesell_Int',
                        # 'ALA210024_GrandAve_Improvements',
                        # 'FBP_AL_039_I580_Interchange_Imps',
                        # 'ALA250210_I580_Greenville',
                        # 'FBP_SCL_050_I680_MontagueExpwy',
                        # 'FBP_SC_042_I280_Downtown_Access_Improvements',
                        # 'FBP_SC_083_US101_Zanker_Skyport_Interchange',
                        # {'name':'RRSP_East_West_Connector',                            'variants_exclude':['Alt1']},
                        # 'BP_Vision_Zero',
                       ],
                'trn':[
                    #     'FBP_MU_029_ACRapid_2040',
                    #     'MAJ_BRT030001_BART_to_SanJose',
                    #     'Transform_I680_Multimodal_Imp',
                    #     'FBP_CC_018_BRT_Brentwood',
                    #     {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'1'}},
                    #     'FBP_NP_051_Airport_Junction',
                    #     {'name':'FBP_SC_088_Envision_Expwy',                           'variants_exclude':['Alt1']},
                    #     'Transform_Valley_Link',
                    #     {'name':'FBP_SON_Caulfield_Extension',                         'variants_exclude':['Alt1']},
                    #     'SCL250204_10thBridge_Ext',
                    #     'FBP_MU_049_Caltrain_8TPHPD',
                    #     'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',
                    #     'FBP_MuniForward_Uncommitted_Rail',
                    #     {'name':'MAJ_Sonoma_Frequency_Increase',  'kwargs':{'MODELYEAR':'2040'}},
                    #    'RRSP_South_East_Waterfront_Transit_Imp',
                    #    'FBP_SC_042_I280_Downtown_Access_Improvements',
                       ]
        }),
        (2045, {'hwy':[ 
                        # 'RRSP_E14_Mission_Corridor',
                        # {'name':'FBP_AL_048_SR262_Phase1',                             'variants_exclude':['Alt1']},
                        # 'FBP_SF_012_Geneva_Harney_BRT',
                        # {'name':'FBP_CC_15_23rd_St_BRT',      'kwargs':{'PHASE':'2'}},
                        # {'name':'FBP_CC_15_23rd_St_BRT',      'kwargs':{'PHASE':'3'}},
                        # {'name':'MAJ_SC_VTAVisionaryNetwork', 'kwargs':{'MODELYEAR': '2045'}},
                        # 'RRSP_EC_Cap_Imp_ECR_Bus',
                        # 'BP_Vision_Zero',
                       ],
                'trn':[
                    # {'name':'FBP_SM_020_Regional_Express_Buses', 'kwargs':{'PHASE':"'Phase1_4Routes'"}},
                    # {'name':'FBP_SM_020_Regional_Express_Buses', 'kwargs':{'PHASE':"'Phase2_2Routes'"}},
                    #     'MAJ_RedwoodCity_SF_Ferry',
                    #     'BART_Irvington_Infill',
                    #     {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'2'}},
                    #     {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'3'}},
                    #     'RRSP_E14_Mission_Corridor',
                    #    {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2045'}},
                    #     'FBP_SF_012_Geneva_Harney_BRT',
                    #     {'name':'MAJ_SC_VTAVisionaryNetwork',   'kwargs':{'MODELYEAR':'2045'}},
                    #     'RRSP_Alameda_Point_Transit_Improvements',
                    #     'RRSP_EC_Cap_Imp_ECR_Bus',                
                       ]
        }),
        (2050, {'hwy':[
                        # {'name':'FBP_CC_051_SR4_Operation_Improvements_WB',            'variants_exclude':['Alt1']},
                        # 'BP_Vision_Zero',
                       ],
                'trn':[
                        # 'Transform_SeamlessTransit',
                        # {'name':'EIR_ALT1_IncreaseTransitService',      'kwargs':{'MODELYEAR':'2050', 'min_load':'0.7', 'freq_min': '15', 'freq_fac': '0.35'}, 'variants_include':['Alt1']}
                       ]
        })
    ])



###########################################################
# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS   = collections.OrderedDict()

for YEAR in COMMITTED_PROJECTS.keys():
    if SCENARIO == "NoProject":
        # baseline: just committed
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn']
        }

    else:
        # tip
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'] + TIP_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn'] + TIP_PROJECTS[YEAR]['trn']
        }
        # handle net_remove, nets keywords
        for netmode in ['hwy','trn']:

            # iterate backwards via index to delete cleanly
            for project_idx in range(len(NETWORK_PROJECTS[YEAR][netmode])-1,-1,-1):
                project = NETWORK_PROJECTS[YEAR][netmode][project_idx]
                # special handling requires project to be specified as dictionary
                if not isinstance(project, dict): continue

                # variants_exclude: specifies list of network variants for which this project should be *excluded*
                if 'variants_exclude' in project.keys() and NET_VARIANT in project['variants_exclude']:
                    Wrangler.WranglerLogger.info("Removing {} {} {}".format(YEAR, netmode, project))
                    del NETWORK_PROJECTS[YEAR][netmode][project_idx]
                    continue

                # variants_include: specifies list of network variants for which this project should be *included*
                # if this keyword is present, then this project is included *only* for variants in this list
                if 'variants_include' in project.keys() and NET_VARIANT not in project['variants_include']:
                    Wrangler.WranglerLogger.info("Removing {} {} {}".format(YEAR, netmode, project))
                    del NETWORK_PROJECTS[YEAR][netmode][project_idx]
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
