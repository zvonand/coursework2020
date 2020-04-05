#!/usr/bin/env python3

"""
Deploys network with given backbone topology
"""

import argparse
#import netbuilder
#import net_manager
#import network as nk
#import flow_gen as fg
import networkx as nx
#import os
#import ovs
import pickle
#import utils
#import copy
#import matplotlib.pyplot as plt

def get_paths(graph: nx.Graph, fr, to, path_num: int):
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
    parser = argparse.ArgumentParser(
        description='Manage OVS network deployment.'
    )

    # input data
    parser.add_argument('graph', type=str, help='path to graph dump')

    args = parser.parse_args()

    with open(args.graph, 'rb') as fp:
        graph = pickle.load(fp)

    if isinstance(graph, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        graph = nx.Graph(graph)

    paths = get_paths(graph, 1, 5, 3)
    print (paths)
