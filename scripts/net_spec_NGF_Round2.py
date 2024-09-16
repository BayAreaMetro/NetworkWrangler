import os
import collections
# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT  = "NGF"

# MANDATORY. Set this to be the git tag for checking out network projects.
#TAG = "HEAD"               # Use this tag if you want NetworkWrangler to use the latest version in the local repo to build the network
#TAG = "PBA50_Blueprint"    # Use this tag if you want to replicate the network built for PBA50
TAG = "HEAD"

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
# NextGenFwy projects


# Pathways - note these are 2035 projects
NGF_PROJECTS = {

    # Pathway 1: Round 2 All lane tolling
    # https://app.asana.com/0/1203644633064654/1206291041610290/f
    'R2P1_AllLaneTolling':{
        'hwy':[
            'PBA2050_RTP_ID_attributes',
            {'name':'EXP_uncommitted_noAllLaneTolling',     'kwargs':{'MODELYEAR':'2035','PATHWAY':"P5"},     'branch':'master'},
            'NGF_r2_EL_to_HOV2',
            'NGF_r2_ALT_on_All_Fwys',                     # All-Lane-Tolling on All Freeways (fill in any gaps after NGF_BlueprintSegmented)
            'NGF_BlueprintSegmented',
            'NGF_HOV3_to_HOV2',
            'NGF_CarpoolLanes',
            'NGF_r2_BRTonParallelArterials',           # Road Space Reallocation and BRT Improvements on Parallel Arterials
            #'NGF_r2_RemoveSIGCORonParallelArterials',  # Limiting Diversion on Parallel Arterials with SIGCOR Removal   
            #{'name':'BP_Vision_Zero',                                   'branch':'NGF_IncFwyFFS'}, # Speed Limit Reductions
         ],
        'trn':[
            'NGF_NoProject_farefiles',      # ensures these files get included; note this is not a real project
            # Complementary strategy - Transit improvements (frequency boosts for parallel buses, feeder buses, and EPC buses)
            {'name':'NGF_r2_TrnFreqBoosts', 'kwargs':{
                'NoProject_dir' : 'r"L:\\Application\\Model_One\\NextGenFwys_Round2\\Scenarios\\2035_TM160_NGF_r2_NoProject_04\\OUTPUT\\trn"'
            }}
        ]
    },

    # NGF Round 2 pathway 
    # Transit complementary strategy definitions: https://app.asana.com/0/1203644633064654/1208037147689342/f
    'R2P2_MBUF':{
        'hwy':[
            'NGF_r2_BRTonParallelArterials',           # Road Space Reallocation and BRT Improvements on Parallel Arterials
         ],
          'trn':[
            'NGF_NoProject_farefiles',      # ensures these files get included; note this is not a real project
            # Complementary strategy - Transit improvements (frequency boosts for parallel buses, feeder buses, and EPC buses)
            {'name':'NGF_r2_TrnFreqBoosts', 'kwargs':{
                'NoProject_dir' : 'r"L:\\Application\\Model_One\\NextGenFwys_Round2\\Scenarios\\2035_TM160_NGF_r2_NoProject_06\\OUTPUT\\trn"'
            }},
            {'name':'NGF_r2_TrnFreqBoosts_Path2', 'kwargs':{
                'NoProject_dir' : 'r"L:\\Application\\Model_One\\NextGenFwys_Round2\\Scenarios\\2035_TM160_NGF_r2_NoProject_06\\OUTPUT\\trn"'
            }}
        ]
    },

    # Pathway 4: Pathway 4 2035 Express Lanes (would be most similar to Round 1 No New Pricing)
    # https://app.asana.com/0/1203644633064654/1206115787970079/f
    'R2P4_2035_Express_Lanes':{
        'hwy':[
            'PBA2050_RTP_ID_attributes',
            {'name':'EXP_uncommitted_noAllLaneTolling',     'kwargs':{'MODELYEAR':'2035','PATHWAY':"P4"},     'branch':'master'},
         ],
        'trn':[
            'NGF_NoProject_farefiles',      # ensures these files get included; note this is not a real project
        ]
    },
    # Pathway 5: 2035 Express Lanes Conversion Only
    # https://app.asana.com/0/1203644633064654/1206115787970085/f
    'R2P5_Conversion_Only':{
        'hwy':[
            'PBA2050_RTP_ID_attributes',
            {'name':'EXP_uncommitted_noAllLaneTolling',     'kwargs':{'MODELYEAR':'2035','PATHWAY':"P5"},     'branch':'master'},
        ],
        'trn':[
            'NGF_NoProject_farefiles',      # ensures these files get included; note this is not a real project
        ]
    },
    # Pathway 6: 2035 Dual Express Lanes (1 EL lanes if total number of lanes <= 3)
    # https://app.asana.com/0/1203644633064654/1206115787970089/f
    'R2P6_Dual_Express_Lanes':{
        'hwy':[
            'PBA2050_RTP_ID_attributes',
            {'name':'EXP_uncommitted_noAllLaneTolling',     'kwargs':{'MODELYEAR':'2035','PATHWAY':"P6"},     'branch':'master'},
        ],
        'trn':[
            'NGF_NoProject_farefiles',      # ensures these files get included; note this is not a real project
        ]
    },
    
    # Sensitivity test: No Project with local road speed limit reductions 
    # https://app.asana.com/0/1203644633064654/1208321467422880/f
    'R2NP_wFFSreduction':{
        'hwy':[
            {'name':'BP_Vision_Zero',                                   'branch':'NGF_IncFwyFFS'}, # Speed Limit Reductions
         ],
        'trn':[
            'NGF_NoProject_farefiles',      # ensures these files get included; note this is not a real project
        ]
    },
}

# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS   = collections.OrderedDict()

# we're only building 2035
for YEAR in [2035]:

    NETWORK_PROJECTS[YEAR] = {
        'hwy':NGF_PROJECTS[SCENARIO]['hwy'],
        'trn':NGF_PROJECTS[SCENARIO]['trn']
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
