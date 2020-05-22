def removeCycles(path):
    i = 0
    while i < len(path):
        if path[i] in path[i+1:]:
            j = len(path) - 1
            while path[j] != path[i]:
                j -= 1
            for k in range(i+1, j+1):
                del path[i+1]
        i += 1
    return path
