#!/usr/bin/env python3

import sys
import networkx as nx
import pickle


def mcmf_mod(graph: nx.Graph, fr, to, path_num: int):
    size = len(graph.edges())
    max_node = size
    for a, b, data in graph.edges(data=True):
        data['cap'] = 1
        data['wt'] = 0
        for i in range(1, path_num):
            graph.add_edge(a, max_node + i - 1, cap=1, weight=i)
            graph.add_edge(max_node + i - 1, b, cap=1, weight=0)
        max_node += path_num - 1

    mfmc = nx.max_flow_min_cost(graph, fr, to, capacity='cap', weight='wt')
    paths = []
    finish = to

    for counter in range(path_num):
        i = fr
        path = [fr]
        while i != finish:
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

    paths = mcmf_mod(g, 1, 5, 3)
    print (paths)
