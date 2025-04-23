import os
# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT  = "Blueprint"

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "HEAD"              # Use this tag if you want NetworkWrangler to use the latest version in the local repo to build the network
# TAG = "PBA50_Blueprint"    # This is the default tag since this is the netspec for the Blueprint 

# roadway attributes to include; used by HighwayNetwork.writeShapefile() and HighwayNetwork.reportDiff()
ADDITONAL_ROADWAY_ATTRS = [
    'PROJ',           # added by PROJ_attributes
    'PBA2050_RTP_ID', # added by PBA2050_RTP_ID_attributes
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
# Blueprint projects
BLUEPRINT_PROJECTS = collections.OrderedDict([
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
                        'SF_130017_SF_Congestion_Pricing',
                    #    'FBP_MU_041_Hovercraft_Pilot',
                    #    'EXP_Blueprint',
                    #    'FBP_MU_044_SouthSF_Ferry_Serv_Incr',
                        'FBP_MU_029_ACRapid_2025',
                    #    'FBP_MR_026_NovatoWide',
                    #    'FBP_NP_038_TSP_On_SR29',
                    #    {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2025'},              'variants_exclude':['Alt1']},
                    #    {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2025'},              'variants_include':['Alt1']},
                        {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2025'}},
                    #    'FBP_CC_065_LaurelWide',
                    #    'FBP_SC_039_SR237WBWide',      
                    #    'FBP_AL_051_7St_Grade_Sep_West',
                    #    'FBP_SN_017_Arata_Int',
                    #    'FBP_CC_017_Brentwood_Intermodal',
                    #    'EXP_Blueprint',
                    #    'FBP_AL_039_I580_Interchange_Imps',
                    #    'FBP_CC_056_LaurelExtension',
                    #    'FBP_SC_084_10th_BridgeWide',
                    #    'FBP_SC_073_BlossomHill_101Wide',
                    #    'FBP_CC_045_SanPabloDam_Interchange_Phase2',

                    #    'FBP_SM_034_Route92_ElCamino_Interchange',
                    #    'FBP_SL_019_BeniciaRoad_Diet',
                    #    'FBP_SL_023_WestTexasRoad_Diet',
                    #    'FBP_SN_012_PetalumaBlvd_Diet',
                    #    {'name':'EIR2_Val_Link_ExpressBus',                                                'variants_include':['Alt2']},
                    #    {'name':'EIR2_ReXBlue',                                                            'variants_include':['Alt2']},
                    #    'FBP_SC_072_US101_Trimble_Interchange',
                        {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2025'}},
                        'BP_Vision_Zero',
                       ],
                'trn':[
                    #    'FBP_AL_001_NewarkFremPDA',
                    #    {'name':'FBP_MU_059_ACTransbay_Freq_Incr',                                         'variants_exclude':['Alt2']},
                        'SF_130017_SF_Congestion_Pricing',
                    #    'FBP_MU_041_Hovercraft_Pilot',
                    #    'FBP_MU_060_ReX_Blue',
                    #    {'name':'EIR2_ReXBlue',                                                            'variants_include':['Alt2']},                       
                    #    'FBP_MU_044_SouthSF_Ferry_Serv_Incr',
                         {'name':'GGT_Service_Imp',                                                         'kwargs':{'MODELYEAR':'2025'}},
                        'FBP_MU_029_ACRapid_2025',  
                        {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2025'}},
                    #    {'name':'EIR1_Freq_Boosts',              'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt1']},
                    #    {'name':'EIR2_HRA_Freq_Incr',            'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt2']},
                    #    {'name':'EIR2_PDA_Freq_Incr',            'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt2']},
                    #    {'name':'EIR2_Val_Link_ExpressBus',                                                'variants_include':['Alt2']}
                       ]
        }),
        (2030, {'hwy':[
                    #    'BP_Tolls_On_Congested_Freeways_2030',
                        'FBP_AL_021_South_Bay_Connect',
                        'FBP_SF_Caltrain_Bayview',
                    #    'FBP_MU_044_Richmond_Ferry_Serv_Incr',
                    #    {'name':'Transform_Valley_Link',                                                   'variants_exclude':['Alt2']},
                        'FBP_NP_040_VINE_Exp_Bus_Enhancements',
                        'FBP_AL_045_Oak_Ala_Access_Pr',
                    #    {'name':'FBP_MR_021_101_580_Direct_Connector',                                     'variants_exclude':['Alt1']},
                        'FBP_MR_018_US101_BOS',
                    #    'FBP_CC_036_I80_ExpBus_Impr',
                        {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'1'"},  'variants_exclude':['Alt1']},
                        {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'2'"},  'variants_exclude':['Alt1']},
                        {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5','kwargs':{'PHASE':"'4'"}, 'variants_exclude':['Alt1']},
                    #    'FBP_CC_021_Ant_Mart_Herc_Ferry',
                    #    {'name':'EXP_uncommitted_all',              'kwargs':{'MODELYEAR':'2030'},         'variants_exclude':['Alt1']},
                    #    {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2030'},},
                    #    {'name':'EIR1_EXP_uncommitted_all',         'kwargs':{'MODELYEAR':'2030'},         'variants_include':['Alt1']},
                        {'name':'I880_US101_AdaptiveRampMetering',  'kwargs':{'MODELYEAR':'2030'}}, # this is a component of Bay Area Forward
                        {'name':'MAJ_Bay_Area_Forward_all',         'kwargs':{'MODELYEAR':'2030'}},
                    #    'FBP_CC_066_CypressWide',
                    #    'FBP_SC_059_SR237EBWide',
                       'FBP_AL_044_I880_Whipple_Imps',
                       'ALA110002_I880_Industrial_Interchange',
                    #    'FBP_AL_064_UnionCityWide',
                    #    'FBP_SC_074_US101_BuenaVista_Int',
                    #    'EXP_Blueprint',
                        'FBP_SC_054_SR17_Corridor_Relief',
                       'FBP_SM_042_Hwy1_ManorDrive',
                    #    'FBP_CC_024_Oakley_PNR_Tri_Delta',
                    #    'FBP_SC_083_US101_Zanker_Skyport_Interchange',
                    #    'FBP_SL_022_SonomaBlvd_Diet',
                        'FBP_SM_027_US101_92',
                    #    'FBP_SM_007_ElCamino_CompleteStreets',
                        'FBP_AL_062_TassajaraWide',
                        'Dumbarton_Bridge_Bus_Service',
                        'SCL210026_Julian_James_Conversion',
                        'EXP_CC_I680NB_Livorna_to_Arthur',
                        'EXP_AL_I680NB_SR84_to_Alcosta',
                        'EXP_SM_US101_I380_to_SFcounty',
                        'EXP_SC_SR85_SR87_to_US101_Phase4',
                        'EXP_SC_US101_SR237_to_I880_Phase5',
                        'EXP_SC_US101_I880_to_SR85_Phase6',
                        'FBP_CC_028_Hercules_Station',
                        'FBP_CC_054_CrowCanyonWide',
                        'FBP_SC_103_MontagueWide', 
                        'CC_070011_170015_Brentwood_Blvd_Widening',
                        'FBP_SM_033_US101_Holly_Interchange',
                        'FBP_SF_090004_Harney_Wide',
                        'STIP_17_06_0010_WoodsideRd',
                        'FBP_SC_082_US101_25_Interchange',
                        'SOL110004_Jepson_Walters_Extension',
                        'FBP_ALA_I800_42nd_High_Interchange',
                        'FBP_CC_050_SR4_Operation_Improvements_EB',
                        {'name':'MAJ_SC_VTAVisionaryNetwork', 'kwargs':{'MODELYEAR': '2030'}},
                        'SCL230001_SR237_Middlefield_interchange',
                        'Transform_SR37_Widening_Interim',
                        'FBP_SC_041_Envision_Highway_Minor',
                        'BP_Vision_Zero',
                       ],
                'trn':[
                       'BP_PDA_Transit_Enhancements',
                       {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2030'}},
                    #    'BART_Irvington_Infill',
                       'MAJ_REG090037_BART_Core_Cap',
                       'FBP_AL_021_South_Bay_Connect',
                       'MAJ_WETA_Service_Frequency_Increase',
                       'FBP_NP_040_VINE_Exp_Bus_Enhancements',
                       'FBP_CC_019_CCCTA_Freq_Increase',
                    #    'FBP_MU_061_ReX_Green',
                    #    'FBP_MU_044_Richmond_Ferry_Serv_Incr',
                    #    {'name':'Transform_Valley_Link',                                                   'variants_exclude':['Alt2']},
                    #    'FBP_SF_028_SF_Express_Bus_On_Exp_Lanes',
                    #    {'name':'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',                             'variants_exclude':['Alt2']},
                    #    {'name':'FBP_SF_024_Historic_Streetcar_Ext',                                       'branch':'PBA50plus_DBP'},
                    #    'FBP_CC_036_I80_ExpBus_Impr',
                    #    'FBP_CC_021_Ant_Mart_Herc_Ferry',
                        'FBP_AL_045_Oak_Ala_Access_Pr',
                        'FBP_CC_028_Hercules_Station',
                        'MAJ_MTC050027_Berkeley_Ferry',
                    #    'FBP_CC_024_Oakley_PNR_Tri_Delta',
                    #    {'name':'EIR1_Freq_Boosts',              'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt1']},
                    #    {'name':'EIR2_HRA_Freq_Incr',            'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                    #    {'name':'EIR2_PDA_Freq_Incr',            'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                    #    {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                        'Dumbarton_Bridge_Bus_Service',
                        {'name':'MAJ_SC_VTAVisionaryNetwork', 'kwargs':{'MODELYEAR': '2030'}},
                        {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2030'}},
                        'SON_SMART_to_Healdsburg',
                        {'name':'GGT_Service_Imp',                                                         'kwargs':{'MODELYEAR':'2030'}},
                        'FBP_MU_049_Caltrain_6TPHPD',
                        'FBP_SF_Caltrain_Bayview',
                        'Transform_SR37_Widening_Interim',
                        'FBP_NP_NapaVine_Serv_Freq_Boost',
                       ]
        }),
        (2035, {'hwy':[
                        'MAJ_SanPablo_BRT',
                        'MAJ_MuniForward_Uncommitted',
                        'SF_110049_Treasure_Island_Congestion_Pricing',
                    #    'BP_Tolls_On_Congested_Freeways_2035',
                    #    {'name': 'NGF_BlueprintSegmented'},
                    #    'RRSP_East_West_Connector',
                    #    'FBP_SM_022_I380_Widening',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"3"'}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"4"'}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"5"'}},
                    #    {'name':'EXP_uncommitted_all',                  'kwargs':{'MODELYEAR':'2035'},     'variants_exclude':['Alt1']},
                    #    {'name':'EIR1_EXP_uncommitted_all',             'kwargs':{'MODELYEAR':'2035'},     'variants_include':['Alt1']},
                    #    'FBP_AL_076_TelegraphDiet',
                    #    'FBP_SN_018_Cotati_101_RailroadAve_Impr',
                    #    'FBP_NP_079_Trower_Ext',
                    #    'EXP_Blueprint',
                    #    {'name':'EIR1_No_SR37',                                                            'variants_include':['Alt1']},
                        'FBP_SM_027_US101_92_directConnector',
                        'FBP_T5_All_Lane_Tolling',
                        'BP_Vision_Zero',
                       ],
                'trn':[
                        'MAJ_MuniForward_Uncommitted',
                        'MAJ_AC_Frequency_Improvement',
                        'MAJ_SanPablo_BRT',
                    #    'FBP_MU_062_ReX_Red',
                        'SF_110049_Treasure_Island_Congestion_Pricing',
                    #    'RRSP_East_West_Connector',
                    #    'FBP_NP_079_Trower_Ext',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"3"'}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"4"'}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_packages_3_4_5', 'kwargs':{'PHASE':'"5"'}},
                       {'name':'FBP_SL_026_SolExpressBus',             'kwargs':{'MODELYEAR':'2035'}},
                       {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2035'}},
                    #    {'name':'FBP_SL_026_SolExpressBus',             'kwargs':{'MODELYEAR':'2035'}},
                    #    'FBP_SL_020_MilitaryWest_Diet',
                    #    {'name':'EIR1_Freq_Boosts',                     'kwargs':{'MODELYEAR':'2035'},     'variants_include':['Alt1']},
                    #    {'name':'EIR2_VTA_LRT_Orange',                                                     'variants_include':['Alt2']},
                    #    {'name':'EIR2_Fix_Alt2',                        'kwargs':{'MODELYEAR':'2035'},     'variants_include':['Alt2']},
                    #    {'name':'EIR1_No_SR37',                                                            'variants_include':['Alt1']},
                        'SON_SMART_to_Cloverdale',
                        {'name':'GGT_Service_Imp',                                                         'kwargs':{'MODELYEAR':'2035'}},
                        'Transform_SeamlessTransit',                        
                       ]
        }),
        (2040, {'hwy':[
                        'FBP_AL_055_DubBlvd_NCanyons_Ext',
                    #    'FBP_SC_050_I680_Montague_Int_Imp', 
                        'FBP_MU_029_ACRapid_2040',
                        'FBP_NP_074_SoscolWide',
                        'FBP_CC_057_LoneTreeWide',                        
                        'FBP_CC_059_PittAntiochWide',
                        'FBP_SL_053_PeabodyWide',
                        'Transform_I680_Multimodal_Imp',
                    #    'FBP_CC_037_680_AuxLanes',
                    #    {'name':'RRSP_EC_Cap_Imp_ECR_Bus',                                                 'branch':'PBA50plus_DBP'},
                        'MAJ_SR_239',
                    #    'FBP_NP_033_Napa_PNR_Lots',
                        'FBP_CC_018_BRT_Brentwood',
                    #    'FBP_SC_043_I280_Mainline_Impr',
                       'MAJ_ElCaminoReal_BRT',
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'1'}},
                       'FBP_AL_042_I680_Stoneridge_Widening',
                    #    {'name':'EXP_uncommitted_all',                            'kwargs':{'MODELYEAR':'2040'},    'variants_exclude':['Alt1']},
                    #    {'name':'EIR1_EXP_uncommitted_all',                       'kwargs':{'MODELYEAR':'2040'},    'variants_include':['Alt1']},
                    #    'FBP_SC_105_SanTomasWide',
                        'FBP_SC_102_CalaverasWide',
                    #    'FBP_CC_039_Eastbound24Wide',
                    #    {'name':'FBP_MU_064_SR37_LongTerm',                                               'variants_exclude':['Alt1']},
                    #    'FBP_SC_094_LawrenceWide',
                        'FBP_NP_066_Newell_Dr',
                    #    'EXP_Blueprint',
                        'FBP_AL_052_AutoMallWide',
                    #    'FBP_CC_038_SR242_Clayton_OnOffRamps',
                        'FBP_SC_047_I280_Winchester_OffRamp',
                        'FBP_SC_076_US101_Taylor_Interchange',
                        'FBP_NP_051_Airport_Junction',
                        'FBP_SC_101_BrokawBridgeWide',
                    #    'FBP_SC_081_US101_SR237',
                    #    'FBP_SC_088_Envision_Expwy',
                    #    {'name':'FBP_MU_056_Dumbarton_GRT',                                                'variants_exclude':['Alt2']},
                    #    {'name':'EIR2_Val_Link_ExpressBus',      'kwargs':{'action':"'revert'"},           'variants_include':['Alt2']},
                        'Transform_Valley_Link',
                    #    {'name':'Transform_AC_Transbay_Improvements',                                      'variants_include':['Alt2']},
                        'SCL210002_US101_SR152_Interchange',
                        'FBP_CC_067_WillowPassWide',
                        'FBP_AL_043_A_StreetWide',
                        'FBP_SL_033_FairgroundsWide',
                        'FBP_SC_104_OaklandWide',
                        'FBP_CC_064_CaminoTassajaraWide',
                        'FBP_SL_042_Jepson_2B_2C',
                        'FBP_CC_061_062_West_Leland_Ext_Phases1_2',
                        'FBP_SON_Caulfield_Extension',
                        'SCL250204_10thBridge_Ext',
                        'SM110003_US101_ProduceAve',
                        'ALA090020_I880_Industrial_Parkway_AuxLanes',
                        'SCL190012_US101_SanAntonio_Charleston_Rengstroff_Int',
                        'BP_Vision_Zero',
                        'FBP_SF_030_Balboa_Park_Area_2',                        
                        'ALA230222_I580_Vasco',
                        'ALA090016_SR92_Clawiter_Whitesell_Int',
                       ],
                'trn':[
                    #    'MAJ_Vasona_LRT_Extension',
                        'FBP_MU_029_ACRapid_2040',
                    #    {'name':'RRSP_EC_Cap_Imp_ECR_Bus',                                                 'branch':'PBA50plus_DBP'},
                    #    'MAJ_SJC_People_Mover',
                        'MAJ_BRT030001_BART_to_SanJose',
                        'Transform_I680_Multimodal_Imp',
                    #    'FBP_NP_028_NapaVineRegRoutesFrequency',
                    #    'FBP_NP_034_NapaVineRegExpServiceHrs',
                    #    'FBP_NP_029_NapaVineLocExpServiceHrs',
                    #    'FBP_NP_033_Napa_PNR_Lots',
                    #    'FBP_SC_043_I280_Mainline_Impr',
                        'FBP_CC_018_BRT_Brentwood',
                        {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'1'}},
                    #    {'name':'FBP_MU_064_SR37_LongTerm',                                                'variants_exclude':['Alt1']},
                        'FBP_NP_051_Airport_Junction',
                    #    {'name':'FBP_MU_056_Dumbarton_GRT',                                                'variants_exclude':['Alt2']},
                    #    'FBP_SC_088_Envision_Expwy',
                    #    {'name':'HSR',                                                                     'variants_exclude':['Alt2']},
                    #    {'name':'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',                             'variants_include':['Alt2']},
                    #    {'name':'EIR2_Val_Link_ExpressBus',      'kwargs':{'action':"'revert'"},           'variants_include':['Alt2']},
                        'Transform_Valley_Link',
                    #    {'name':'Transform_AC_Transbay_Improvements',                                      'variants_include':['Alt2']},
                    #    {'name':'EIR2_ReXGreen',                                                           'variants_include':['Alt2']},
                    #    {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2040'},            'variants_include':['Alt2']},
                        'FBP_SON_Caulfield_Extension',
                        'SCL250204_10thBridge_Ext',
                        'FBP_MU_049_Caltrain_8TPHPD',
                        'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',
                        'FBP_MuniForward_Uncommitted_Rail',
                        {'name':'MAJ_Sonoma_Frequency_Increase',                                            'kwargs':{'MODELYEAR':'2040'}},
                       'RRSP_South_East_Waterfront_Transit_Imp',
                       ]
        }),
        (2045, {'hwy':[ 
                        'RRSP_E14_Mission_Corridor',
                    #    {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2045'},            'variants_exclude':['Alt1']},
                    #    {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2045'},            'variants_include':['Alt1']},
                        {'name':'FBP_AL_048_SR262_Phase1',                                                 'variants_exclude':['Alt1']},
                    #    'FBP_NP_045_SR29_Gateway_Impr',
                    #    'EXP_Blueprint',
                        'FBP_SF_012_Geneva_Harney_BRT',
                        {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'2'}},
                        {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'3'}},
                        {'name':'MAJ_SC_VTAVisionaryNetwork', 'kwargs':{'MODELYEAR': '2045'}},
                        'RRSP_EC_Cap_Imp_ECR_Bus',
                        'BP_Vision_Zero',
                       ],
                'trn':[
                    {'name':'FBP_SM_020_Regional_Express_Buses', 'kwargs':{'PHASE':"'Phase1_4Routes'"}},
                    {'name':'FBP_SM_020_Regional_Express_Buses',    'kwargs':{'PHASE':"'Phase2_2Routes'"}},
                        'MAJ_RedwoodCity_SF_Ferry',
                        'BART_Irvington_Infill',
                        {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'2'}},
                        {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'PHASE':'3'}},
                        'RRSP_E14_Mission_Corridor',
                       {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2045'}},
                    #    'FBP_SC_106_VTA_LRT_Modernization',
                        'FBP_SF_012_Geneva_Harney_BRT',
                        {'name':'MAJ_SC_VTAVisionaryNetwork', 'kwargs':{'MODELYEAR': '2045'}},
                        'RRSP_Alameda_Point_Transit_Improvements',
                        'RRSP_EC_Cap_Imp_ECR_Bus',                
                       ]
        }),
        (2050, {'hwy':[
                        'FBP_CC_051_SR4_Operation_Improvements_WB',
                    #    'FBP_SC_028_Stevens_Creek_LRT',
                    #    'EXP_Blueprint',
                    #    'STIP_ITS_SM',
                    #    {'name':'BP_Transbay_Crossing',                                                    'variants_exclude':['Alt2']},
                        'BP_Vision_Zero',
                       ],
                'trn':[
                    #    'FBP_SC_028_Stevens_Creek_LRT',
                    #    {'name':'BP_Transbay_Crossing',                                                    'variants_exclude':['Alt2']}
                         'Transform_SeamlessTransit',                            
                       ]
        })
    ])


# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS   = collections.OrderedDict()

# NOTE: SLR is invoked explicitly in build_network_mtc_blueprint.py because it requires special handling
# re: backing up the network

# NET_VARIANTS
################
# "Baseline",                          # committed only
# "BPTransitProjectsOnly",             # committed + Blueprint Transit Projects 
# "BPTransitProjectsStrategyOnly",     # committed + Blueprint Transit Projects + Transit Strategies (T2/3/4); (T2/T4 are not network projects)
# "BPwithoutRoadwayPricingSafety",     # committed + Blueprint Transit Projects + Transit Strategies (T2/3/4) + Roadway Projects
# "BPwithoutRoadwaySafety",            # committed + Blueprint Transit Projects + Transit Strategies (T2/3/4) + Roadway Projects + Pricing (T5 ALT, cordons)
# "Blueprint",                         # committed + Blueprint Transit Projects + Transit Strategies (T2/3/4) + Roadway Projects + Pricing (T5 ALT, cordons) + Safety (T9/10)
# "Alt1",                              # EIR Alt 1, TBD
# "Alt2",                              # EIR Alt 2, TBD

T3_TRANSIT_STRATEGY = 'Transform_SeamlessTransit'
ROADWAY_PRICING_STRATEGIES = [
    'FBP_T5_All_Lane_Tolling',
    'SF_130017_SF_Congestion_Pricing',
    'SF_110049_Treasure_Island_Congestion_Pricing'
]
T10_SAFETY_STRATEGY = 'BP_Vision_Zero'

for YEAR in COMMITTED_PROJECTS.keys():
    if NET_VARIANT == "Baseline":
        # baseline: just committed
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn']
        }
        continue

    Wrangler.WranglerLogger.info(f"Constructing project list for {YEAR}")
    # TODO: delete? I don't think this did anything
    # blueprint, alt1, alt2
    if YEAR not in BLUEPRINT_PROJECTS: 
        Wrangler.WranglerLogger.warn(f"YEAR {YEAR} in COMMITTED_PROJECTS.keys() but not BLUEPRINT_PROJECTS")
        continue

    # For these, we want transit projects only
    # But some transit projects have a roadway component -- include that as well
    if NET_VARIANT in ["BPTransitProjectsOnly", "BPTransitProjectsStrategyOnly"]:

        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn'] + BLUEPRINT_PROJECTS[YEAR]['trn']
        }

        # for BPTransitProjectsOnly, remove T3 Seamless
        if NET_VARIANT == "BPTransitProjectsOnly":
            if T3_TRANSIT_STRATEGY in NETWORK_PROJECTS[YEAR]['trn']:
                NETWORK_PROJECTS[YEAR]['trn'].remove(T3_TRANSIT_STRATEGY)
                Wrangler.WranglerLogger.info(f"  Removing transit strategy {T3_TRANSIT_STRATEGY}")

        # ROADWAY_PRICING_STRATEGIES may have transit components - remove those
        for roadway_pricing in ROADWAY_PRICING_STRATEGIES:
            if roadway_pricing in NETWORK_PROJECTS[YEAR]['trn']:
                NETWORK_PROJECTS[YEAR]['trn'].remove(roadway_pricing)
                Wrangler.WranglerLogger.info(f"  Removing roadway pricing strategy from transit {roadway_pricing}")

        # check if transit project has a roadway component in BLUEPRINT_PROJECTS and check the primary network for that project.
        # For roadway, remove from transit. For transit, add to roadway.
        roadway_projects_in_transit = []

        # for convenience, make a list of the names of roadway projects that are dicts for checking
        blueprint_roadway_dict_projects = [] 
        for proj_dict in BLUEPRINT_PROJECTS[YEAR]['hwy']: 
            if isinstance(proj_dict,dict): blueprint_roadway_dict_projects.append(proj_dict['name'] )
        Wrangler.WranglerLogger.debug(f"Checking projects in transit AND roadway; {blueprint_roadway_dict_projects=}")

        for transit_project in NETWORK_PROJECTS[YEAR]['trn']:
            if isinstance(transit_project, dict):
                transit_project = transit_project['name']
            # transit_project is a string

            # check if this is both roadway AND transit
            if transit_project in BLUEPRINT_PROJECTS[YEAR]['hwy'] or transit_project in blueprint_roadway_dict_projects:

                # this is a roadway project *AND* a transit project -- but which one is it primarily?
                primary_network = build_network_mtc.getPrimaryNetworkForProject(transit_project, TEMP_SUBDIR)

                # if it's primarily a hwy network then we should delete from transit
                if primary_network == 'hwy':
                    roadway_projects_in_transit.append(transit_project)
                    continue
                
                # if it's primarily a transit project then we should add it to roadway
                Wrangler.WranglerLogger.info(f"  Transit project {transit_project} has roadway component and primary_network={primary_network}; adding")
                
                # add dict version
                if transit_project in blueprint_roadway_dict_projects:
                    for roadway_project in BLUEPRINT_PROJECTS[YEAR]['hwy']:
                        if isinstance(roadway_project,dict) and roadway_project['name'] == transit_project: 
                            NETWORK_PROJECTS[YEAR]['hwy'].append(roadway_project)
                else:
                    NETWORK_PROJECTS[YEAR]['hwy'].append(transit_project)

        # cleanup -- delete the roadway_projects_in_transit from transit
        for roadway_project in roadway_projects_in_transit:
            Wrangler.WranglerLogger.info(f"  Roadway project {roadway_project} has transit component and primary_network={primary_network}; removing")

            for project_idx in range(len(NETWORK_PROJECTS[YEAR]['trn'])-1,-1,-1):
                # check dict version
                if isinstance(NETWORK_PROJECTS[YEAR]['trn'][project_idx],dict) and NETWORK_PROJECTS[YEAR]['trn'][project_idx]['name'] == roadway_project:
                    del NETWORK_PROJECTS[YEAR]['trn'][project_idx]
                    Wrangler.WranglerLogger.info(f"  Roadway project {roadway_project} has transit component and primary_network={primary_network}; removing")
                    break
                # just string
                if NETWORK_PROJECTS[YEAR]['trn'][project_idx] == roadway_project:
                    del NETWORK_PROJECTS[YEAR]['trn'][project_idx]
                    Wrangler.WranglerLogger.info(f"  Roadway project {roadway_project} has transit component and primary_network={primary_network}; removing")
                    break
                
        continue

    # NET_VARIANT is one of "BPwithoutRoadwayPricingSafety", "BPwithoutRoadwaySafety", "Blueprint", "Alt1", "Alt2"
    NETWORK_PROJECTS[YEAR] = {
        'hwy':COMMITTED_PROJECTS[YEAR]['hwy'] + BLUEPRINT_PROJECTS[YEAR]['hwy'],
        'trn':COMMITTED_PROJECTS[YEAR]['trn'] + BLUEPRINT_PROJECTS[YEAR]['trn']
    }

    # remove roadway safety
    if NET_VARIANT in ["BPwithoutRoadwayPricingSafety", "BPwithoutRoadwaySafety"]:
        if T10_SAFETY_STRATEGY in NETWORK_PROJECTS[YEAR]['hwy']:
            NETWORK_PROJECTS[YEAR]['hwy'].remove(T10_SAFETY_STRATEGY)
            Wrangler.WranglerLogger.info(f"  Removing roadway safety strategy {T10_SAFETY_STRATEGY}")

    # remove roadway pricing from hwy and trn
    if NET_VARIANT == "BPwithoutRoadwayPricingSafety":
        for roadway_pricing in ROADWAY_PRICING_STRATEGIES:
            if roadway_pricing in NETWORK_PROJECTS[YEAR]['hwy']:
                NETWORK_PROJECTS[YEAR]['hwy'].remove(roadway_pricing)
                Wrangler.WranglerLogger.info(f"  Removing roadway pricing strategy from transit {roadway_pricing}")

            if roadway_pricing in NETWORK_PROJECTS[YEAR]['trn']:
                NETWORK_PROJECTS[YEAR]['trn'].remove(roadway_pricing)
                Wrangler.WranglerLogger.info(f"  Removing roadway pricing strategy from transit {roadway_pricing}")
                       
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

    # NOTE: SLR is handled in build_network_mtc_blueprint.py

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
