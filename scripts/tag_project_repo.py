USAGE = """

Tagging Network Project local git repository based on project coding version (e.g. Network scenario).
Example tags: 'PPA', 'dbp', 'STIP', 'PBA50_Blueprint', 'PBA50_NoProject'

Inputs:
    - tag_name: the name of the tag to be added
    - tag_message: the tagging message
    - network_creation_log: log file containing info on which Network Projects should be tagged

Example call:
python tag_project_repo.py "PBA50plus_Blueprint" "version used to build PBA50+ Blueprint Network"  "M:\Application\Model One\RTP2025\INPUT_DEVELOPMENT\Networks\BlueprintNetworks_v35\buildnetwork_Blueprint_Blueprint_2025Apr29.221709.info.LOG"

"""


import git
import pandas as pd
import os, argparse


if __name__ == '__main__':
    
    # NetworkProjects directory, this is where the local repos are located
    username = os.environ['USERNAME']
    networkProjects_folder = 'M:\\Application\\Model One\\NetworkProjects'

    # arguments
    parser = argparse.ArgumentParser(description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument('tag_name', help='name of the tag to be created')
    parser.add_argument('tag_message', help='tagging message')
    parser.add_argument('network_creation_log', help='network creation log listing all projects to be tagged')

    args = parser.parse_args()
    print('tag name: {}'.format(args.tag_name))
    print('tagging message: {}'.format(args.tag_message))
    print('network creation log: {}'.format(args.network_creation_log))


    # Step 1: create a dataframe to store project_name and the commit (SHA1_id) to tag

    projects_df = pd.DataFrame(columns=['project_name', 'SHA1_id'])
    no_SHA1_id_ls = []

    with open(args.network_creation_log) as f:
        log_lines = list(enumerate(f))
        for line_num, line in log_lines:

            # get name of project
            if 'Applying project' in line:
                project_name = line.split("Applying project [project_name='")[1].split("'] [projType=")[0]

                # with NetworkWrangler log file format, the SHA1_id is usually in the next line
                # which also contains the project's name
                next_line = log_lines[line_num+1][1]
                if project_name in next_line:
                    SHA1_id = next_line.split('| '+project_name)[0].split('|')[-1].strip()
                    print('Project: ', project_name, ', SHA1_id: ', SHA1_id)                   
                    # add 'project_name', 'SHA1_id' to the dataframe
                    projects_df.loc[len(projects_df.index)] = [project_name, SHA1_id]
                
                elif project_name not in next_line:
                    if project_name != 'Move_buses_to_HOV_EXP_lanes':
                        print('No SHA1_id in the next line for project: ', project_name)
                        no_SHA1_id_ls.append(project_name)

            elif ('Move_buses_to_HOV_EXP_lanes' in line) & ('Applying project' not in line):
                # this is a special case, where the project name is not in the next line
                # but in the same line, so we need to extract it from the line itself
                SHA1_id = line.split('| Move_buses_to_HOV_EXP_lanes')[0].split('|')[-1].strip()
                print('Special case for project "Move_buses_to_HOV_EXP_lanes": ', SHA1_id)
                # add 'project_name', 'SHA1_id' to the dataframe
                projects_df.loc[len(projects_df.index)] = ['Move_buses_to_HOV_EXP_lanes', SHA1_id]

    no_SHA1_id_ls = list(set(no_SHA1_id_ls))
    print('Projects with no SHA1_id: ', no_SHA1_id_ls)
    
    # drop duplicates
    projects_df.drop_duplicates(inplace=True)
    print('tagging {} projects'.format(projects_df.shape[0]))

    # set project_name as index
    projects_df.set_index('project_name', inplace=True)

    # Step 2: loop through the projects and add tag to the corresponding commit
    cannot_create_tag_ls = []
    no_repo_found_ls = []

    for project in projects_df.index:
        print('Project: ', project)

        # try to open the existing repo
        try:
            repo = git.Repo(os.path.join(networkProjects_folder, project))

            # optional: print out existing tags, sorted by time of creation            
            # existing_tags = sorted(repo.tags, key=lambda t: t.commit.committed_date)
            # print('existing_tags: {}'.format(existing_tags))

            # try creating the tag to the right commit
            commit_ref = repo.commit(projects_df.SHA1_id[project])
            print('commit_reference: {}'.format(commit_ref))
            try:
                print('create tag {} with comment {}'.format(args.tag_name, args.tag_message))
                repo.create_tag(args.tag_name,
                                ref=commit_ref, 
                                message = args.tag_message)

            # if need to delete a tag due to an error, uncomment the next line
            # repo.delete_tag(args.tag_name)

            # if the tag already exists, cannot create, will skip
            except:
                print('cannot create tag "{}"'.format(args.tag_name))

        except:
            print('repo {} doest not exist'.format(project))
            no_repo_found_ls.append(project)

    print('Finished tagging projects.')
    print('Created tag "{}" with message "{}" for {} projects'.format(args.tag_name, args.tag_message, projects_df.shape[0] - len(cannot_create_tag_ls) - len(no_repo_found_ls)))
    print('Cannot create tag for the following projects: ', cannot_create_tag_ls)
    print('No repo found for the following projects: ', no_repo_found_ls)