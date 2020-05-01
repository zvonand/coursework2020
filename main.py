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
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    flow_without = maxFlowWoPath(g, path, max_cap)
    if flow_without == 0:
        return -1
    return (flow_with - flow_without - max_cap)*100//max_cap + len(path)*100//g.number_of_nodes()

def getNextPath(g: nx.Graph, candidates):
    return candidates[0]


'''
somehow relate part of capacity taken to path weight
pathCost//200
'''
def optimalCapacity(g: nx.Graph, path):
    return (1 - pathCost(g, path)//200) * pathCapacity(g, path)


'''
Returnd a dictionary {path_list: path_flow}
'''
def findPaths(g: nx.Graph, fr, to, cap_req=1):
    capacity, cost = 0, 0
    paths = {}
    candidates = list(nx.all_simple_paths(g, fr, to))
    candidates.sort(key=lambda x: pathCost(g, x))

    req_met = False
    while not req_met:
        if len(candidates) == 0:
            return {}
        path = getNextPath(g, candidates)
        cost += pathCost(g, path)
        path_cap = optimalCapacity(g, path)
        if path_cap >= (cap_req - capacity):
            path_cap = cap_req - capacity
        paths[tuple(path)] = path_cap
        removePath(g, path, path_cap)
        capacity += path_cap

        candidates.remove(path)
        if capacity >= cap_req:
            req_met = True
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

    # print(g[1][8]['cap'])
    print(findPaths(g, 1, 8, 23))
    print(findPaths(g, 1, 8, 33))
    # print(g[1][8]['cap'])
