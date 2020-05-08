import sys
import networkx as nx
import pickle


mf = 0

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
#TODO: reduce number of maxflows
def pathCost(g: nx.Graph, path):
    global mf
    max_cap = pathCapacity(g, path)
    if max_cap == 0:
        return -1
    flow_with = mf
    flow_without = maxFlowWoPath(g, path, max_cap)
    mf = flow_without
    print(f'path: {path},  overload cost: {(flow_with - flow_without - max_cap)*100//max_cap}, len cost: {len(path)*10//g.number_of_nodes()}')
    return (flow_with - flow_without - max_cap)*100//max_cap + len(path)*10//g.number_of_nodes()

def getNextPath(g: nx.Graph, candidates):
    global mf
    ret = min(candidates, key=lambda x: pathCost(g, x))
    return ret


'''
somehow relate part of capacity taken to path weight
pathCost//200
'''
def optimalCapacity(g: nx.Graph, path):
    return (1 - pathCost(g, path)//200) * pathCapacity(g, path)


'''
Return a dictionary {path_list: path_flow}
'''
def findPaths(g: nx.Graph, fr, to, cap_req=1):
    global mf
    if cap_req > mf:
        print("Denied: no sufficient paths")
        return {}
    capacity, cost = 0, 0
    paths = {}
    candidates = list(nx.all_simple_paths(g, fr, to))

    req_met = False
    while not req_met:
        if len(candidates) == 0:
            break
        mf = nx.maximum_flow(g, fr, to, capacity='cap')[0]
        path = getNextPath(g, candidates)
        path_cost = pathCost(g, path)
        if path_cost == -1:
            candidates.remove(path)
            continue
        cost += path_cost
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
