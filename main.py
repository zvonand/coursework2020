#!/usr/bin/env python3

import sys
import networkx as nx
import pickle

def convert_graph (base: nx.Graph) -> nx.Graph:
    #for now assume initial graph was not a multigraph
    ret = base
    base_edges = base.edges()
    size = len(base.edges())
    max_node = size

    for a, b in base_edges:
        for i in range(base[a][b]['cap']):
            ret.add_edge(a, max_node, cap=1, wt=1)
            ret.add_edge(max_node, b, cap=1, wt=1)
            max_node += 1

    return ret


def find_paths(base_graph: nx.Graph, fr, to, path_num: int, cap_req: int):

    graph = nx.Graph() #convert_graph(nx.Graph(base_graph))

    size = len(base_graph.edges())
    max_node = size

    for a, b in base_graph.edges():

        graph.add_edge(a, b, cap=1, wt=0)
        for i in range(1, path_num):
            graph.add_edge(a, max_node + i - 1, cap=1, wt=i)
            graph.add_edge(max_node + i - 1, b, cap=1, wt=0)
        max_node += path_num - 1

    graph.add_edge(to, max_node, cap=cap_req, wt=0)
    finish = max_node
    mfmc = nx.max_flow_min_cost(graph, fr, finish, capacity='cap', weight='wt')
    paths = []

    for counter in range(path_num):
        i = fr
        path = [fr]
        while i != to:
            for key, value in mfmc[i].items():
                if value == 1:
                    mfmc[i][key] = 0
                    path.append(key)
                    i = key
                    break
        paths.append(path)

    return paths



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Usage: main.py [topo_file]')
        sys.exit(1)

    with open(sys.argv[1], 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    paths = find_paths(g, 1, 5, 1, 66)
    print (paths)
