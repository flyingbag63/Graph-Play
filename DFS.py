def dfs(edges,start):
    #print('here')
    order = []
    final_path = []
    visited = set()
    stack = [(start,-1)]
    while stack:
        node,parent = stack.pop()
        if node not in visited:
            if parent != -1:
                order.append((parent,node))
            visited.add(node)
            for kid,w in edges[node]:
                stack.append((kid,node))

    if not order:
        order = [(start,start)]
    final_path = order[:]
    return order,final_path
