def bfs(edges,start):
    #print(edges)
    order = []
    final_path = []
    visited = set()
    queue = [(start,-1)]
    while queue:
        node,parent = queue.pop(0)
        if node not in visited:
            if parent != -1:
                order.append((parent,node))
            visited.add(node)
            for kid,w in edges[node]:
                queue.append((kid,node))

    if not order:
        order = [(start,start)]
        
    final_path = order[:]
    return order,final_path
