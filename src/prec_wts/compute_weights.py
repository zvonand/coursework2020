#!/usr/bin/env python3

import sys
import os
import networkx as nx
import pickle
import collections


def pathCapacity(g: nx.Graph, path):
    if len(path) <= 1:
        return 0
    capacity = g[path[0]][path[1]]['cap']
    for i in range(1, len(path)-1):
        link_cap =  g[path[i]][path[i+1]]['cap']
        if link_cap < capacity:
            capacity = link_cap
    return capacity

def removePath(g: nx.Graph, path, path_cap):
    for i in range(0, len(path)-1):
        g[path[i]][path[i+1]]['cap'] -= path_cap

def addPath(g: nx.Graph, path, path_cap):
    for i in range(0, len(path)-1):
        g[path[i]][path[i+1]]['cap'] += path_cap

def maxFlowWoPath(g: nx.Graph, path, path_cap):
    removePath(g, path, path_cap)
    flow = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    addPath(g, path, path_cap)
    return flow


def pathCost(g: nx.Graph, path):
    max_cap = pathCapacity(g, path)
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    flow_without = maxFlowWoPath(g, path, max_cap)
    #print(f'overload cost: {(flow_with - flow_without - max_cap)*100 // max_cap}, length cost: {len(path) * 10 // g.number_of_nodes()}')
    return (flow_with - flow_without - max_cap)*100 // max_cap + len(path) * 10 // g.number_of_nodes()





files = []
for tp in os.listdir('topo/'):
    files.append(tp)

files.sort()

for tp in files:
    with open('topo/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    print(f'Processing: {tp}, nodes: {g.number_of_nodes()}, edges: {g.number_of_edges()}')

    wts = {}

    nodes_lst = sorted(list(g.nodes))

    for i in range(len(nodes_lst)-1):
        for j in range(i+1, len(nodes_lst)):
            if g.has_edge(nodes_lst[i], nodes_lst[j]):
                wts[(nodes_lst[i], nodes_lst[j])] = 0

    for i in range(len(nodes_lst)-1):
        for j in range(i+1, len(nodes_lst)):
            paths = nx.all_simple_paths(g, nodes_lst[i], nodes_lst[j])
            for path in paths:
                cost = pathCost(g, path)
                for k in range(len(path) - 1):
                    if path[k] < path[k+1]:
                        wts[(path[k], path[k+1])] += cost
                    else:
                        wts[(path[k+1], path[k])] += cost

    mn, mx = wts[list(g.edges)[0]], wts[list(g.edges)[0]]
    for i in wts.keys():
        if wts[i] < mn:
            mn = wts[i]
        if wts[i] > mx:
            mx = wts[i]

    koeff = 100 / (mx - mn)
    for i in wts.keys():
        wts[i] = int((wts[i] - mn) * koeff)
        g[i[0]][i[1]]['wt'] = wts[i]


    with open('edge_weights/' + tp, 'wb') as fp:
        pickle.dump(g, fp)

    print(f'Done with: {tp}')
