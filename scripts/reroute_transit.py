USAGE="""

Modify transit affected by SLR flooding. Including:
- if called with transit_option == bus, reroute/remove bus segments that are flooded. 
- if called with transit_option == rail, create bus shuttle services for rail lines with partial shutdown to connect the remaining segments.

"""
import geopandas as gpd
import pandas as pd
import momepy
import networkx as nx
import os, logging, datetime, argparse


def get_unflooded_network(link_del_df, links_gdf, trn_links_gdf, trn_stops_gdf, year):
    """
    Give transportation network (roadway links, transit links, transit stops) and SLR flooding link tag (roadway links to be flooded),
    create the following files:
        - unflooded_links: roadway links remain unflooded; used for generating a graph to reroute bus / create shuttle
        - links_on_flooded_lines: links of all bus lines affected by roadway flooding; to be rerouted
        - unflooded_trn_stops: transit stops not flooded; used for creating shuttle services for rail. 
    """

    ## get unflooded roadway links
    links_floodingtag = pd.merge(
        links_gdf,
        link_del_df,
        on=['A', 'B'],
        how='left'
    )
    
    # links available for rerouting transit: not dummy links & not flooded
    unflooded_links = links_floodingtag.loc[
        (links_floodingtag['FT'] != 6) & (links_floodingtag['DEL'] != 1)
    ]
    num_of_nodes = len(list(set(list(unflooded_links['A']) + list(unflooded_links['B']))))
    logging.info('{} TM1 links and {} nodes remain unflooded, available for rerouting'.format(
        len(unflooded_links), num_of_nodes))

    ## get transit links on lines affected by flooded (partial flooding)
    # add flooding/deleting tag
    trn_links_gdf_floodtagging = pd.merge(
        trn_links_gdf,
        link_del_df,
        on=['A', 'B'],
        how='left'
    )
    # print(len(trn_links_gdf_floodtagging))

    # lines affected by flooding
    flooded_lines = trn_links_gdf_floodtagging.loc[trn_links_gdf_floodtagging['DEL'] == 1]['NAME'].unique()
    logging.info('{} bus lines are affected by flooding: \n{}'.format(len(flooded_lines), sorted(flooded_lines)))

    # all links on lines affected by flooding
    links_on_flooded_lines = trn_links_gdf_floodtagging.loc[trn_links_gdf_floodtagging['NAME'].isin(flooded_lines)]
    links_on_flooded_lines['A-B'] = links_on_flooded_lines['A'].astype(str) + '-' + links_on_flooded_lines['B'].astype(str)
    links_on_flooded_lines['DEL'].fillna(0, inplace=True)

    # for QAQC: get a summary table
    flood_tag_ls = links_on_flooded_lines.sort_values(
        ['NAME', 'SEQ']).groupby(['NAME'])['DEL'].apply(list)
    link_ls = links_on_flooded_lines.sort_values(
        ['NAME', 'SEQ']).groupby(['NAME'])['A-B'].apply(list)
    # merge, to generate a link and flooding tag lookup by line
    lines_to_modify = pd.concat([flood_tag_ls, link_ls], axis=1).reset_index()
    lines_to_modify_qaqc_file = os.path.join(QAQC_DIR, 'bus_lines_affected_by_flooding_{}.csv'.format(year))
    logging.info('{} bus lines need modification, write out to {}'.format(len(lines_to_modify), lines_to_modify_qaqc_file))
    # write out
    lines_to_modify.to_csv(lines_to_modify_qaqc_file, index=False)    
    
    ## get unflooded transit stops
    
    unflooded_trn_links = trn_links_gdf_floodtagging.loc[trn_links_gdf_floodtagging['DEL'] != 1]

    # get A/B nodes of transit links
    unflooded_trn_nodes = pd.concat([
        unflooded_trn_links[['A']].rename({'A': 'N'}, axis=1), 
        unflooded_trn_links[['B']].rename({'B': 'N'}, axis=1)
        ])
    unflooded_trn_nodes.drop_duplicates(inplace=True)
    unflooded_trn_nodes['node_good'] = 1
    logging.debug('{} nodes remain on unflooded transit links'.format(unflooded_trn_nodes.shape[0]))

    # tag stops
    unflooded_trn_stops = pd.merge(
        trn_stops_gdf,
        unflooded_trn_nodes,
        on='N',
        how='left'
    )
    # only keep unflooded
    unflooded_trn_stops = unflooded_trn_stops.loc[unflooded_trn_stops['node_good'] == 1]

    logging.info('{} transit line+stops remain unflooded'.format(len(unflooded_trn_stops)))

    return unflooded_links, links_on_flooded_lines, unflooded_trn_stops



def build_graph(TM1_links_gdf):
    """
    Build a graph from the links available - links not flooded - for rerouting.

    """
    
    G = momepy.gdf_to_nx(TM1_links_gdf, approach="primal", directed=True, preserve_index=True)

    num_edges = len(list(G.edges(data=True)))
    num_nodes = len(list(G.nodes(data=True)))
    logging.debug('Graph has {} nodes and {} edges'.format(num_nodes, num_edges))

    # step 2: build a dictionary from TM1 network nodes to Graph nodes
    TM1_nodes_G_nodes_dict_A = dict(zip([i[2]['A'] for i in list(G.edges(data=True))], [i[0] for i in list(G.edges(data=True))]))
    TM1_nodes_G_nodes_dict_B = dict(zip([i[2]['B'] for i in list(G.edges(data=True))], [i[1] for i in list(G.edges(data=True))]))
    # print(len(TM1_nodes_G_nodes_dict_A))
    # print(len(TM1_nodes_G_nodes_dict_B))

    def Merge(dict1, dict2): 
        res = dict1 | dict2
        return res

    TM1_nodes_G_nodes_dict = Merge(TM1_nodes_G_nodes_dict_A, TM1_nodes_G_nodes_dict_B)
    logging.debug('TM1_nodes_G_nodes_dict has length {}'.format(len(TM1_nodes_G_nodes_dict)))
    logging.debug(TM1_nodes_G_nodes_dict)

    return G, TM1_nodes_G_nodes_dict


def get_line_segments_to_reroute(line_to_be_rerouted):
    """
    For a line that is affected and needs rerouting, get all the segments that need rerouting.
    A line could have more than one segments that need rerouting.
    
    """

    to_reroute = []
    to_reroute_part = []
    i = 1
    pre_del = 0

    while i <= line_to_be_rerouted['SEQ'].max():
        if ((pre_del == 0) & (line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'DEL'].iloc[0] == 0)):    
            i += 1
        elif ((pre_del == 0) & (line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'DEL'].iloc[0] == 1) & (i < line_to_be_rerouted['SEQ'].max())):
            to_reroute_part.append(
                [
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'A'].iloc[0],
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'B'].iloc[0]])
            pre_del = 1
            i += 1
        elif ((pre_del == 0) & (line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'DEL'].iloc[0] == 1) & (i == line_to_be_rerouted['SEQ'].max())):
            to_reroute_part.append(
                [
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'A'].iloc[0],
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'B'].iloc[0]])
            to_reroute.append(to_reroute_part)
            pre_del = 1
            i += 1
        elif ((pre_del == 1) & (line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'DEL'].iloc[0] == 0)):
            to_reroute.append(to_reroute_part)
            to_reroute_part = []
            pre_del = 0
            i += 1
            # pre_del = 1
        elif ((pre_del == 1) & (line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'DEL'].iloc[0] == 1) & (i < line_to_be_rerouted['SEQ'].max())):
            to_reroute_part.append(
                [
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'A'].iloc[0],
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'B'].iloc[0]])
            i += 1
        elif ((pre_del == 1) & (line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'DEL'].iloc[0] == 1) & (i == line_to_be_rerouted['SEQ'].max())):
            to_reroute_part.append(
                [
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'A'].iloc[0],
                    line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == i, 'B'].iloc[0]])
            to_reroute.append(to_reroute_part)
            i += 1

    logging.debug('all segments to reroute: {}'.format(to_reroute))

    def node_pairs_to_node_list(node_pairs):
        node_list = []
        for node_pair in node_pairs:
            node_list.append(node_pair[0])
            if node_pair == node_pairs[-1]:
                node_list.append(node_pair[1])
        logging.debug('node_pairs: {}/nnode_list: {}'.format(node_pairs, node_list))
        return node_list

    to_reroute_as_node_list = []
    for segment in to_reroute:
        segment_as_node_list = node_pairs_to_node_list(segment)
        to_reroute_as_node_list.append(segment_as_node_list)

    return to_reroute_as_node_list


def find_shortest_path(start, end, G, TM1_nodes_G_nodes_dict):

    route_in_G_nodes = nx.shortest_path(
                G,
                source=TM1_nodes_G_nodes_dict[start], 
                target=TM1_nodes_G_nodes_dict[end], 
                weight='DISTANCE')
    logging.debug('rerouted nodes in the Graph: {}'.format(route_in_G_nodes))

    # convert back to TM1 node id
    route_in_TM1_nodes = [list(TM1_nodes_G_nodes_dict.keys())[list(TM1_nodes_G_nodes_dict.values()).index(i)] for i in route_in_G_nodes]
    logging.debug('rerouted nodes in TM1: {}'.format(route_in_TM1_nodes))

    return route_in_TM1_nodes


def reroute_segment(segment_start_end, G, TM1_nodes_G_nodes_dict, line_to_be_rerouted, line_name):

    """
    Reroute one flooded segment by looking for the shortest path between the start/end nodes of the flooded segment within the remaining (unflooded)
    network. When a shortest path cannot be found between the initial flooded start/end nodes, incrementally expand the to-reroute segment, try
    rerouting from an earlier start node and/or a later end node. 
    Finally, write out the original flooded start/end node, the actual to-reroute start/end node, and the rerouted path (expressed in TM1 node).
    
    """

    # segment is presented as a node list
    logging.debug('segment for reroute: {}'.format(segment_start_end))
    start_node = segment_start_end[0]
    end_node = segment_start_end[-1]
    logging.debug('initial start node: {}'.format(start_node))
    logging.debug('initial end node: {}'.format(end_node))
    
    original_start_node_seq = line_to_be_rerouted.loc[line_to_be_rerouted['A'] == start_node, 'SEQ'].iloc[0]
    original_end_node_seq = line_to_be_rerouted.loc[line_to_be_rerouted['B'] == end_node, 'SEQ'].iloc[0]

    # try rerouting
    start_node_seq = line_to_be_rerouted.loc[line_to_be_rerouted['A'] == start_node, 'SEQ'].iloc[0]
    end_node_seq = line_to_be_rerouted.loc[line_to_be_rerouted['B'] == end_node, 'SEQ'].iloc[0]

    while ((start_node_seq >= 1) & (end_node_seq <= line_to_be_rerouted['SEQ'].max())):
        try:
            logging.debug('rerouting: {}-{}'.format(start_node, end_node))
            # rerouted_G_nodes = nx.shortest_path(
            #     G,
            #     source=TM1_nodes_G_nodes_dict[start_node], 
            #     target=TM1_nodes_G_nodes_dict[end_node], 
            #     weight='DISTANCE')
            # logging.debug('rerouted nodes in the Graph: {}'.format(rerouted_G_nodes))

            # # convert back to TM1 node id
            # rerouted_TM1_nodes = [list(TM1_nodes_G_nodes_dict.keys())[list(TM1_nodes_G_nodes_dict.values()).index(i)] for i in rerouted_G_nodes]
            # logging.debug('rerouted nodes in TM1: {}'.format(rerouted_TM1_nodes))
            rerouted_TM1_nodes = find_shortest_path(start_node, end_node, G, TM1_nodes_G_nodes_dict)
            break
        except:
            logging.debug('failed to reroute: {}-{}'.format(start_node, end_node))

        if end_node_seq < line_to_be_rerouted['SEQ'].max():
            # if the initial rerouting failed to find a path, try rerouting to the end of the immediate next link
            try:
                end_node_seq += 1
                end_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == end_node_seq, 'B'].iloc[0]
                
                logging.debug('cannot reroute the initial segment, including the next link')
                logging.debug('rerouting: {}-{}'.format(start_node, end_node))
                # rerouted_G_nodes = nx.shortest_path(
                #     G,
                #     source=TM1_nodes_G_nodes_dict[start_node],
                #     target=TM1_nodes_G_nodes_dict[end_node],
                #     weight='DISTANCE')
                # logging.debug('rerouted nodes in the Graph: {}'.format(rerouted_G_nodes))

                # # convert back to TM1 node id
                # rerouted_TM1_nodes = [list(TM1_nodes_G_nodes_dict.keys())[list(TM1_nodes_G_nodes_dict.values()).index(i)] for i in rerouted_G_nodes]
                # logging.debug('rerouted nodes in TM1: {}'.format(rerouted_TM1_nodes))
                rerouted_TM1_nodes = find_shortest_path(start_node, end_node, G, TM1_nodes_G_nodes_dict)
                break
            except:
                logging.debug('failed to reroute: {}-{}'.format(start_node, end_node))
                end_node_seq -= 1
                end_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == end_node_seq, 'B'].iloc[0]

        if start_node_seq > 1:
            try:
                # if still failed to find a path, try rerouting from the start of the immeidate previous link
                start_node_seq -= 1
                start_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == start_node_seq, 'A'].iloc[0]
                
                logging.debug('cannot reroute the initial segment, including the previous link')
                logging.debug('rerouting: {}-{}'.format(start_node, end_node))
                # rerouted_G_nodes = nx.shortest_path(
                #     G,
                #     source=TM1_nodes_G_nodes_dict[start_node], 
                #     target=TM1_nodes_G_nodes_dict[end_node], 
                #     weight='DISTANCE')
                # logging.debug('rerouted nodes in the Graph: {}'.format(rerouted_G_nodes))

                # # convert back to TM1 node id
                # rerouted_TM1_nodes = [list(TM1_nodes_G_nodes_dict.keys())[list(TM1_nodes_G_nodes_dict.values()).index(i)] for i in rerouted_G_nodes]
                # logging.debug('rerouted nodes in TM1: {}'.format(rerouted_TM1_nodes))
                rerouted_TM1_nodes = find_shortest_path(start_node, end_node, G, TM1_nodes_G_nodes_dict)
                break        
            except:
                logging.debug('failed to reroute: {}-{}'.format(start_node, end_node))
                start_node_seq += 1
                start_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == start_node_seq, 'A'].iloc[0]

        # if still failed to find a path, try rerouting with both the next and previous links
        if (end_node_seq < line_to_be_rerouted['SEQ'].max()) & (start_node_seq > 1):
            end_node_seq += 1
            end_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == end_node_seq, 'B'].iloc[0]
            start_node_seq -= 1
            start_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == start_node_seq, 'A'].iloc[0]
            logging.debug('start the next round, with start-end: {}-{}'.format(start_node, end_node))
        elif (end_node_seq == line_to_be_rerouted['SEQ'].max()) & (start_node_seq > 1):
            start_node_seq -= 1
            start_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == start_node_seq, 'A'].iloc[0]
        elif (end_node_seq < line_to_be_rerouted['SEQ'].max()) & (start_node_seq == 1):
            end_node_seq += 1
            end_node = line_to_be_rerouted.loc[line_to_be_rerouted['SEQ'] == end_node_seq, 'B'].iloc[0]       
        if (end_node_seq == line_to_be_rerouted['SEQ'].max()) & (start_node_seq == 1):
            logging.debug('finally, cannot reroute')
            break

    try:
        rerouted_TM1_nodes
        logging.info('--------finished rerouting segment {}'.format(line_name))
        segment_rerouted = {
            'line': line_name,
            'flooded': segment_start_end,
            'flood_seq': [original_start_node_seq, original_end_node_seq],
            'reroute_segment': [start_node, end_node],
            'reroute_segment_seq': [start_node_seq, end_node_seq],
            'rerouted': rerouted_TM1_nodes
        }
    except NameError:
        logging.info('--------cannot reroute segment {}'.format(line_name))
        if (original_end_node_seq == line_to_be_rerouted['SEQ'].max()) & (original_start_node_seq != 1):
            segment_rerouted = {
                'line': line_name,
                'flooded': segment_start_end,
                'flood_seq': [original_start_node_seq, original_end_node_seq],
                'reroute_segment': segment_start_end,
                'reroute_segment_seq': [original_start_node_seq, original_end_node_seq],
                'rerouted': ['cannot reroute, end of line']
            }
        elif (original_start_node_seq == 1) & (original_end_node_seq < line_to_be_rerouted['SEQ'].max()):
            segment_rerouted = {
                'line': line_name,
                'flooded': segment_start_end,
                'flood_seq': [original_start_node_seq, original_end_node_seq],
                'reroute_segment': segment_start_end,
                'reroute_segment_seq': [original_start_node_seq, original_end_node_seq],
                'rerouted': ['cannot reroute, start of line']
            }
        elif (original_start_node_seq == 1) & (original_end_node_seq == line_to_be_rerouted['SEQ'].max()):
            segment_rerouted = {
                'line': line_name,
                'flooded': segment_start_end,
                'flood_seq': [original_start_node_seq, original_end_node_seq],
                'reroute_segment': segment_start_end,
                'reroute_segment_seq': [original_start_node_seq, original_end_node_seq],
                'rerouted': ['cannot reroute, entire ine']
            }
    
    return segment_rerouted


def reroute_line(G, TM1_nodes_G_nodes_dict, line_to_be_rerouted, line_name):

    """
    For a line that is affected and needs rerouting, reroute all the flooded segments.
    
    """ 

    rerouted_per_line = pd.DataFrame(columns = ['line', 'flooded', 'flood_seq', 'reroute_segment', 'reroute_segment_seq', 'rerouted'])
    
    flooded_segments_as_node_list = get_line_segments_to_reroute(line_to_be_rerouted)

    # third, reroute each segment
    
    for segment_to_route in flooded_segments_as_node_list:
        logging.info('--------segment_to_route: {}'.format(segment_to_route))
        rerouted = reroute_segment(
            [segment_to_route[0], segment_to_route[-1]], 
            G, 
            TM1_nodes_G_nodes_dict, 
            line_to_be_rerouted, 
            line_name)
        # print(rerouted)
        # line_reroute_tracking.append(rerouted)
        rerouted_per_line.loc[rerouted_per_line.shape[0]] = rerouted

        logging.info('--------rerouting result: {}'.format(rerouted_per_line))

    rerouted_per_line['rerouted_cnt'] = rerouted_per_line.shape[0]
    logging.info('----finished initial rerouting of line {}: \n{}'.format(line_name, rerouted_per_line))
    
    return rerouted_per_line


def remove_reroute_overlap(G, TM1_nodes_G_nodes_dict, line_rerouted, line_to_be_rerouted, line_name):
    """
    When a line needs to reroute multiple flooded segments, and one of more segment has extended start/end node during the initial rerouting,
    there could be overlaps among the rerouted segments. This step modifies the initial rerouting by combining the rerouted segments.

    """
    logging.info('----modifying raw resulting result to remove overlap for line {}'.format(line_name))
    line_rerouted_modified = pd.DataFrame(columns=list(line_rerouted)+['modify'])

    df = line_rerouted.reset_index()
    df['modify'] = ''

    df['start_seq'] = df['reroute_segment_seq'].apply(lambda x: x[0])
    df['end_seq'] = df['reroute_segment_seq'].apply(lambda x: x[-1])

    df['initial_start_node'] = df['flooded'].apply(lambda x: x[0])
    df['initial_end_node'] = df['flooded'].apply(lambda x: x[-1])
    df['initial_start_seq'] = df['flood_seq'].apply(lambda x: x[0])
    df['initial_end_seq'] = df['flood_seq'].apply(lambda x: x[-1])

    df['rerouted_start_node'] = df['reroute_segment'].apply(lambda x: x[0])
    df['rerouted_end_node'] = df['reroute_segment'].apply(lambda x: x[-1])
    logging.debug('--------before modification: \n{}'.format(df))

    # if the line only has 1 segment rerouted, do nothing
    if df.shape[0] == 1:
        line_rerouted_modified = pd.concat([line_rerouted_modified, df])

    # if the line only more than 1 segment rerouted
    elif df.shape[0] > 1:
        for i in range(1, df.shape[0]):
            logging.debug('--------modifying rerouted segment {}'.format(i))
            # print(i)
            # if the previous rerouted segment covers partial the current rerouted segment (previous end of reroute fall into the middle of the current),
            # update the staring node of the current segment to be the end node of the previous rerouted segment, and redo the current reroute
            if (df['end_seq'][i-1] > df['start_seq'][i]) & \
                (df['end_seq'][i-1] < df['end_seq'][i]) & \
                (df['start_seq'][i-1] < df['start_seq'][i]):
                logging.debug('update rerouting')
                df['flooded'][i] = [df['rerouted_end_node'][i-1], df['rerouted_end_node'][i]]
                # print(df)
                logging.debug('--------case 1')
                rerouted = reroute_segment(
                    df['flooded'][i], 
                    G, 
                    TM1_nodes_G_nodes_dict, 
                    line_to_be_rerouted, 
                    linename)
                # print(rerouted)
                df.loc[i] = rerouted
                df['modify'][i] = 'updated'
                logging.debug('--------modified to \n{}'.format(df))

            # if the previous rerouted segment completely fall into the current rerouted segment 
            elif (df['end_seq'][i-1] <= df['end_seq'][i]) & \
                (df['start_seq'][i-1] >= df['start_seq'][i]):
                    # if the end of the previous reroute segment already covers the end of the current flooded segment (which could be earler
                    # on the line than the actually current rerouted end point), only keep the previous reroute segment,
                    # because it has less overall rerouting but already covers both flooded segments
                    if df['end_seq'][i-1] >= df['initial_end_seq'][i]:
                        logging.debug('--------case 2')
                        df['modify'][i] = 'drop'
                        logging.debug('--------modified to \n{}'.format(df))
                    # otherwise, keep the current one (with more overall rerouting)
                    elif df['end_seq'][i-1] < df['initial_end_seq'][i]:
                        logging.debug('--------case 3')
                        df['modify'][i-1] = 'drop'
                        logging.debug('--------modified to \n{}'.format(df))
            
            # if the previous rerouted segment completely covers the current rerouted segment 
            elif (df['end_seq'][i-1] >= df['end_seq'][i]) & \
                (df['start_seq'][i-1] <= df['start_seq'][i]):
                    # if the start of the current reroute segment already covers the start of the previous flooded segment (which could be later
                    # on the line than the actually previous rerouted start point), only keep the current reroute segment,
                    # because it has less overall rerouting but already covers both flooded segments
                    if df['start_seq'][i] <= df['initial_start_seq'][i-1]:
                        logging.debug('--------case 4')
                        df['modify'][i-1] = 'drop'
                        logging.debug('--------modified to \n{}'.format(df))
                    # otherwise, keep the previous one (with more overall rerouting)
                    elif df['start_seq'][i] > df['initial_start_seq'][i-1]:
                        logging.debug('--------case 5')
                        df['modify'][i] = 'drop'
                        logging.debug('--------modified to \n{}'.format(df))

        # append the update segment reroute result
        line_rerouted_modified = pd.concat([line_rerouted_modified, df])
    
    line_rerouted_modified = line_rerouted_modified[list(line_rerouted)+['modify']]
    logging.info('----finished modifying the rerouting of line {}: \n{}'.format(line_name, line_rerouted_modified))

    return line_rerouted_modified


def add_stop_attr(line_rerouted, trn_stops_on_line):
    """
    For the rerouted line segments, add info for whether the start node and end node are stops - if the start/end nodes are stops
    before rerouting, yes, otherwise no. 
    """

    logging.info('----adding stop information for the start/end nodes of the rerouted segments')

    line_rerouted['start'] = line_rerouted['reroute_segment'].apply(lambda x: x[0])
    line_rerouted['end'] = line_rerouted['reroute_segment'].apply(lambda x: x[-1])
    line_rerouted = pd.merge(
        line_rerouted,
        trn_stops_on_line[['N', 'IS_STOP']].rename({'N': 'start', 'IS_STOP': 'start_is_stop'}, axis=1).drop_duplicates(),
        on='start',
        how='left'
    )
    line_rerouted = pd.merge(
        line_rerouted,
        trn_stops_on_line[['N', 'IS_STOP']].rename({'N': 'end', 'IS_STOP': 'end_is_stop'}, axis=1).drop_duplicates(),
        on='end',
        how='left'
    )
    # print(line_rerouted.shape[0])

    # format 'rerouted' to reflect stop information
    def add_stop_sign(route_ls, start_is_stop, end_is_stop):
        route_ls_withStopSign = [i*(-1) for i in route_ls]
        if start_is_stop == 1:
            route_ls_withStopSign[0] = route_ls_withStopSign[0] * (-1)
        if end_is_stop == 1:
            route_ls_withStopSign[-1] = route_ls_withStopSign[-1] * (-1)
        return route_ls_withStopSign

    for index, row in line_rerouted.iterrows():
        if len(row['rerouted']) > 1:
            logging.debug('--------reroute result: {}'.format(row['rerouted']))
            row['rerouted_stopSign'] = add_stop_sign(row['rerouted'], row['start_is_stop'], row['end_is_stop'])
            logging.debug('--------after adding stop info: {}'.format(row['rerouted_stopSign']))
            line_rerouted.loc[index, 'rerouted_stopSign'] = str(row['rerouted_stopSign'])

    logging.info('----finished adding stop information for the start/end nodes of the rerouted segments')

    return line_rerouted


def format_for_initDotPy(all_lines_rerouted_final, text_file_path):

    """
    Write the rerouting result into text file with format that can be copy-pasted into __init__.py for project coding.
    """

    if os.path.exists(text_file_path):
        os.remove(text_file_path)

    all_lines_rerouted_final['rerouted_stopSign'].fillna('na', inplace=True)
    all_lines_rerouted_final.loc[all_lines_rerouted_final['rerouted_stopSign']=='', 'rerouted_stopSign'] = 'na'

    # logging.debug('\n{}'.format(all_lines_rerouted_final['rerouted_stopSign'].value_counts(dropna=False)))
    with open(text_file_path, 'w') as file_out:

        # segments that can reroute
        df_rerouted = all_lines_rerouted_final.loc[all_lines_rerouted_final['rerouted_stopSign'] != 'na']

        # print(df_rerouted.dtypes())
        df_rerouted_agg = df_rerouted.groupby([
            df_rerouted['reroute_segment'].apply(tuple),
            df_rerouted['rerouted'].apply(tuple),
            'rerouted_stopSign', 
            'start', 
            'end'])['line'].apply(lambda x: ','.join(x)).reset_index()
        logging.debug(df_rerouted_agg)
        df_rerouted_agg.sort_values(by='reroute_segment', inplace=True)

        for index, row in df_rerouted_agg.iterrows():
            line = '# reroute segment {}: {}\n'.format(row['reroute_segment'], row['line'])
            file_out.write(line)
            line = 'net.replaceSegmentInTransitLines(\n'
            file_out.write(line)
            line = '    nodeA={},\n'.format(row['start'])
            file_out.write(line)
            line = '    nodeB={},\n'.format(row['end'])
            file_out.write(line)
            line = '    newNodes={},\n'.format(row['rerouted_stopSign'])
            file_out.write(line)
            line = '    )\n'
            file_out.write(line)
        
        # segments that cannot reroute
        df_cannot_reroute = all_lines_rerouted_final.loc[all_lines_rerouted_final['rerouted_stopSign'] == 'na']
        for index, row in df_cannot_reroute.iterrows():
            if not '-' in row['line']:
                if ('end of line' in str(row['rerouted'])):
                    line = '# {} remove end of line segment {}\n'.format(row['line'], row['reroute_segment'])
                    file_out.write(line)
                    line = 'line = net.line("{}")\n'.format(row['line'])
                    file_out.write(line)
                    line = 'line.extendLine(oldnode   ={},\n'.format(row['start'])
                    file_out.write(line)
                    line = '                newsection={},\n'.format([row['start']])
                    file_out.write(line)
                    line = '                beginning =False)\n'
                    file_out.write(line)
                elif ('start of line' in str(row['rerouted'])):
                    line = '# {} remove start of line segment {}\n'.format(row['line'], row['reroute_segment'])
                    file_out.write(line)
                    line = 'line = net.line("{}")\n'.format(row['line'])
                    file_out.write(line)
                    line = 'line.extendLine(oldnode   ={},\n'.format(row['end'])
                    file_out.write(line)
                    line = '                newsection={},\n'.format([row['end']])
                    file_out.write(line)
                    line = '                beginning =True)\n'
                    file_out.write(line)
            else:
                if ('end of line' in str(row['rerouted'])):
                    line = '# {} remove end of line segment {}\n'.format(row['line'], row['reroute_segment'])
                    file_out.write(line)
                    line = "try:\n"
                    file_out.write(line)
                    line = '    line = net.line("{}")\n'.format(row['line'])
                    file_out.write(line)
                    line = '    line.extendLine(oldnode   ={},\n'.format(row['start'])
                    file_out.write(line)
                    line = '                    newsection={},\n'.format([row['start']])
                    file_out.write(line)
                    line = '                    beginning =False)\n'
                    file_out.write(line)
                    line = 'except:\n'
                    file_out.write(line)
                    line = '    net.replaceSegmentInTransitLines(\n'
                    file_out.write(line)
                    line = '    nodeA={},\n'.format(row['start'])
                    file_out.write(line)
                    line = '    nodeB={},\n'.format(row['end'])
                    file_out.write(line)
                    line = '    newNodes={},\n'.format([row['start']])
                    file_out.write(line)
                    line = '    )\n'
                    file_out.write(line)

                elif ('start of line' in str(row['rerouted'])):
                    line = '# {} remove start of line segment {}\n'.format(row['line'], row['reroute_segment'])
                    file_out.write(line)
                    line = "try:\n"
                    file_out.write(line)
                    line = '    line = net.line("{}")\n'.format(row['line'])
                    file_out.write(line)
                    line = '    line.extendLine(oldnode   ={},\n'.format(row['end'])
                    file_out.write(line)
                    line = '                    newsection={},\n'.format([row['end']])
                    file_out.write(line)
                    line = '                    beginning =True)\n'
                    file_out.write(line)                
                    line = 'except:\n'
                    file_out.write(line)
                    line = '    net.replaceSegmentInTransitLines(\n'
                    file_out.write(line)
                    line = '    nodeA={},\n'.format(row['start'])
                    file_out.write(line)
                    line = '    nodeB={},\n'.format(row['end'])
                    file_out.write(line)
                    line = '    newNodes={},\n'.format([row['end']])
                    file_out.write(line)
                    line = '    )\n'
                    file_out.write(line)

    file_out.close()

def find_nearest_stop(rail_stations_gdf, bus_stops_gdf):
    """
    Find the nearest bus stops to the rail stations.
    """

    # convert to EPSG:26910
    rail_stations_gdf = rail_stations_gdf.to_crs('EPSG:26910')
    bus_stops_gdf = bus_stops_gdf.to_crs('EPSG:26910')

    # nearest stop
    nearest_stops = gpd.sjoin_nearest(
        rail_stations_gdf, 
        bus_stops_gdf, 
        distance_col='distances',
        lsuffix='rail',
        rsuffix='bus',
        exclusive=True)
    
    logging.debug('nearest stops: \n{}'.format(nearest_stops))
   
    return nearest_stops

def create_rail_connecting_shuttle(G, TM1_nodes_G_nodes_dict, rail_segments_need_shuttle):

    for index, row in rail_segments_need_shuttle.iterrows():
        railname = row['operator']
        rail_segment = row['rail_segment_flood']
        logging.debug('create shuttle route for {}, {}; rail stations {}-{}, bus stops {}-{}'.format(
            railname, rail_segment, row['start_node'], row['end_node'], row['start_node_bus'], row['end_node_bus']
        ))
        row['shuttle_route'] = find_shortest_path(
            row['start_node_bus'],
            row['end_node_bus'],
            G_for_rerouting,
            TM1_nodes_G_nodes_dict_for_rerouting
        )
        rail_segments_need_shuttle.loc[index, 'shuttle_route'] = str(row['shuttle_route'])

    # return rail_segments_need_shuttle


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter,)
    # parser.add_argument("transit_option",       choices=['bus','rail'], help="reroute bus line segments or create bus shuttle for rail segments")
    parser.add_argument("--bus",                dest='bus', action='store_true', help="reroute bus line segments")
    parser.add_argument("--rail",               dest='rail', action='store_true', help="create bus shuttle for rail segments")
    parser.add_argument("year",                 help="Year for the rerouting, currently 2035 or 2050")
    parser.add_argument("del_link_file_path",   help="File path of link deletion, which would require rerouting transit")
    parser.add_argument("base_network_dir",     help="Directory of base network files, typically the 'shapefile' folder created with cube_to_shape script")
    # TODO: make the following arg optional, only required if transit_option == rail
    parser.add_argument("--slr_fact_sheet",       help='File path of SLR fact sheet')
    parser.add_argument("qaqc_dir",             help="Directory of QAQC files")
    # parser.add_argument("text_file_path",       help="File path of text file with TM1 NetworkProject file __init__.py format")
    args = parser.parse_args()

    if not args.bus and not args.rail:
        print("Must be bus (for bus rerouting) or rail (for rail alternative shuttle creating). Please specify --bus and/or --rail")
        sys.exit(2)
    
    if args.rail and args.slr_fact_sheet is None:
        print("Must provide SLR fact sheet for rail")
        sys.exit(2)       

    # QAQC_DIR = r'M:\Application\PBA50Plus_Data_Processing\SLR\reroute_TM1_transit\testing'
    
    # TRANSIT_OPTION = args.transit_option
    YEAR = args.year
    DEL_LINK_FILE = args.del_link_file_path
    BASE_NETWORK_DIR = args.base_network_dir
    if args.rail :
        SLR_FACT_SHEET = args.slr_fact_sheet
    QAQC_DIR = args.qaqc_dir
    if args.bus:
        BUS_REROUTING_TEXT_FILE = os.path.join(QAQC_DIR, 'bus_reroute_text_file_{}.text'.format(YEAR))
    if args.rail:
        RAIL_SHUTTLE_FILE = os.path.join(QAQC_DIR, 'rail_shuttle_{}.csv'.format(YEAR))
    LOG_FILE = os.path.join(QAQC_DIR, 'reroute_transit_{}_{}_{}.log')

    ################## create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ################## console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(ch)
    ################## file handler - info
    fh = logging.FileHandler(LOG_FILE.format(YEAR, 'info', datetime.date.today()), mode="w")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(fh)
    ################## file handler - debug
    fh = logging.FileHandler(LOG_FILE.format(YEAR, 'debug', datetime.date.today()), mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(fh)

    # logging.info('Transit option: {}'.format(TRANSIT_OPTION))
    logging.info('Run bus rerouting: {}'.format(args.bus))
    logging.info('Run rail shuttle creating: {}'.format(args.rail))
    logging.info('Year: {}'.format(YEAR))
    logging.info('link_delete_file: {}'.format(DEL_LINK_FILE))
    logging.info('base network: {}'.format(BASE_NETWORK_DIR))
    if args.rail:
        logging.info('slr fact sheet: {}'.format(SLR_FACT_SHEET))
    logging.info('QAQC and export directory: {}'.format(QAQC_DIR))


    # tm1_link_delete = pd.read_csv(r'M:\Application\PBA50Plus_Data_Processing\SLR\tag_TM1_roadway_links\SLR_Del_20240820.csv')
    tm1_link_delete = pd.read_csv(DEL_LINK_FILE)
    logging.info('total {} roadway links tagged as flooded'.format(len(tm1_link_delete[['A', 'B']].drop_duplicates())))
    logging.info('count deleted links by year and scenario: \n{}'.format(tm1_link_delete.groupby(['SCENARIO', 'YEAR'])['A'].count()))
    logging.debug(tm1_link_delete.head())

    tm1_link_delete = tm1_link_delete.loc[tm1_link_delete['YEAR'] <= int(YEAR)]
    logging.info('keep {} roadway links flooded for the current year'.format(tm1_link_delete.shape[0]))


    # roadway_links_gdf_2035 = gpd.read_file(
    #     r'M:\Application\Model One\RTP2025\INPUT_DEVELOPMENT\Networks\BlueprintNetworks_v18\net_2035_Blueprint\shapefiles\network_links.shp')
    base_roadway_links_gdf = gpd.read_file(os.path.join(BASE_NETWORK_DIR, 'network_links.shp'))
    logging.info('loaded {} rows of roadway links from {}'.format(len(base_roadway_links_gdf), os.path.join(BASE_NETWORK_DIR, 'network_links.shp')))
    logging.info('link count by FT: \n{}'.format(base_roadway_links_gdf['FT'].value_counts()))

    # base_tm1_trn_links = gpd.read_file(
    # r'M:\Application\Model One\RTP2025\INPUT_DEVELOPMENT\Networks\BlueprintNetworks_v18\net_2035_Blueprint\shapefiles\network_trn_links.shp')
    base_tm1_trn_links = gpd.read_file(os.path.join(BASE_NETWORK_DIR, 'network_trn_links.shp'))
    logging.info('loaded trn_links from {}, {} rows in trn_links, {} unique A-B pairs'.format(
        os.path.join(BASE_NETWORK_DIR, 'network_trn_links.shp'),
        len(base_tm1_trn_links), 
        len(base_tm1_trn_links[['A', 'B']].drop_duplicates())))

    # tm1_trn_stops_2035 = gpd.read_file(
    # r'M:\Application\Model One\RTP2025\INPUT_DEVELOPMENT\Networks\BlueprintNetworks_v18\net_2035_Blueprint\shapefiles\network_trn_stops.shp'
    # )
    base_tm1_trn_stops = gpd.read_file(os.path.join(BASE_NETWORK_DIR, 'network_trn_stops.shp'))
    logging.info('loaded trn_stops from {}, {} rows, by IS_STOP: \n{}'.format(
        os.path.join(BASE_NETWORK_DIR, 'network_trn_stops.shp'),
        base_tm1_trn_stops.shape[0],
        base_tm1_trn_stops['IS_STOP'].value_counts()))
    
    base_tm1_trn_stops_IsStop = base_tm1_trn_stops.loc[base_tm1_trn_stops['IS_STOP'] == 1]
    logging.info('keep only stops, {} rows'.format(base_tm1_trn_stops_IsStop.shape[0]))

    # step 1: flooding tagging
    logging.info('Step 1: tagging roadway links, transit links, and transit stops with flooding info')
    unflooded_links, links_on_flooded_lines, unflooded_trn_stops = get_unflooded_network(
        tm1_link_delete,
        base_roadway_links_gdf,
        base_tm1_trn_links,
        base_tm1_trn_stops_IsStop,
        YEAR
    )
    # step 2: build graph from unflooded roadway network
    logging.info('Step 2: building a graph with unflooded network')
    G_for_rerouting, TM1_nodes_G_nodes_dict_for_rerouting = build_graph(unflooded_links)

    if args.bus:
        # step 3: reroute lines affected by flooding
        logging.info('Step 3: rerouting bus lines')
        # raw rerouting result, for QAQC
        all_rerouted_raw = pd.DataFrame(
            columns = ['line', 'flooded', 'flood_seq', 'reroute_segment', 'reroute_segment_seq', 'rerouted', 'rerouted_cnt'])
        
        # an interim version with modify note, for QAQC
        all_rerouted_modify = pd.DataFrame(
            columns = ['line', 'flooded', 'flood_seq', 'reroute_segment', 'reroute_segment_seq', 'rerouted', 'rerouted_cnt', 'modify'])

        # final rerouting result
        all_rerouted_final = pd.DataFrame(
            columns = ['line', 'flooded', 'flood_seq', 'reroute_segment', 'reroute_segment_seq', 'rerouted', 'rerouted_cnt',
                    'start', 'end', 'start_is_stop', 'end_is_stop', 'rerouted_stopSign'])

        for linename in links_on_flooded_lines['NAME'].unique():
            logging.info('----rerouting line {}'.format(linename))
            links_on_line = links_on_flooded_lines.loc[links_on_flooded_lines['NAME'] == linename][[
                'A', 'B', 'SEQ', 'DEL', 'YEAR'
            ]]
            # first, for each line affected, reroute all the segments
            line_rerouted = reroute_line(
                G_for_rerouting,
                TM1_nodes_G_nodes_dict_for_rerouting,
                links_on_line,
                linename)

            all_rerouted_raw = pd.concat([all_rerouted_raw, line_rerouted])

            # second, modify to deal with overlapping rerouted segment
            line_rerouted_modified = remove_reroute_overlap(
                G_for_rerouting,
                TM1_nodes_G_nodes_dict_for_rerouting,
                line_rerouted,
                links_on_line,
                linename
            )
            # keep a record for QAQC
            all_rerouted_modify = pd.concat([all_rerouted_modify, line_rerouted_modified])

            # drop rerouted segment labeled as 'drop', and update the count
            line_rerouted_final = line_rerouted_modified.loc[
                line_rerouted_modified['modify'] != 'drop']
            line_rerouted_final.drop(['modify'], axis=1, inplace=True)
            line_rerouted_final['rerouted_cnt'] = line_rerouted_final.groupby('line')['flooded'].transform('count')

            # lastly, add info on whether the start/end of the rerouted segment is a stop
            stops_on_line = base_tm1_trn_stops_IsStop.loc[base_tm1_trn_stops_IsStop['LINE_NAME'] == linename]
            line_rerouted_withStopAttr = add_stop_attr(line_rerouted_final, stops_on_line)

            all_rerouted_final = pd.concat([all_rerouted_final, line_rerouted_withStopAttr])

        # write out
        logging.info('Step 3 complete: writing out rerouting data')
        all_rerouted_raw.to_csv(os.path.join(QAQC_DIR, 'bus_reroute_{}_raw.csv'.format(YEAR)), index=False)
        all_rerouted_modify.to_csv(os.path.join(QAQC_DIR, 'bus_reroute_{}_interim.csv'.format(YEAR)), index=False)
        all_rerouted_final.to_csv(os.path.join(QAQC_DIR, 'bus_reroute_{}_final.csv'.format(YEAR)), index=False)

        # format the rerouting info into text that can be pasted into _init__.py
        logging.info('Step 4: formating')
        format_for_initDotPy(
            all_rerouted_final,
            BUS_REROUTING_TEXT_FILE)
        logging.info('Step 4 complete: formated file saved as {}'.format(BUS_REROUTING_TEXT_FILE))

    if args.rail:
        logging.info('Step 3: get rail link flooding info from fact sheet: {}'.format(SLR_FACT_SHEET))
        rail_flooding = pd.read_excel(SLR_FACT_SHEET, sheet_name='rail_links_flood')

        rail_need_shuttle = rail_flooding.loc[(rail_flooding['shuttle'] == 'yes') & (rail_flooding['year'] == int(YEAR))]
        for i in ['start_node', 'end_node']:
            rail_need_shuttle[i] = rail_need_shuttle[i].astype(int)
        logging.info('Shuttle bus needed for the following rail segments: \n{}'.format(rail_need_shuttle))

        logging.info('Step 4: get the nearest unflooded bus stops of each rail station that need shuttle connection')
        # rail staions (in TM1 nodes) as the start/end of shuttles
        rail_stations_for_shuttle = list(set(rail_need_shuttle['start_node']) | set(rail_need_shuttle['end_node']))
        # get geometry
        rail_stations_for_shuttle_gdf = base_tm1_trn_stops.loc[
            base_tm1_trn_stops['N'].isin(rail_stations_for_shuttle)][['N', 'IS_STOP', 'geometry']].drop_duplicates()
        
        # get unflooded stops that are not rail/ferry/LRT stops
        # first, get lines that are not rail/ferry/LRT
        base_tm1_trn_links_busOnly = base_tm1_trn_links.loc[
            base_tm1_trn_links['MODE_NAME'].str.contains('Ferries|Ferry|BART|Caltrain|Amtrak|ACE|SMART|LRT|Cable|Metro') == False]
        bus_lines = base_tm1_trn_links_busOnly['NAME'].unique()
        # then, busOnly stops
        unflooded_trn_stops_busOnly = unflooded_trn_stops.loc[unflooded_trn_stops['LINE_NAME'].isin(bus_lines)]
        # drop duplicates as one stop can be used by multiple lines
        unflooded_trn_stops_busOnly = unflooded_trn_stops_busOnly[['N', 'geometry']].drop_duplicates()

        # find the closest unflooded transit stops
        stops_for_shuttle = find_nearest_stop(
            rail_stations_for_shuttle_gdf,
            unflooded_trn_stops_busOnly)

        # add the cloest bus stops to rail_need_shuttle
        rail_need_shuttle = pd.merge(
            rail_need_shuttle,
            stops_for_shuttle[['N_rail', 'N_bus']].rename({'N_rail': 'start_node', 'N_bus': 'start_node_bus'}, axis=1),
            on='start_node',
            how='left'
        )
        rail_need_shuttle = pd.merge(
            rail_need_shuttle,
            stops_for_shuttle[['N_rail', 'N_bus']].rename({'N_rail': 'end_node', 'N_bus': 'end_node_bus'}, axis=1),
            on='end_node',
            how='left'
        )
        logging.debug('found the cloest bus stops of the following rail stations: \n{}'.format(rail_need_shuttle))

        # create shuttle and append to the df
        logging.info('Step 5: find shuttle route to replace flooded rail segments based on shortest path')
        create_rail_connecting_shuttle(
            G_for_rerouting,
            TM1_nodes_G_nodes_dict_for_rerouting,
            rail_need_shuttle)
        
        # TODO: automatically generate other info, e.g. operator, color, frequencies

        # write out
        logging.info('Step 6: writing out to {}'.format(RAIL_SHUTTLE_FILE))
        rail_need_shuttle.to_csv(RAIL_SHUTTLE_FILE, index=False)