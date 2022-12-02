USAGE = """

Tagging Network Project local git repository based on project coding version (e.g. Network scenario).
Example tags: 'PPA', 'dbp', 'STIP', 'PBA50_Blueprint', 'PBA50_NoProject'

Inputs:
    - tag_name: the name of the tag to be added
    - tag_message: the tagging message
    - network_creation_log: log file containing info on which Network Projects should be tagged

Example call:
python tag_project_repo.py "PBA50_Blueprint" "version used to build PBA50 Blueprint Networks" "M:\\Application\\Model One\\RTP2021\\Blueprint\\INPUT_DEVELOPMENT\\Networks\\BlueprintNetworks_64\\buildnetwork_Blueprint_Blueprint_2021Jul29.170436.info.LOG"
python tag_project_repo.py "PBA50_NoProject" "version used to build PBA50 NoProject Networks" "M:\\Application\\Model One\\RTP2021\\Blueprint\\INPUT_DEVELOPMENT\\Networks\\BlueprintNetworks_62\\buildnetwork_Blueprint_Baseline_2021Jul13.222230.info.LOG"

"""


import git
import pandas as pd
import os, argparse


if __name__ == "__main__":

    # NetworkProjects directory, this is where the local repos are located
    networkProjects_folder = "M:\\Application\\Model One\\NetworkProjects"

    # arguments
    parser = argparse.ArgumentParser(
        description=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("tag_name", help="name of the tag to be created")
    parser.add_argument("tag_message", help="tagging message")
    parser.add_argument(
        "network_creation_log",
        help="network creation log listing all projects to be tagged",
    )

    args = parser.parse_args()
    print("tag name: {}".format(args.tag_name))
    print("tagging message: {}".format(args.tag_message))
    print("network creation log: {}".format(args.network_creation_log))

    # Step 1: create a dataframe to store project_name and the commit (SHA1_id) to tag

    projects_df = pd.DataFrame(columns=["project_name", "SHA1_id"])

    with open(args.network_creation_log) as f:
        log_lines = list(enumerate(f))
        for line_num, line in log_lines:

            # get name of project
            if "Applying project" in line:
                project_name = line.split("] of type")[0].split("Applying project [")[1]
                # print(project_name)

                # with NetworkWrangler log file format, the SHA1_id is usually in the next line
                # which also contains the project's name
                next_line = log_lines[line_num + 1][1]
                if project_name in next_line:
                    SHA1_id = (
                        next_line.split("| " + project_name)[0].split("|")[-1].strip()
                    )
                    # print(SHA1_id)

                    # add 'project_name', 'SHA1_id' to the dataframe
                    projects_df.loc[len(projects_df.index)] = [project_name, SHA1_id]

                elif project_name not in next_line:
                    print("No SHA1_id in the next line for project: ", project_name)

    # manually add SHA1_id for project 'Move_buses_to_HOV_EXP_lanes' which has
    # a different format in the log
    projects_df.loc[len(projects_df.index)] = [
        "Move_buses_to_HOV_EXP_lanes",
        "b8ac63bfe873df1c80e2c8ecd67904ad3970b721",
    ]

    # drop duplicates
    projects_df.drop_duplicates(inplace=True)
    print("tagging {} projects".format(projects_df.shape[0]))

    # set project_name as index
    projects_df.set_index("project_name", inplace=True)

    # Step 2: loop through the projects and add tag to the corresponding commit

    for project in projects_df.index:
        print("Project: ", project)

        # try to open the existing repo
        try:
            repo = git.Repo(os.path.join(networkProjects_folder, project))

            # optional: print out existing tags, sorted by time of creation
            # existing_tags = sorted(repo.tags, key=lambda t: t.commit.committed_date)
            # print('existing_tags: {}'.format(existing_tags))

            # try creating the tag to the right commit
            commit_ref = repo.commit(projects_df.SHA1_id[project])
            print("commit_reference: {}".format(commit_ref))
            try:
                print(
                    "create tag {} with comment {}".format(
                        args.tag_name, args.tag_message
                    )
                )
                repo.create_tag(args.tag_name, ref=commit_ref, message=args.tag_message)

            # if the tag already exists, cannot create, will skip
            except:
                print('cannot create tag "{}"'.format(args.tag_name))

        except:
            print("repo {} doest not exist".format(project))
