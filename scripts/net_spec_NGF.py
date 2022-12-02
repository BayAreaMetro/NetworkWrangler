import os
import collections

# MANDATORY. Set this to be the Project Name.
# e.g. "RTP2021", "TIP2021", etc
PROJECT = "NGF"

# MANDATORY. Set this to be the git tag for checking out network projects.
# TAG = "HEAD"               # Use this tag if you want NetworkWrangler to use the latest version in the local repo to build the network
# TAG = "PBA50_Blueprint"    # Use this tag if you want to replicate the network built for PBA50
TAG = "HEAD"

# A Alamedaproject can either be a simple string, or it can be
# a dictionary with with keys 'name', 'tag' (optional), and 'kwargs' (optional)
# to specify a special tag or special keyword args for the projects apply() call.
# For example:
#     {'name':"Muni_TEP", 'kwargs':{'servicePlan':"'2012oct'"}}
###########################################################
COMMITTED_PROJECTS = collections.OrderedDict(
    [
        (2015, {"hwy": [], "trn": []}),
        (
            2020,
            {
                "hwy": [],
                "trn": [],
            },
        ),
        (2025, {"hwy": [], "trn": []}),
        (2030, {"hwy": [], "trn": []}),
        (2035, {"hwy": [], "trn": []}),
    ]
)

###########################################################
# Blueprint projects
BLUEPRINT_PROJECTS = collections.OrderedDict(
    [
        (2015, {"hwy": [], "trn": []}),
        (2020, {"hwy": [], "trn": []}),
        (2025, {"hwy": ["BP_Vision_Zero"], "trn": []}),
        (2030, {"hwy": [], "trn": []}),
        (
            2035,
            {
                "hwy": [],
                "trn": [
                    {
                        "name": "EIR1_Freq_Boosts",
                        "kwargs": {"MODELYEAR": "2035"},
                        "variants_include": ["Mock"],
                    }
                ],
            },
        ),
    ]
)

###########################################################
# NextGenFwy projects
NGF_PROJECTS = collections.OrderedDict(
    [
        (2015, {"hwy": [], "trn": []}),
        (2020, {"hwy": [], "trn": []}),
        (2025, {"hwy": [], "trn": []}),
        (2030, {"hwy": [], "trn": []}),
        (
            2035,
            {
                "hwy": [
                    {
                        "name": "NGF_NoProject_farefiles",
                        "variants_include": ["BlueprintSegmented"],
                    },
                    {
                        "name": "NGF_BlueprintSegmented",
                        "variants_include": ["BlueprintSegmented"],
                    },
                ],
                "trn": [],
            },
        ),
    ]
)

# Put them together for NETWORK_PROJECTS
NETWORK_PROJECTS = collections.OrderedDict()

for YEAR in COMMITTED_PROJECTS.keys():

    NETWORK_PROJECTS[YEAR] = {
        "hwy": COMMITTED_PROJECTS[YEAR]["hwy"]
        + BLUEPRINT_PROJECTS[YEAR]["hwy"]
        + NGF_PROJECTS[YEAR]["hwy"],
        "trn": COMMITTED_PROJECTS[YEAR]["trn"]
        + BLUEPRINT_PROJECTS[YEAR]["trn"]
        + NGF_PROJECTS[YEAR]["trn"],
    }
    # handle net_remove, nets keywords
    for netmode in ["hwy", "trn"]:

        # iterate backwards via index to delete cleanly
        for project_idx in range(len(NETWORK_PROJECTS[YEAR][netmode]) - 1, -1, -1):
            project = NETWORK_PROJECTS[YEAR][netmode][project_idx]
            # special handling requires project to be specified as dictionary
            if not isinstance(project, dict):
                continue

            # variants_exclude: specifies list of network variants for which this project should be *excluded*
            if (
                "variants_exclude" in project.keys()
                and NET_VARIANT in project["variants_exclude"]
            ):
                Wrangler.WranglerLogger.info(
                    "Removing {} {} {}".format(YEAR, netmode, project)
                )
                del NETWORK_PROJECTS[YEAR][netmode][project_idx]
                continue

            # variants_include: specifies list of network variants for which this project should be *included*
            # if this keyword is present, then this project is included *only* for variants in this list
            if (
                "variants_include" in project.keys()
                and NET_VARIANT not in project["variants_include"]
            ):
                Wrangler.WranglerLogger.info(
                    "Removing {} {} {}".format(YEAR, netmode, project)
                )
                del NETWORK_PROJECTS[YEAR][netmode][project_idx]
                continue

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
