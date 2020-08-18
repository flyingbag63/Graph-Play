import heapq

def dijkstra(edges,start,end):
    #print(edges,start,end)
    order = []
    parents = {}
    heap = []
    heapq.heappush(heap,(0,start,-1))
    visited = set()
    while heap:
        wt,node,parent = heapq.heappop(heap)
        if node not in visited:
            #print(node)
            if parent != -1:
                order.append((parent,node))
            visited.add(node)
            parents[node] = parent
            if node == end:
                break
            
            for kid,w in edges[node]:
                heapq.heappush(heap,(wt+w,kid,node))

    final_path = []
    node = end
    while node != -1:
        if parents[node] == -1:
            break
        
        final_path.append((parents[node],node))
        node = parents[node]

    final_path.reverse()
    #print(final_path)
    return order,final_path
