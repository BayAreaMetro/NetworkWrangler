# Intro

This code has been updated to run on a laptop that has Cube Voyager 6.5.0 installed locally. This is primarily the removal and override of anything that appears to be MTC specific (e.g. paths to cube hostnames and a batch file used when calling runtpp).

Questions can be directed to Andrew Rohne at RSG (andrew.rohne (at) rsginc.com). 9/20/2023.

---
Note: This is still being written! 
---

# Setting Up Cube

The computer's path needs to include the path to Cube Voyager to use an executable there. Follow [these instructions](https://www.computerhope.com/issues/ch000549.htm) for your OS version, add C:\Program Files\Citilabs\CubeVoyager to the path.

To test this, open Anaconda Prompt or Anaconda Powershell and type `runtpp`. There should be an error that says "Error in Arg 1: (null)".

# Setting Up Network Wrangler

This largely follows [the Network Wrangler Documentation](https://github.com/BayAreaMetro/modeling-website/wiki/Network-Building-with-NetworkWrangler#step-4-build-a-network-with-your-project) but is distilled down to something a little more concise.

1. Download the [Anaconda environment](https://github.com/RSGInc/NetworkWrangler/blob/transit_2050/environment_nw.yml) to a location on your hard drive.
2. Created the local Anaconda environment. Open Anaconda Prompt or Anaconda Powershell (either will work, hereinafter referred to as Anaconda Prompt) and type:
    `cd path\you\downloaded\the\above\file\to`
    `conda env create -f environment_nw.yml`
3. Switched to it. Use the following command in the Anaconda prompt
    `conda activate NetworkWrangler`
4. Change directories to an appropriate location on your hard drive.
5. Clone the network Wrangler Repo
    `git clone https://github.com/RSGInc/NetworkWrangler.git`
6. Go into that folder and checkout the transit_2050 branch
    `git checkout transit_2050`
7. Install NetworkWrangler. 
    `cd NetworkWrangler`
    `pip install -e .`
8. Open python, import Wrangler, ensure no errors
9. Get the base network - clone https://github.com/BayAreaMetro/TM1_2015_Base_Network to a local folder (I used C:\Models). This probably should not be done inside the network wrangler folder.
10. Get the projects from Box
    Not-RSG: From https://mtcdrive.box.com/s/unic7tf0sokleacg4fgu0dtu8ixkyfg6
    RSG: I Copied to the files folder to Sharepoint as "04_Network_Work\MTC Data\NetworkProjects_20230719.zip
    I unzipped to C:\Models\TM1_NetworkProjects
11. Also download everything on Box since July 19
    Not-RSG: use box, sort by date, select all necessary
    RSG: Copied to files folder as "04_Network_Work\MTC Data\TM1_NetworkProjects-selected.zip"
12. Set base network env var. Use these commands in an Anaconda prompt:
    `conda env config vars set "TM1_2015_Base_Network=C:\Models\TM1_2015_Base_Network"`
    `conda env config vars set "TM1_NetworkProjects=C:\Models\TM1_NetworkProjects"`
    `conda env config vars set "CUBE_HOST_FILE=C:\Models\NetworkWrangler\HostnamesWithCube.txt"`
    `conda activate NetworkWrangler`
    
    Note: you can test these using `conda env config vars list`
    Note2: Don't forget to reset if you start editing project cards straight from Box.
13. If you wish to use the 'reportDiff' function, you will need to install and activate ArcGIS Pro on your machine. The NetworkWrangler environment already has `arcpy` environment installed with it.
# Running Network Wrangler for the Base Year
1. Be in the correct Anaconda Environment (if not already)
    `conda activate NetworkWrangler`
2. Build the test network
    `python .\build_network_mtc.py Test .\net_spec_test.py`\
   (If 'reportDiff' is desired, add `--create_project_diffs` to the end of the command above.)
    
# Test Project Coding 

The basic version is to add the cards to the TM1_NetworkProjects folder, and then copy the net_spec_test.py script to something a little more descriptive (for the BART San Jose example, I used `net_spec_MAJ_BRT030001_BART_to_SanJose.py`). The script needs to have a project code, scenario (for the purposes of this project, I use `build`)

Run with `python build_network_mtc.py build net_spec_MAJ_BRT030001_BART_to_SanJose.py`

# Adding a Project Card for PPA

Use [build_network_mtc_add_project.py](https://github.com/BayAreaMetro/NetworkWrangler/blob/master/scripts/build_network_mtc_add_project.py) for PPA since only a small number of projects are added (mostly just 1). The base network should be the latest 2050 network in [Sample of L drive Projects Folder](https://mtcdrive.box.com/s/vbpsrs7tpvj1qfxmasink52wls8pexrj), one for each future. The script will automatically use `XXX_17` (latest). In [build_network_mtc_add_project.py](https://github.com/BayAreaMetro/NetworkWrangler/blob/master/scripts/build_network_mtc_add_project.py), point `PPA_DIR` to [Sample of L drive Projects Folder](https://mtcdrive.box.com/s/vbpsrs7tpvj1qfxmasink52wls8pexrj) and `NODE_NAMES` to `TM1_2015_Base_Network\Node Description.xls`.

Required arguments to use the script:

1. Future scenario: one of these three - `CleanAndGreen`, `RisingTides`, and `BackToTheFuture`. `CleanAndGreen` is taken as an example to demonstrate.
2. Input network: `..\Sample of L drive Projects Folder\2050_TM151_PPA_CG_17\INPUT`.
3. Project to be added: one of the projects in `TM1_NetworkProjects`. Take `MAJ_BRT030001_BART_to_SanJose` as an example.
4. Nature of project: `--hwy`, `--trn`, or both.
5. Output: create a separate folder - `..\MTC_Outputs\MAJ_BRT030001_BART_to_SanJose_CG`.
6. `project_short_id`: in this case it's `MAJ_BRT030001_BART_to_SanJose_CG`.

Full example: `python build_network_mtc_add_project.py --trn --input_network "..\Box\Performance and Equity\Project Performance\Sample of L drive Projects Folder\2050_TM151_PPA_CG_17\INPUT" --output_network "..\MTC_Outputs\MAJ_BRT030001_BART_to_SanJose_CG" --create_project_diffs CleanAndGreen MAJ_BRT030001_BART_to_SanJose_CG MAJ_BRT030001_BART_to_SanJose`


## Determine Pre-requisite Projects

# Notes and Errors

## Pre-requisite Projects

If you see this: `WranglerLogger: DEBUG    !!!WARNING!!! Some PRE-REQUISITES were not found or ordered correctly.  Continue anyway? (y/n)`, that means you're missing one or more projects and these projects are required for the project you're using to work. Listed above this, you'll see the pre-requisite projects:

```
WranglerLogger: INFO     Requirement verification - Pre-requisite
WranglerLogger: INFO         Year    Project                                                Pre-requisite Project                              Year
WranglerLogger: INFO     trn 2020.trn.01 MAJ_BRT030001_BART_to_SanJose                      trn ALA050015_BART_to_WarmSprings                      -1
WranglerLogger: INFO     trn 2020.trn.01 MAJ_BRT030001_BART_to_SanJose                      trn SCL110005_BART_to_Berryessa                        -1
```

In this case, it can be fixed by including the prerequisite projects in the appropriate network.
