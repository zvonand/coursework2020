#!/usr/bin/env python3

import sys
import os
import networkx as nx
import pickle


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




#tp = 'aaa'
for tp in os.listdir('topo/'):
    print('Processing: ', tp)
    with open('topo/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    wts = {}

    for a in g.nodes:
        for b in g.nodes:
            if a == b:
                continue
            lst = []
            paths = nx.all_simple_paths(g, a, b)
            for path in paths:
                lst.append((path, pathCost(g, path)))
            wts[(a, b)] = lst
    #print(wts)
    with open('path_weights/' + tp, 'wb') as fp:
        pickle.dump(wts, fp)
