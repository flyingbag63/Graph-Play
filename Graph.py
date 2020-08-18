from BFS import bfs
from DFS import dfs
from dijkstra import dijkstra
from connected_components import connected_components
from Cycles import find_cycles


class Graph:
    '''A class representing graph
       where nodes are represnted as (x,y) coordinates
    '''
    
    def __init__(self):
        self.edges = {}
        self.order = []                                   #order of edges in which they are chosen while running an algorithm
        self.final_path = []                              #final path chosen by an algorithm

    def rearrange(self):
        new_order = []
        for i in self.order:
            if isinstance(i,str):
                new_order.append(i)
            else:
                new_order.append((i[0],))
                new_order.append(i)
                new_order.append((i[1],))

        new_path = []
        for i in self.final_path:
            if isinstance(i,str):
                new_path.append(i)
            else:
                new_path.append((i[0],))
                new_path.append(i)
                new_path.append((i[1],))

        self.order = new_order[:]
        self.final_path = new_path[:]
    
    def add_node(self,x):
        if x not in self.edges.keys():
            self.edges[x] = []
        
    def add_edge(self,x,y,weight=1):
        #add edge between two nodes
        
        self.edges[x].append((y,1))
        self.edges[y].append((x,1))

    def bfs(self,start):
        #breadth first search of the graph
        self.order,self.final_path = bfs(self.edges,start)
        self.rearrange()

    def dfs(self,start):
        #depth first search of the graph
        self.order,self.final_path = dfs(self.edges,start)
        self.rearrange()
    
    def shortest_path(self,start,end):
        #return shortest path between two nodes using dijkstra
        self.order,self.final_path = dijkstra(self.edges,start,end)
        self.rearrange()

    def connected_components(self):
        #all the connected components of the graph
        self.order,self.final_path = connected_components(self.edges)
        self.rearrange()

    def cycles(self):
        #find and return cycles if present
        #all cycles code is not correct, maybe I will add in future
        self.order,self.final_path = find_cycles(self.edges)
        self.rearrange() 

    def mst(self):
        #Minimum spanning tree of the graph
        pass
