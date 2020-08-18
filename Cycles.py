def find_cycle(parents,start,end):
    #print(parents)
    cycle = []
    while start != end:
        #print(start,end)
        cycle.append(start)
        start = parents[start]

    cycle.append(start)

    return cycle

def find(edges,node,visited):
    stack = [(node,-1)]
    cycles = []
    parents = {}
    parents[node] = -1
    while stack:
        node,parent = stack.pop()
        if node not in visited:
            visited.add(node)
            parents[node] = parent
            for kid,w in edges[node]:
                if kid != parents[node]:
                    if kid in visited:
                        cycles.append(find_cycle(parents,node,kid))
                    else:
                        stack.append((kid,node))

    return cycles

def find_cycles(edges):
    #make dfs ordering of the graph
    #add back edges
    #number of cycles will be number of back edges
    visited = set()
    all_cycles = []
    for i in edges.keys():
        if i not in visited:
            cycles = find(edges,i,visited)
            if cycles:
                all_cycles.extend(cycles)

    order = []
    for cycle in all_cycles:
        #print(cycle)
        for i in range(len(cycle)-1):
            order.append((cycle[i],cycle[i+1]))

        order.append((cycle[-1],cycle[0]))
        order.append('change')
        
    final_path = order[:]

    #print(order)
    return order,final_path

def main():
    n = int(input())
    edges = {}
    for i in range(1,n+1):
        edges[i] = []

    m = int(input())
    for i in range(m):
        x,y = map(int,input().split())
        edges[x].append((y,1))
        edges[y].append((x,1))

    find_cycles(edges)

#main()
