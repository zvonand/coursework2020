#!/usr/bin/env python3

import sys
import networkx as nx
import pickle



def pathWeight(g: nx.Graph, path):
    if len(path) <= 1:
        return 0
    weight = 0
    for i in range(len(path)-1):
        weight += g[path[i]][path[i+1]]['wt']
    return weight

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


'''
By now, cost is declared as:
    used nodes percentage                   topology overload
(path_length/total_nodes * 100) + (flow_occupance/max_path_capacity * 100)
'''
def pathCost(g: nx.Graph, path):
    max_cap = pathCapacity(g, path)
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')
    flow_without = maxFlowWoPath(g, path, max_cap)
    if flow_without == 0:
        return -1
    return (flow_with - flow_without-max_cap)*100//max_cap + len(path)*100//g.number_of_nodes()





def alg(g: nx.Graph, fr=1, to=1, cap_req=1, paths):
    # capacity = 0
    # paths = {}
    # candidates = nx.all_simple_paths(g, fr, to).sort(key=len)
    #
    # req_met = False
    # while not req_met:
    #     if len(candidates) == 0:
    #         return {}
    #
    #     path = paths[0]




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Usage: main.py [topo_file]')
        sys.exit(1)

    with open(sys.argv[1], 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    # print(g[1][8]['cap'])
    # alg(g)
    # print(g[1][8]['cap'])
