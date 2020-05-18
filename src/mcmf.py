import sys
import networkx as nx
import pickle
import copy

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

def maxFlowWoPath(g: nx.Graph, path, path_cap=-1):
    if path_cap == -1:
        path_cap = pathCapacity(g, path)
    removePath(g, path, path_cap)
    flow = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    addPath(g, path, path_cap)
    return flow

def pathCost(g: nx.Graph, path):
    max_cap = pathCapacity(g, path)
    if max_cap == 0:
        return -1
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    flow_without = maxFlowWoPath(g, path, max_cap)
    #print(f'path: {path},  overload cost: {(flow_with - flow_without - max_cap)*100//max_cap}, len cost: {len(path)*10//g.number_of_nodes()}')
    return (flow_with - flow_without - max_cap)*100//max_cap + len(path)*10//g.number_of_nodes()

def getNPaths(g: nx.Graph, fr, to, path_num: int):
    graph = copy.deepcopy(g)
    size = len(graph.edges())
    max_node = size
    edges = list(graph.edges)
    for a, b in edges:
        mul = 0
        if graph[a][b]['cap'] != 0:
            mul = 1000 / graph[a][b]['cap']
            graph[a][b]['cap'] = 1
        for i in range(1, path_num):
            graph.add_edge(a, max_node + i - 1, cap=1, weight=(i+1)*mul)
            graph.add_edge(max_node + i - 1, b, cap=1, weight=0)
        max_node += path_num - 1

    sink = graph.number_of_nodes()+1
    graph.add_edge(to, sink, cap=path_num)
    mfmc = nx.max_flow_min_cost(graph, fr, sink, capacity='cap', weight='wt')
    #print(mfmc)
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

        pth = []
        for elem in path:
            if elem < size and not (elem in pth):
                pth.append(elem)

        if not pth in paths:
            paths.append(pth)
    return paths

def balanceCapacities(g: nx.Graph, paths, req):
    ret = {}
    cap = 0
    while paths != []:
        if (cap == req):
            return ret
        path = min(paths, key=lambda x: pathCost(g, x))
        pc = pathCapacity(g, path)
        ret[tuple(path)] = min(pc, req-cap)
        cap += ret[tuple(path)]
        removePath(g, path, ret[tuple(path)])
        paths.remove(path)
    if cap < req:
        return {}
    return ret


def findPaths(g: nx.Graph, fr, to, req = 10, path_num = 4):
    mf = nx.maximum_flow(g, fr, to, capacity='cap')[0]
    if req > mf or req == 0:
        return 0
    paths = getNPaths(g, fr, to, path_num)
    paths = balanceCapacities(g, paths, req)
    print(paths)
    return paths
