def dfs(node,edges,visited):
    order = []
    final_path = []
    stack = [(node,-1)]
    while stack:
        node,parent = stack.pop()
        if node not in visited:
            if parent != -1:
                order.append((parent,node))
            visited.add(node)
            for kid,w in edges[node]:
                stack.append((kid,node))

    if not order:
        order = [(node,node)]
    else:
        order.append((order[0][1],order[0][0]))
        
    return order

def connected_components(edges):
    order = []
    visited = set()
    for i in edges.keys():
        if i not in visited:
            curr_order = dfs(i,edges,visited)
            order.extend(curr_order)
            order.append('change')

    final_path = order[:]
    #print(order)
    return order,final_path
