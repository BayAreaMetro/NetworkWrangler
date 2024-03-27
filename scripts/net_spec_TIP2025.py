import os

# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT = "TIP2023"

# MANDATORY. Set this to be the Scenario Name e.g. "NoProject","Project"
# for TIP2023, we only have to build the Project network
SCENARIO = "Project"

# MANDATORY. Set this to be the git tag for checking out network projects.
TAG = "TIP_2023"

# MANDATORY. Set this to the directory in which to write your outputs.
# "hwy" and "trn" subdirectories will be created here.
#OUT_DIR = PROJECT + "_" + SCENARIO + "_network_{}"  # YEAR
OUT_DIR = PROJECT + "_" + "_network_{}"  # YEAR

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
               'SF_070005_VanNess_BRT',
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
               'SF_MuniForward_Committed',
               'FBP_MU_029_Broadway_Transit_Only_Lanes',
               'EXP_Blueprint_NoProject',
               'FBP_AL_067_Rte84Wide',
               'FBP_AL_065_Bancroft_Bus_Only',
               'FBP_SM_032_US101_Willow_Interchange'],
        'trn':['ALA050015_BART_to_WarmSprings',
               'ACGo',
               'CC_050025_EBart_to_Antioch',
               'GGTransit_Committed',
               'SCL110005_BART_to_Berryessa',
               'SF_010015_Transbay_Terminal',
               'SF_010037_Muni_Central_Subway',
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
               'Napa_Solano_Updates_2020',
               'FBP_Beale_Transit_Only_Lane',
               'SamTrans_ECR_Rapid',
               'ALA150004_EastBay_BRT',
               {'name':'FBP_SL_026_SolExpressBus', 'kwargs':{'MODELYEAR':'2020'}}],
    }),
    (2025, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2025'}},
               'EXP_CC_050028_I680_SB_HOV_Completion',
               'EXP_101B1',
               'EXP_101B2',
               'EXP_680C1',
               'EXP_680F',
               'EXP_85D',
               'EXP_101C',
               'ALA150001_I680_SR84_Int_Wid',
               'ALA150043_Claremont_road_diet',
               'CC_070009_Slatten_Ranch_Rd_Extension',
               'SF_070004_Geary_BRT_Phase1',
               'SON070004_101_MarinSonNarrows_Phase2',
               'SOL110006_Jepson_1B_1C',
               'SCL190008_US101_DLC_Int_Imp',
               'I880_US101_AdaptiveRampMetering',
               'SOL070020_I80_I680_SR12_Int_1_2A',
               'FBP_NP_036_SR29_Imola_PNR',
               'ALA170052_Fruitvale_Ave_ped_improvements',
               'EXP_Blueprint_NoProject'],
        'trn':['SF_010028_Caltrain_Modernization',
               'REG090037_New_BART_Trains',
               'FBP_NP_036_SR29_Imola_PNR',
               'SOL070020_I80_I680_SR12_Int_1_2A']
    }),
    (2030, {
        'hwy':[{'name':'Bridge_Toll_Updates_2_2pct', 'kwargs':{'MODELYEAR':'2030'}},
               'EXP_Blueprint_NoProject'],
        'trn':['BART_NoProject',
               'SON090002_SMART_to_Windsor'],
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
# TIP projects
TIP_PROJECTS = collections.OrderedDict([
        (2015, {'hwy':[],
                'trn':[]
        }),
        (2020, {'hwy':[],
                'trn':[]
        }),
        (2025, {'hwy':[{'name':'RRSP_Alameda_Point_Transit_Improvements',                                   'tag':'PBA50_Blueprint'},
                       'MAJ_MTC050027_Berkeley_Ferry',
                       'MAJ_WETA_Service_Frequency_Increase',                       
                       'FBP_MU_041_Hovercraft_Pilot',
                       'BP_Vision_Zero',
                       'EXP_Blueprint',
                       'MAJ_AC_Frequency_Improvement',
                       'MRN050034_101_MarinSonNarrows_Phase2',
                       'FBP_MU_044_SouthSF_Ferry_Serv_Incr',
                       'FBP_MU_029_ACRapid_2025',
                       'RRSP_E14_Mission_Corridor',
                       'FBP_MR_026_NovatoWide',
                       'FBP_NP_038_TSP_On_SR29',
                       'FBP_NP_044_Soscol_Junction',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7','kwargs':{'PHASE':"'2B'"}},
                       {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2025'},              'variants_exclude':['Alt1', 'NextGenFwy']},
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2025'},              'variants_include':['Alt1']},
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2025'}},
                       'FBP_CC_057_LoneTreeWide',
                       'FBP_CC_067_WillowPassWide',
                       'FBP_CC_065_LaurelWide',
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
                       'FBP_CC_045_SanPabloDam_Interchange_Phase2',
                       'FBP_CC_030_OakleyAmtrak',
                       'FBP_SM_034_Route92_ElCamino_Interchange',
                       'FBP_SL_019_BeniciaRoad_Diet',
                       'FBP_SL_023_WestTexasRoad_Diet',
                       'FBP_SN_012_PetalumaBlvd_Diet',
                       'SF_Park_Presidio_HOV_Pilot',
                       'SF_Lombard_HOV_Pilot',
                       {'name':'EIR2_Val_Link_ExpressBus',                                                'variants_include':['Alt2']},
                       {'name':'EIR2_ReXBlue',                                                            'variants_include':['Alt2']},
                       'FBP_SC_072_US101_Trimble_Interchange',
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2025'},         'variants_include':['NextGenFwy']}],
                'trn':['FBP_AL_001_NewarkFremPDA',
                       {'name':'FBP_MU_059_ACTransbay_Freq_Incr',                                         'variants_exclude':['Alt2']},
                       'MAJ_AC_Frequency_Improvement',
                       {'name':'RRSP_Alameda_Point_Transit_Improvements',                                 'tag':'PBA50_Blueprint'},
                       'MAJ_MTC050027_Berkeley_Ferry',
                       'MAJ_WETA_Service_Frequency_Increase',
                       {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2025'}},                       
                       'FBP_MU_041_Hovercraft_Pilot',
                       'FBP_MU_049_Caltrain_6TPHPD',
                       {'name':'FBP_MU_060_ReX_Blue',                                                     'variants_exclude':['Alt2']},
                       {'name':'EIR2_ReXBlue',                                                            'variants_include':['Alt2']},                       
                       'FBP_MU_044_SouthSF_Ferry_Serv_Incr',
                       'GGT_Service_Imp',
                       'FBP_MU_029_ACRapid_2025',
                       'RRSP_E14_Mission_Corridor',
                       'FBP_NP_044_Soscol_Junction',
                       'MAJ_Alameda_Point_SF_Ferry',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7','kwargs':{'PHASE':"'2B'"}},
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2025'}},
                       'FBP_CC_030_OakleyAmtrak',          
                       'MAJ_Sonoma_Frequency_Increase',
                       {'name':'EIR1_Freq_Boosts',              'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt1']},
                       {'name':'EIR2_HRA_Freq_Incr',            'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt2']},
                       {'name':'EIR2_PDA_Freq_Incr',            'kwargs':{'MODELYEAR':'2025'},            'variants_include':['Alt2']},
                       {'name':'EIR2_Val_Link_ExpressBus',                                                'variants_include':['Alt2']}]
        }),
        (2030, {'hwy':['MAJ_SanPablo_BRT',
                       'SF_070027_Yerba_Buena_Ramp_Imp',
                       'CC_170061_Bus_On_Shoulder_680BRT',
                       'BP_Vision_Zero',
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_exclude':['Alt2']},
                       'FBP_MU_044_Richmond_Ferry_Serv_Incr',
                       'MAJ_REG090037_BART_Core_Cap',
                       {'name':'Transform_Valley_Link',                                                   'variants_exclude':['Alt2']},
                       'FBP_NP_040_VINE_Exp_Bus_Enhancements',
                       'FBP_AL_045_Oak_Ala_Access_Pr',
                     #  'FBP_MR_018_US101_BOS',
                       'FBP_CC_036_I80_ExpBus_Impr',
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5','kwargs':{'PHASE':"'4'"}, 'variants_exclude':['Alt1']},
                       'FBP_CC_021_Ant_Mart_Herc_Ferry',
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt1']},
                       'FBP_SC_104_OaklandWide',
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'BP_Tolls_On_Congested_Freeways_2030',                                     'variants_exclude':['NextGenFwy']},
                       {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2030'},            'variants_exclude':['Alt1', 'NextGenFwy']},
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
                       'FBP_AL_044_I880_Whipple_Imps',
                       'ALA110002_I880_Industrial_Interchange',
                       'FBP_AL_051_7St_Grade_Sep_West',
                       'FBP_AL_055_DubBlvd_NCanyons_Ext',
                       'FBP_AL_062_TassajaraWide',
                       'ALA090020_I880_Industrial_Parkway_AuxLanes',
                       'FBP_CC_063_BrentwoodWide',
                       'FBP_CC_054_CrowCanyonWide',
                       'MAJ_Geary_BRT_Phase2',
                       'MAJ_SF_Congestion_Pricing',
                       'MAJ_MissionBay_SF_Ferry',
                       'FBP_SM_033_US101_Holly_Interchange',
                       'FBP_SM_035_Peninsula_101_OnOffRamps',
                       'STIP_ProduceAve',
                       'MAJ_SCL050009_VTA_Eastridge_Extension',
                       'FBP_SC_103_MontagueWide',
                       'FBP_SL_033_FairgroundsWide',
                       'ALA_Fallon_Realign',
                       'ALA210027_180_Powell_Transit_Access',
                       'ALA210028_I80_HOV_Bus_Lane_Ext',
                       'SCL210026_Julian_James_Conversion',
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'1'"},  'variants_exclude':['Alt1']},
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'2'"},  'variants_exclude':['Alt1']},
                       {'name':'FBP_CC_050_SR4_Operation_Improvements_EB',                                  'variants_exclude':['Alt1']},
                       {'name':'FBP_CC_051_SR4_Operation_Improvements_WB',                                  'variants_exclude':['Alt1']},
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2030'},         'variants_include':['NextGenFwy']},
                       {'name':'Transform_SR37_Widening_Interim',                                           'variants_exclude':['Alt1']}],
                'trn':['BP_PDA_Transit_Enhancements',
                       'SF_070027_Yerba_Buena_Ramp_Imp',
                       {'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2030'}},
                       'BART_Irvington_Infill',
                       'MAJ_REG090037_BART_Core_Cap',
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_exclude':['Alt2']},
                       'FBP_MU_049_Caltrain_8TPHPD',
                       'FBP_MU_061_ReX_Green',
                       'MAJ_SanPablo_BRT',
                       'FBP_MU_044_Richmond_Ferry_Serv_Incr',
                       {'name':'Transform_Valley_Link',                                                  'variants_exclude':['Alt2']},
                       'FBP_SF_028_SF_Express_Bus_On_Exp_Lanes',
                       {'name':'MAJ_SF_050002_Caltrain_Ext_TransbayTerminal',                             'variants_exclude':['Alt2']},
                       'FBP_SF_024_Historic_Streetcar_Ext',
                       'FBP_MuniForward_Uncommitted_Rail',
                       'FBP_CC_036_I80_ExpBus_Impr',
                       'FBP_CC_021_Ant_Mart_Herc_Ferry',
                       'FBP_AL_045_Oak_Ala_Access_Pr',
                       'FBP_CC_028_Hercules_Station',
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2030'}},
                       {'name':'FBP_CC_15_23rd_St_BRT',         'kwargs':{'MODELYEAR':'2030'}},
                       'FBP_CC_024_Oakley_PNR_Tri_Delta',
                       'MAJ_Geary_BRT_Phase2',
                       'MAJ_SF_Congestion_Pricing',
                       'MAJ_MissionBay_SF_Ferry',
                       'MAJ_RedwoodCity_SF_Ferry',
                       'MAJ_SCL050009_VTA_Eastridge_Extension',
                       {'name':'FBP_SM_020_Regional_Express_Buses', 'kwargs':{'PHASE':"'Phase1_4Routes'"}},
                       {'name':'EIR1_Freq_Boosts',              'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt1']},
                       {'name':'EIR2_HRA_Freq_Incr',            'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                       {'name':'EIR2_PDA_Freq_Incr',            'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                       {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2030'},            'variants_include':['Alt2']},
                       {'name':'Transform_SR37_Widening_Interim',                                         'variants_exclude':['Alt1']},
                       {'name':'SON090002_SMART_NorthPetaluma',                                           'variants_exclude':['Baseline']}]
        }),
        (2035, {'hwy':['MAJ_MuniForward_Uncommitted',
                       'MAJ_Treasure_Island_Congestion_Pricing',
                       'BP_Vision_Zero',
                       'RRSP_East_West_Connector',
                       'Transform_I680_Multimodal_Imp',
                       'FBP_SM_022_I380_Widening',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'3'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'4'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'5'"},          'variants_exclude':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2035'}},
                       {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2035'},            'variants_exclude':['Alt1', 'NextGenFwy']},
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2035'},            'variants_include':['Alt1']},
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2035'}},
                       {'name':'BP_Tolls_On_Congested_Freeways_2035',                                     'variants_exclude':['NextGenFwy']},
                       'FBP_AL_076_TelegraphDiet',
                       'FBP_SN_018_Cotati_101_RailroadAve_Impr',
                       'FBP_NP_079_Trower_Ext',
                       'EXP_Blueprint',
                       {'name':'EIR1_No_SR37',                                                            'variants_include':['Alt1']},
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2035'},         'variants_include':['NextGenFwy']}],
                'trn':['MAJ_MuniForward_Uncommitted',
                       'RRSP_South_East_Waterfront_Transit_Imp',
                       'FBP_MU_062_ReX_Red',
                       'Transform_I680_Multimodal_Imp',
                       'Transform_SeamlessTransit',
                       'MAJ_Treasure_Island_Congestion_Pricing',
                       'RRSP_East_West_Connector',
                       'MAJ_Treasure_Island_Ferry',
                       'FBP_NP_079_Trower_Ext',
                       {'name':'FBP_SM_020_Regional_Express_Buses', 'kwargs':{'PHASE':"'Phase2_2Routes'"}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'3'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'4'"},          'variants_exclude':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2035'}},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'5'"},          'variants_exclude':['Alt1']},
                       {'name':'FBP_SL_026_SolExpressBus', 'kwargs':{'MODELYEAR':'2035'}},
                       'FBP_SL_020_MilitaryWest_Diet',
                       {'name':'EIR1_Freq_Boosts', 'kwargs':{'MODELYEAR':'2035'},                         'variants_include':['Alt1']},
                       {'name':'EIR2_VTA_LRT_Orange',                                                     'variants_include':['Alt2']},
                       {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2035'},            'variants_include':['Alt2']},
                       {'name':'EIR1_No_SR37',                                                            'variants_include':['Alt1']}]
        }),
        (2040, {'hwy':['BP_Vision_Zero',
                       'FBP_SC_050_I680_Montague_Int_Imp', 
                       'FBP_MU_029_ACRapid_2040',
                       'FBP_NP_074_SoscolWide',
                       'FBP_CC_059_PittAntiochWide',
                       {'name':'FBP_CC_051_SR4_Operation_Improvements_WB',                                'variants_exclude':['Alt1']},
                       'FBP_CC_037_680_AuxLanes',
                       'RRSP_EC_Cap_Imp_ECR_Bus',
                       {'name':'MAJ_SR_239',                                                              'variants_exclude':['Alt1']},
                       'FBP_NP_033_Napa_PNR_Lots',
                       'FBP_CC_018_BRT_Brentwood',
                       'FBP_SC_043_I280_Mainline_Impr',
                       'MAJ_ElCaminoReal_BRT',
                       'FBP_AL_042_I680_Stoneridge_Widening',
                       {'name':'FBP_CC_040_041_042_I680_SR4_Int_Phases_1_2_4_5', 'kwargs':{'PHASE':"'5'"},'variants_exclude':['Alt1']},
                       {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2040'},            'variants_exclude':['Alt1', 'NextGenFwy']},
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2040'},            'variants_include':['Alt1']},
                       {'name':'FBP_SF_012_Geneva_Harney_BRT',  'kwargs':{'MODELYEAR':'2040'}},
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2040'}},
                       'FBP_SC_105_SanTomasWide',
                       'FBP_SC_102_CalaverasWide',
                       'FBP_CC_039_Eastbound24Wide',
                       {'name':'FBP_MU_064_SR37_LongTerm',                                                'variants_exclude':['Alt1']},
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
                       'FBP_SC_039_SR237WBWide',
                       {'name':'FBP_MR_021_101_580_Direct_Connector',                                     'variants_exclude':['Alt1']},
                       {'name':'FBP_MU_056_Dumbarton_GRT',                                                'variants_exclude':['Alt2']},
                       {'name':'EIR2_Val_Link_ExpressBus',      'kwargs':{'action':"'revert'"},           'variants_include':['Alt2']},
                       {'name':'Transform_Valley_Link',                                                   'variants_include':['Alt2']},
                       {'name':'FBP_AL_021_South_Bay_Connect',                                            'variants_include':['Alt2']},
                       {'name':'Transform_AC_Transbay_Improvements',                                      'variants_include':['Alt2']},
                       'FBP_SC_042_I280_Downtown_Access_Improvements',
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2040'},         'variants_include':['NextGenFwy']}],
                'trn':[{'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2040'}},
                       'MAJ_BRT030001_BART_to_SanJose',
                       'MAJ_Vasona_LRT_Extension',
                       'FBP_MU_029_ACRapid_2040',
                       'RRSP_EC_Cap_Imp_ECR_Bus',
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
                       'FBP_CC_019_CCCTA_Freq_Increase',
                       {'name':'EIR2_Fix_Alt2',                 'kwargs':{'MODELYEAR':'2040'},            'variants_include':['Alt2']}]
        }),
        (2045, {'hwy':['BP_Vision_Zero',
                       {'name':'EXP_uncommitted_all',           'kwargs':{'MODELYEAR':'2045'},            'variants_exclude':['Alt1', 'NextGenFwy']},
                       {'name':'EIR1_EXP_uncommitted_all',      'kwargs':{'MODELYEAR':'2045'},            'variants_include':['Alt1']},
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2045'}},
                       {'name':'FBP_AL_048_SR262_Phase1',                                                 'variants_exclude':['Alt1']},
                       'FBP_NP_045_SR29_Gateway_Impr',
                       'EXP_Blueprint',
                       {'name':'EXP_uncommitted_noAllLaneTolling', 'kwargs':{'MODELYEAR':'2045'},         'variants_include':['NextGenFwy']}],
                'trn':[{'name':'FBP_MU_046_ACE_Freq_Inc',       'kwargs':{'MODELYEAR':'2045'}},
                       'FBP_SC_106_VTA_LRT_Modernization']
        }),
        (2050, {'hwy':['BP_Vision_Zero',
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'6'"},          'variants_exclude':['Alt1']},
                       {'name':'MAJ_SOL070020_I80_I680_SR12_Int_2B_7', 'kwargs':{'PHASE':"'7'"},          'variants_exclude':['Alt1']},
                       'FBP_SC_028_Stevens_Creek_LRT',
                       {'name':'MAJ_Bay_Area_Forward_all',      'kwargs':{'MODELYEAR':'2050'}},
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
