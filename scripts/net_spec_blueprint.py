import os
# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT  = "Blueprint"

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "HEAD"              # Use this tag if you want NetworkWrangler to use the latest version in the local repo to build the network
# TAG = "PBA50_Blueprint"    # This is the default tag since this is the netspec for the Blueprint 
# For NGF variants, the default TAG will be replaced by the alternative TAG "NGF_NoProject"  (this is handled with code in build_network_mtc_blueprint.py) 

# A project can either be a simple string, or it can be
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
               'ALA170049_Central_AVE_Safety_Improvements',
               'ALA150004_EastBay_BRT',
               'CC_130001_BaileyRd_SR4',
               'CC_130046_I680_SR4_Int_Rec',
               'CC_070035_I80_SPDamRd_Int_Phase1',
               'CC_070011_Brentwood_Blvd_Widening',
               'CC_070075_Kirker_Pass_Truck_Lane',
               'CC_090019_Bollinger_Canyon_Widening',
               'CC_130006_Concord_BART_road_diets',
               'CC_170001_SanRamonValleyBlvd_Lane_Addition',
               'MRN150009_San_Rafael_Bridge_Improvements',
               'SF_070027_Yerba_Buena_Ramp_Imp',
               'SF_130011_2ndSt_Road_Diet',
               'SF_Market_Street_Closure',
               'SM_110047_SR92_ElCam_Ramp_Mod',
               'SOL110005_Jepson_Van_to_Com',
               'FBP_SL_042_Jepson_2A',
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
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2020'}},  # This applies for multiple years on the roadway side
               'FBP_MU_029_Broadway_Transit_Only_Lanes',
               'EXP_Blueprint_NoProject',
               'FBP_AL_067_Rte84Wide',
               'FBP_AL_065_Bancroft_Bus_Only',
               'FBP_SM_032_US101_Willow_Interchange',
               {'name': 'RRSP_Alameda_Point_Transit_Improvements', 'kwargs':{'BUILT':"'built'"},'branch':'PBA50plus_DBP'} # unbuilt portion is in BLUEPRINT_PROJECTS 2025
               ],
        'trn':['ALA050015_BART_to_WarmSprings',
               'ACGo',
               'CC_050025_EBart_to_Antioch',
               'GGTransit_Committed',
               'SCL110005_BART_to_Berryessa',
               'SF_010015_Transbay_Terminal',
               'SF_070027_Yerba_Buena_Ramp_Imp',
               'SOL030002_FairfieldVacaville_Stn',
               'SON090002_SMART',
               'SON090002_SMART_to_Larkspur',
               'CC_070062_Richmond_Ferry',
               'SF_MuniForward_Committed',
               {'name':'VTA_Next',                 'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
               'SCL130001_237_101_MAT_Int_Mod',
               'SonomaCounty_Transit_NoBuild2050',
               'SMART_Novato',
               'Xfare_update_2020',
               'ACTransit_Committed',
               'ferry_update_2019',
               'Napa_Solano_Updates_2020',
               'FBP_Beale_Transit_Only_Lane',
               'SamTrans_ECR_Rapid',
               'ALA150004_EastBay_BRT',
               {'name':'FBP_SL_026_SolExpressBus', 'kwargs':{'MODELYEAR':'2020'}, 'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
               {'name': 'RRSP_Alameda_Point_Transit_Improvements', 'kwargs':{'BUILT':"'built'"},'branch':'PBA50plus_DBP'} # unbuilt portion is in BLUEPRINT_PROJECTS 2025
                ],
    }),
    (2023, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2023'}},
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
               'I880_US101_AdaptiveRampMetering',
               'SOL070020_I80_I680_SR12_Int_1_2A',
               'FBP_NP_036_SR29_Imola_PNR',
               'ALA170052_Fruitvale_Ave_ped_improvements',
               'SF_070005_VanNess_BRT',
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
               'GTFS2023_SF_Muni',
               'GTFS2023_SC_VTA',
               'GTFS2023_AC_ACTransit',
               'GTFS2023_SM_SamTrans',
               'GTFS2023_Other_Operators',
               'MAJ_Treasure_Island_Ferry',
               # Transit_Frequency_Updates_Using_511
               # Update transit frequency for BART and Caltrain using 511 2023-09 data due to big service update in Sept 2023
               # Asana task: https://app.asana.com/0/1204085012544660/1205493838123328/f  
               # Update transit frequency for other operators using 511 2023-05 data 
               # Asana task: https://app.asana.com/0/1204085012544660/1205328142972885/f
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Bay Area Rapid Transit"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Altamont Corridor Express"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Capitol Corridor Joint Powers Authority"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"San Francisco Municipal Transportation Agency"'}},                   
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Caltrain"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"VTA"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Golden Gate Ferry"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"San Francisco Bay Ferry"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"AC TRANSIT"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"SamTrans"'}},
               {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Union City Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Marin Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Tri Delta Transit"'}},  
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Sonoma Marin Area Rail Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Petaluma"'}},  
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"County Connection"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"FAST"'}},
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Golden Gate Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"SolTrans"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"VINE Transit"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Sonoma County Transit"'}},
                # Santa Rosa CityBus implementation isn't used since their GTFS data is inaccurate
                #  https://app.asana.com/0/0/1206596966483061/f
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"WestCat (Western Contra Costa)"'}}, 
#                {'name':'Transit_Frequency_Updates_Using_511', 
#                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
#                          'operator':'"Rio Vista Delta Breeze"'}}, 
#                no model routes for Rio Vista Delta Breeze
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Dumbarton Express Consortium"'}}, 
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Emery Go-Round"'}},
                {'name':'Transit_Frequency_Updates_Using_511', 
                'kwargs':{'regional_gtfs_zip':'r"M:\\Data\\Transit\\511\\2023-09.zip"', 
                          'operator':'"Vacaville City Coach"'}},      
        ]
    }),
    (2025, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2025'}},             
               'ALA150001_I680_SR84_Int_Wid',
               'SOL110006_Jepson_1B_1C',
               'SCL190008_US101_DLC_Int_Imp',
               'CC_170061_Bus_On_Shoulder_680BRT',
               'MAJ_SCL050009_VTA_Eastridge_Extension',
               'MAJ_Geary_BRT_Phase2',
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2025'}},  # This applies for multiple years on the roadway side
               'MRN050034_101_MarinSonNarrows_Phase2',
               'EXP_Blueprint_NoProject',
               'EXP_SL030_I80_RedTopRd_to_I505',
               'EXP_AL025_I680_SR84_to_Alcosta'
               ],
        'trn':['SF_010028_Caltrain_Modernization',
               'SON090002_SMART_to_Windsor',
               'SON090002_SMART_NorthPetaluma',
               'MAJ_SCL050009_VTA_Eastridge_Extension',
               'MAJ_Geary_BRT_Phase2',
               ]
    }),
    (2030, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2030'}},
               {'name':'SF_MuniForward_Committed', 'kwargs':{'MODELYEAR':'2030'}},  # This applies for multiple years on the roadway side
               'EXP_Blueprint_NoProject'],
        'trn':[{'name':'BART_NoProject',             'branch':'PBA50plus_DBP'},
            ]
    }),
    (2035, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2035'}},
               'EXP_Blueprint_NoProject'],
        'trn':[]
    }),
    (2040, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2040'}},
               'EXP_Blueprint_NoProject'],
        'trn':[]
    }),
    (2045, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2045'}},
               'EXP_Blueprint_NoProject'],
        'trn':[]
    }),
    (2050, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2050'}},
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
        (2025, {'hwy':[{'name': 'RRSP_Alameda_Point_Transit_Improvements', 'kwargs':{'BUILT':"'unbuilt'"}, 'branch':'PBA50plus_DBP'},
                       'MAJ_MTC050027_Berkeley_Ferry',
                       'MAJ_WETA_Service_Frequency_Increase',                       
                       {'name':'Transform_SR37_Widening_Interim',                                           'variants_exclude':['Alt1']},
                       {'name':'MAJ_SF_Congestion_Pricing',                                                 'variants_exclude':['NGFNoProjectNoSFCordon', 'NGFround2NoProject']},
                       'FBP_MU_041_Hovercraft_Pilot',
                       {'name':'BP_Vision_Zero',               'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon', 'NGFround2NoProject'], 'DraftBlueprint':True},
                       'EXP_Blueprint',
                       {'name':'MAJ_AC_Frequency_Improvement', 'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       'FBP_MU_044_SouthSF_Ferry_Serv_Incr',
                       'FBP_MU_029_ACRapid_2025',
                       'RRSP_E14_Mission_Corridor',
                       'FBP_MR_026_NovatoWide',
                       'FBP_CC_054_CrowCanyonWide',
                       'FBP_NP_038_TSP_On_SR29',
                       {'name':'FBP_CC_050_SR4_Operation_Improvements_EB',                                  'variants_exclude':['Alt1']},
                       'FBP_NP_044_Soscol_Junction',
                       'FBP_SL_033_FairgroundsWide',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7','kwargs':{'PHASE':"'2B'"}},
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'1'"},  'variants_exclude':['Alt1']},
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'2'"},  'variants_exclude':['Alt1']},
                       {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2025'},              'variants_exclude':['Alt1', 'NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']},
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2025'},           'variants_include':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2025'},              'variants_include':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2025'}},
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2025'}},
                       'FBP_SC_103_MontagueWide', 
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2025'}},
                       'FBP_CC_057_LoneTreeWide',
                       'FBP_CC_063_BrentwoodWide',
                       'FBP_CC_067_WillowPassWide',
                       'FBP_CC_065_LaurelWide',
                       'FBP_AL_062_TassajaraWide',
                       'FBP_SC_039_SR237WBWide',      
                       'FBP_AL_051_7St_Grade_Sep_West',
                       'FBP_AL_044_I880_Whipple_Imps',
                       'FBP_AL_055_DubBlvd_NCanyons_Ext',
                       'FBP_SN_017_Arata_Int',
                       'FBP_CC_017_Brentwood_Intermodal',
                       'FBP_SF_030_Balboa_Park_Area_2',
                       'EXP_Blueprint',
                       'FBP_AL_039_I580_Interchange_Imps',
                       'FBP_CC_056_LaurelExtension',
                       'FBP_SC_084_10th_BridgeWide',
                       'FBP_SL_053_PeabodyWide',
                       'FBP_SC_073_BlossomHill_101Wide',
                       'FBP_SC_082_US101_25_Interchange',
                       'FBP_SM_035_Peninsula_101_OnOffRamps',
                       'FBP_CC_045_SanPabloDam_Interchange_Phase2',
                       'FBP_CC_030_OakleyAmtrak',
                       'STIP_ProduceAve',
                       'FBP_SM_033_US101_Holly_Interchange',
                       'FBP_SM_034_Route92_ElCamino_Interchange',
                       'FBP_SL_019_BeniciaRoad_Diet',
                       'FBP_SL_023_WestTexasRoad_Diet',
                       'FBP_SN_012_PetalumaBlvd_Diet',
                       'MAJ_MissionBay_SF_Ferry',
                       {'name':'EIR2_Val_Link_ExpressBus',                                                'variants_include':['Alt2']},
                       {'name':'EIR2_ReXBlue',                                                            'variants_include':['Alt2']},
                       'FBP_SC_072_US101_Trimble_Interchange',
                       ],
                'trn':['FBP_AL_001_NewarkFremPDA',
                       {'name':'FBP_MU_059_ACTransbay_Freq_Incr',                                         'variants_exclude':['Alt2']},
                       {'name':'MAJ_AC_Frequency_Improvement',                                            'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name': 'RRSP_Alameda_Point_Transit_Improvements',  'kwargs':{'BUILT':"'unbuilt'"},'branch':'PBA50plus_DBP'},
                       'MAJ_MTC050027_Berkeley_Ferry',
                       'MAJ_WETA_Service_Frequency_Increase',
                       {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2025'}},                       
                       {'name':'Transform_SR37_Widening_Interim',                                         'variants_exclude':['Alt1']},
                       {'name':'MAJ_SF_Congestion_Pricing',                                               'variants_exclude':['NGFNoProjectNoSFCordon', 'NGFround2NoProject']},
                       'FBP_MU_041_Hovercraft_Pilot',
                       'FBP_MU_049_Caltrain_6TPHPD',
                       {'name':'FBP_MU_060_ReX_Blue',                                                     'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']},
                       {'name':'EIR2_ReXBlue',                                                            'variants_include':['Alt2']},                       
                       'FBP_MU_044_SouthSF_Ferry_Serv_Incr',
                       {'name':'GGT_Service_Imp',                                                         'branch':'PBA50plus_DBP'},
                       'FBP_MU_029_ACRapid_2025',
                       'RRSP_E14_Mission_Corridor',
                       'FBP_NP_044_Soscol_Junction',
                       'MAJ_RedwoodCity_SF_Ferry',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7','kwargs':{'PHASE':"'2B'"}},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2025'}},
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2025'}},
                       'FBP_CC_030_OakleyAmtrak',
                       'MAJ_MissionBay_SF_Ferry',              
                       {'name':'MAJ_Sonoma_Frequency_Increase',                                           'branch':'PBA50plus_DBP'},
                       {'name':'EIR1_Freq_Boosts',              'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt1']},
                       {'name':'EIR2_HRA_Freq_Incr',            'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt2']},
                       {'name':'EIR2_PDA_Freq_Incr',            'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt2']},
                       {'name':'EIR2_Val_Link_ExpressBus',                                                'variants_include':['Alt2']}
                ]
        }),
        (2030, {'hwy':['MAJ_SanPablo_BRT',
                       {'name':'BP_Tolls_On_Congested_Freeways_2030',                                     'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']},
                       {'name':'BP_Vision_Zero',                                                          'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject'], 'DraftBlueprint':True},
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_exclude':['Alt2']},
                       'FBP_MU_044_Richmond_Ferry_Serv_Incr',
                       'MAJ_REG090037_BART_Core_Cap',
                       {'name':'Transform_Valley_Link',                                                   'variants_exclude':['Alt2']},
                       {'name':'FBP_NP_040_VINE_Exp_Bus_Enhancements',                                    'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       'FBP_AL_045_Oak_Ala_Access_Pr',
                       {'name':'FBP_MR_021_101_580_Direct_Connector',                                     'variants_exclude':['Alt1']},
                       {'name':'FBP_MR_018_US101_BOS',                                                    'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'FBP_CC_036_I80_ExpBus_Impr',                                              'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5','kwargs':{'PHASE':"'4'"}, 'variants_exclude':['Alt1']},
                       'FBP_CC_021_Ant_Mart_Herc_Ferry',
                       {'name':'EXP_uncommitted_all',              'kwargs':{'MODELYEAR':'2030'},         'variants_exclude':['Alt1', 'NGFNoProject', 'NGFNoProjectNoSFCordon', 'NGFround2NoProject']},
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2030'},         'variants_include':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'EIR1_EXP_uncommitted_all',         'kwargs':{'MODELYEAR':'2030'},         'variants_include':['Alt1']},
                       'FBP_SC_104_OaklandWide',
                       {'name':'FBP_CC_15_23rd_St_BRT',            'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',     'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'MAJ_Bay_Area_Forward_all',         'kwargs':{'MODELYEAR':'2030'}},
                       'FBP_CC_064_CaminoTassajaraWide',
                       'FBP_CC_066_CypressWide',
                       'FBP_SC_059_SR237EBWide',
                       'FBP_AL_064_UnionCityWide',
                       'FBP_SC_074_US101_BuenaVista_Int',
                       'EXP_Blueprint',
                       'FBP_SC_054_SR17_Corridor_Relief',
                       'FBP_AL_043_A_StreetWide',
                       'FBP_CC_061_062_West_Leland_Ext_Phases1_2',
                       'FBP_SM_042_Hwy1_ManorDrive',
                       'FBP_SL_042_Jepson_2B_2C',
                       'FBP_CC_024_Oakley_PNR_Tri_Delta',
                       'FBP_SC_083_US101_Zanker_Skyport_Interchange',
                       'FBP_SL_022_SonomaBlvd_Diet',
                       'FBP_SM_027_US101_92',
                       'FBP_SM_007_ElCamino_CompleteStreets',
                    ],
                'trn':[{'name':'BP_PDA_Transit_Enhancements',                                       'branch':'PBA50plus_DBP', 'DraftBlueprint':True},
                       {'name':'FBP_SM_020_Regional_Express_Buses', 'kwargs':{'PHASE':"'Phase1_4Routes'"}},
                       {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2030'}},
                       'MAJ_BRT030001_BART_to_SanJose',
                       'BART_Irvington_Infill',
                       'MAJ_REG090037_BART_Core_Cap',
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_exclude':['Alt2']},
                       'FBP_MU_049_Caltrain_8TPHPD',
                       {'name':'FBP_MU_061_ReX_Green',                                                    'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon', 'NGFround2NoProject']},
                       'MAJ_SanPablo_BRT',
                       'FBP_MU_044_Richmond_Ferry_Serv_Incr',
                       {'name':'Transform_Valley_Link',                                                   'variants_exclude':['Alt2']},
                       'FBP_SF_028_SF_Express_Bus_On_Exp_Lanes',
                       {'name':'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',                             'variants_exclude':['Alt2']},
                       {'name':'FBP_SF_024_Historic_Streetcar_Ext',                                       'branch':'PBA50plus_DBP'},
                       {'name':'FBP_MuniForward_Uncommitted_Rail',                                        'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon'], 'branch':'PBA50plus_DBP'},
                       {'name':'FBP_CC_036_I80_ExpBus_Impr',                                              'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       'FBP_CC_021_Ant_Mart_Herc_Ferry',
                       'FBP_AL_045_Oak_Ala_Access_Pr',
                       'FBP_CC_028_Hercules_Station',
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2030'}},
                       'FBP_CC_024_Oakley_PNR_Tri_Delta',
                       {'name':'EIR1_Freq_Boosts',              'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt1']},
                       {'name':'EIR2_HRA_Freq_Incr',            'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                       {'name':'EIR2_PDA_Freq_Incr',            'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                       {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']}]
        }),
        (2035, {'hwy':[{'name':'MAJ_MuniForward_Uncommitted',                                             'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon'], 'branch':'PBA50plus_DBP'},
                       'MAJ_Treasure_Island_Congestion_Pricing',
                       {'name':'BP_Tolls_On_Congested_Freeways_2035',                                     'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']},
                       {'name':'NGF_BlueprintSegmented',                                                  'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject'], 'DraftBlueprint':True},
                       {'name':'BP_Vision_Zero',                                                          'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject'], 'DraftBlueprint':True},
                       'RRSP_East_West_Connector',
                       {'name':'Transform_I680_Multimodal_Imp',                                           'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       'FBP_SM_022_I380_Widening',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'3'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'4'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'5'"},          'variants_exclude':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',         'kwargs':{'MODELYEAR':'2035'}},
                       {'name':'EXP_uncommitted_all',                  'kwargs':{'MODELYEAR':'2035'},     'variants_exclude':['Alt1', 'NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']},
                       {'name':'EXP_uncommitted_noAllLaneTolling',     'kwargs':{'MODELYEAR':'2035'},     'variants_include':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'EIR1_EXP_uncommitted_all',             'kwargs':{'MODELYEAR':'2035'},     'variants_include':['Alt1']},
                       {'name':'MAJ_Bay_Area_Forward_all',             'kwargs':{'MODELYEAR':'2035'}},
                       'FBP_AL_076_TelegraphDiet',
                       'FBP_SN_018_Cotati_101_RailroadAve_Impr',
                       'FBP_NP_079_Trower_Ext',
                       'EXP_Blueprint',
                       {'name':'EIR1_No_SR37',                                                            'variants_include':['Alt1']},
                       {'name':'NGF_NoProject_tollscsv',                                                  'variants_include':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']}],
                'trn':[{'name':'MAJ_MuniForward_Uncommitted',                                             'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon'], 'branch':'PBA50plus_DBP'},
                       {'name':'FBP_SM_020_Regional_Express_Buses',    'kwargs':{'PHASE':"'Phase2_2Routes'"}},
                       'RRSP_South_East_Waterfront_Transit_Imp',
                       {'name':'FBP_MU_062_ReX_Red',                                                      'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject']},
                       {'name':'Transform_I680_Multimodal_Imp',                                           'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       'Transform_SeamlessTransit',
                       'MAJ_Treasure_Island_Congestion_Pricing',
                       'RRSP_East_West_Connector',
                       'FBP_NP_079_Trower_Ext',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'3'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'4'"},          'variants_exclude':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',         'kwargs':{'MODELYEAR':'2035'}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'5'"},          'variants_exclude':['Alt1']},
                       {'name':'FBP_SL_026_SolExpressBus',             'kwargs':{'MODELYEAR':'2035'},     'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       'FBP_SL_020_MilitaryWest_Diet',
                       {'name':'EIR1_Freq_Boosts',                     'kwargs':{'MODELYEAR':'2035'},     'variants_include':['Alt1']},
                       {'name':'EIR2_VTA_LRT_Orange',                                                     'variants_include':['Alt2']},
                       {'name':'EIR2_Fix_Alt2',                        'kwargs':{'MODELYEAR':'2035'},     'variants_include':['Alt2']},
                       {'name':'EIR1_No_SR37',                                                            'variants_include':['Alt1']}]
        }),
        (2040, {'hwy':[{'name':'BP_Vision_Zero',                                                          'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject'], 'DraftBlueprint':True},
                       'FBP_SC_050_I680_Montague_Int_Imp', 
                       'FBP_MU_029_ACRapid_2040',
                       'FBP_NP_074_SoscolWide',
                       'FBP_CC_059_PittAntiochWide',
                       {'name':'FBP_CC_051_SR4_Operation_Improvements_WB',                                'variants_exclude':['Alt1']},
                       'FBP_CC_037_680_AuxLanes',
                       {'name':'RRSP_EC_Cap_Imp_ECR_Bus',                                                 'branch':'PBA50plus_DBP'},
                       {'name':'MAJ_SR_239',                                                              'variants_exclude':['Alt1']},
                       'FBP_NP_033_Napa_PNR_Lots',
                       'FBP_CC_018_BRT_Brentwood',
                       'FBP_SC_043_I280_Mainline_Impr',
                       'MAJ_ElCaminoReal_BRT',
                       'FBP_AL_042_I680_Stoneridge_Widening',
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'5'"},         'variants_exclude':['Alt1']},
                       {'name':'EXP_uncommitted_all',                            'kwargs':{'MODELYEAR':'2040'},    'variants_exclude':['Alt1', 'NGFNoProject', 'NGFNoProjectNoSFCordon', 'NGFround2NoProject']},
                       {'name':'EXP_uncommitted_noAllLaneTolling',               'kwargs':{'MODELYEAR':'2040'},    'variants_include':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'EIR1_EXP_uncommitted_all',                       'kwargs':{'MODELYEAR':'2040'},    'variants_include':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',                   'kwargs':{'MODELYEAR':'2040'}},
                       {'name':'MAJ_Bay_Area_Forward_all',                       'kwargs':{'MODELYEAR':'2040'}},
                       'FBP_SC_105_SanTomasWide',
                       'FBP_SC_102_CalaverasWide',
                       'FBP_CC_039_Eastbound24Wide',
                       {'name':'FBP_MU_064_SR37_LongTerm',                                               'variants_exclude':['Alt1']},
                       'FBP_SC_094_LawrenceWide',
                       'FBP_NP_066_Newell_Dr',
                       'EXP_Blueprint',
                       'FBP_AL_052_AutoMallWide',
                       'FBP_CC_038_SR242_Clayton_OnOffRamps',
                       'FBP_SC_047_I280_Winchester_OffRamp',
                       'FBP_SC_076_US101_Taylor_Interchange',
                       'FBP_NP_051_Airport_Junction',
                       'FBP_SC_101_BrokawBridgeWide',
                       'FBP_SC_081_US101_SR237',
                       'FBP_SC_088_Envision_Expwy',
                       {'name':'FBP_MU_056_Dumbarton_GRT',                                                'variants_exclude':['Alt2']},
                       {'name':'EIR2_Val_Link_ExpressBus',      'kwargs':{'action':"'revert'"},           'variants_include':['Alt2']},
                       {'name':'Transform_Valley_Link',                                                   'variants_include':['Alt2']},
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_include':['Alt2']},
                       {'name':'Transform_AC_Transbay_Improvements',                                      'variants_include':['Alt2']},
                       'FBP_SC_042_I280_Downtown_Access_Improvements'],
                'trn':[{'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2040'}},
                       'MAJ_Vasona_LRT_Extension',
                       'FBP_MU_029_ACRapid_2040',
                       {'name':'RRSP_EC_Cap_Imp_ECR_Bus',                                                 'branch':'PBA50plus_DBP'},
                       'MAJ_SJC_People_Mover',
                       'FBP_NP_028_NapaVineRegRoutesFrequency',
                       'FBP_NP_034_NapaVineRegExpServiceHrs',
                       'FBP_NP_029_NapaVineLocExpServiceHrs',
                       'FBP_NP_033_Napa_PNR_Lots',
                       'FBP_SC_043_I280_Mainline_Impr',
                       'FBP_CC_018_BRT_Brentwood',
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2040'}},
                       'MAJ_ElCaminoReal_BRT',
                       {'name':'FBP_MU_064_SR37_LongTerm',                                                'variants_exclude':['Alt1']},
                       'FBP_NP_051_Airport_Junction',
                       {'name':'FBP_MU_056_Dumbarton_GRT',                                                'variants_exclude':['Alt2']},
                       'FBP_SC_088_Envision_Expwy',
                       {'name':'HSR',                                                                     'variants_exclude':['Alt2']},
                       {'name':'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',                             'variants_include':['Alt2']},
                       {'name':'EIR2_Val_Link_ExpressBus',      'kwargs':{'action':"'revert'"},           'variants_include':['Alt2']},
                       {'name':'Transform_Valley_Link',                                                   'variants_include':['Alt2']},
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_include':['Alt2']},
                       {'name':'Transform_AC_Transbay_Improvements',                                      'variants_include':['Alt2']},
                       {'name':'EIR2_ReXGreen',                                                           'variants_include':['Alt2']},
                       {'name':'FBP_CC_019_CCCTA_Freq_Increase',                                          'branch':'PBA50plus_DBP'},
                       {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2040'},            'variants_include':['Alt2']}]
        }),
        (2045, {'hwy':[{'name':'BP_Vision_Zero',                                                          'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject'], 'DraftBlueprint':True},
                       {'name':'EXP_uncommitted_all',              'kwargs':{'MODELYEAR':'2045'},         'variants_exclude':['Alt1', 'NGFNoProject', 'NGFNoProjectNoSFCordon', 'NGFround2NoProject']},
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2045'},         'variants_include':['NGFNoProject', 'NGFNoProjectNoSFCordon']},
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2045'},            'variants_include':['Alt1']},
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2045'}},
                       {'name':'FBP_AL_048_SR262_Phase1',                                                 'variants_exclude':['Alt1']},
                       'FBP_NP_045_SR29_Gateway_Impr',
                       'EXP_Blueprint'],
                'trn':[{'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2045'}},
                       'FBP_SC_106_VTA_LRT_Modernization']
        }),
        (2050, {'hwy':[{'name':'BP_Vision_Zero',                                                          'variants_exclude':['NGFNoProject', 'NGFNoProjectNoSFCordon','NGFround2NoProject'], 'DraftBlueprint':True},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'6'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'7'"},          'variants_exclude':['Alt1']},
                       'FBP_SC_028_Stevens_Creek_LRT',
                       {'name':'MAJ_Bay_Area_Forward_all',             'kwargs':{'MODELYEAR':'2050'}},
                       'EXP_Blueprint',
                       'FBP_SC_041_Envision_Highway_Minor',
                       'STIP_ITS_SM',
                       {'name':'BP_Transbay_Crossing',                                                    'variants_exclude':['Alt2']}],
                'trn':[{'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'6'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'7'"},          'variants_exclude':['Alt1']},
                       'FBP_SC_028_Stevens_Creek_LRT',
                       {'name':'BP_Transbay_Crossing',                                                    'variants_exclude':['Alt2']}]
        })
    ])


# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS   = collections.OrderedDict()

# NOTE: SLR is invoked explicitly in build_network_blueprint.py because it requires special handling
# re: backing up the network

for YEAR in COMMITTED_PROJECTS.keys():

    # TODO: PBA50+ DRAFT BLUEPRINT NETWORKS WILL JUST INCLUDE COMMITTED and BLUEPRINT_PROJECTS with 'DraftBlueprint'==True 
    # TODO: When we get to the Final Blueprint stage, we'll bring back a subset of BLUEPRINT_PROJECTS
    if (NET_VARIANT == "Baseline") or (NET_VARIANT == "Blueprint"):
        # baseline: just committed
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn']
        }
        # add projects with 'DraftBlueprint'==True
        if NET_VARIANT == "Blueprint":
            for netmode in ['hwy','trn']:
                for project in BLUEPRINT_PROJECTS[YEAR][netmode]:
                    if not isinstance(project, dict): continue
                    if 'DraftBlueprint' in project.keys() and project ['DraftBlueprint']: 
                        NETWORK_PROJECTS[YEAR][netmode].append(project)
    else:
        # blueprint, alt1, alt2
        if YEAR not in BLUEPRINT_PROJECTS: continue
        NETWORK_PROJECTS[YEAR] = {
            'hwy':COMMITTED_PROJECTS[YEAR]['hwy'] + BLUEPRINT_PROJECTS[YEAR]['hwy'],
            'trn':COMMITTED_PROJECTS[YEAR]['trn'] + BLUEPRINT_PROJECTS[YEAR]['trn']
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
