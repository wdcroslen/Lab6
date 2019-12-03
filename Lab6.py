#Lab 6
#from scipy.interpolate import interp1d
class DisjointSetForest:
   def __init__(self, n):
       self.forest = [-1] * n

   def is_index_valid(self, index):
       return 0 <= index < len(self.forest)

   def find(self, a):
       if not self.is_index_valid(a):
           return -1

       if self.forest[a] < 0:
           return a

       self.forest[a] = self.find(self.forest[a])  # Path compression

       return self.forest[a]

   def union(self, a, b):
       ra = self.find(a)
       rb = self.find(b)

       if ra != rb:
           self.forest[rb] = ra

   def in_same_set(self, a, b):
       if self.find(a) == self.find(b):
           return True
       return False

   def __str__(self):
       return str(self.forest)

class Queue:
    def __init__(self):
        self.queue = []
        #self.numkeys
        
    def put(self,k):
        self.queue.append(k)
    
    def get(self):
        if not self.is_empty():
            a = self.queue[0]
            del self.queue[0]
            return a
        else:
            #valueError exception
            raise ValueError("THAT DOES NOT EXIST")
            
    def is_empty(self):
        return len(self.queue) == 0
    
    
    
class GraphAM:

    def __init__(self, vertices, weighted=False, directed=False):
        self.am = []

        for i in range(vertices):  # Assumption / Design Decision: 0 represents non-existing edge
            self.am.append([0] * vertices)

        self.directed = directed
        self.weighted = weighted
        self.representation = 'AM'

    def is_valid_vertex(self, u):
        return 0 <= u < len(self.am)

    def insert_vertex(self):
        for lst in self.am:
            lst.append(0)

        new_row = [0] * (len(self.am) + 1)  # Assumption / Design Decision: 0 represents non-existing edge
        self.am.append(new_row)

        return len(self.am) - 1  # Return new vertex id

    def insert_edge(self, src, dest, weight=1):
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return

        self.am[src][dest] = weight

        if not self.directed:
            self.am[dest][src] = weight

    def delete_edge(self, src, dest):
        self.insert_edge(src, dest, 0)

    def num_vertices(self):
        return len(self.am)

    def vertices_reachable_from(self, src):
        reachable_vertices = set()

        for i in range(len(self.am)):
            if self.am[src][i] != 0:
                reachable_vertices.add(i)

        return reachable_vertices

#    def display(self):
##        print('[', end='')
#        print("[")
#        for i in range(len(self.am)):
##            print('[', end='')
#            print("[")
#            for j in range(len(self.am[i])):
#                edge = self.am[i][j]
#                if edge != 0:
#                    print('(' + str(j) + ',' + str(edge) + ')')
##            print(']', end=' ')
#            print("]")
##        print(']')
#        print(self.am)



    #original Display method
    def display(self):
        print('[', end='')
        for i in range(len(self.al)):
            print('[', end='')
            for edge in self.al[i]:
                print('(' + str(edge.dest) + ',' + str(edge.weight) + ')', end='')
            print(']', end=' ')
        print(']')
    
    
    
    def contains_cycle(self):
       dsf = DisjointSetForest(self.num_vertices())
       for i in range(len(self.am)):
           for j in range(len(self.am)):
               if self.am[i][j] != 0:
                   if dsf.find(i) == dsf.find(j):
                       return True
                   dsf.union(i, j)
       return False
        
        
        
    def every_indegree(self):#makes a list of all number of indegrees for all edges
        lista = [] 
        for i in range(len(self.am)):
            count = 0
            for j in range(len(self.am[i])):
                if self.am[i][j]!= 0:
                    count+=1
            lista.append(count)
        print(lista)
        return lista
    
    def weights(self):
        dict = {}
        for i in range(len(self.am)):
            for j in range(len(self.am[i])):
                if self.am[i][j] != 0:
                    dict[(i, j)] = self.am[i][j]
        return dict

        
    ########################
    ########################
    ########################
    ########################
    
def topological_sort(graph):
    allin = graph.every_indegree() #list of all in degrees 
    result = [] 
    q=Queue() 
    for i in range(len(allin)):
        if allin[i]:
            q.put(i) #enqueue
    while not q.is_empty():
        u = q.get() #dequeue
        result.append(u)
        for adj_vertex in graph.vertices_reachable_from(u):
            allin[adj_vertex] -=1
            if allin[adj_vertex]==0:
                q.put(adj_vertex)
    return result

def kruskals(graph):
    new_graph = GraphAM(graph.num_vertices(), weighted=True, directed=True)
    dict = graph.weights() #dictionary with src and dest as key to the weight as the value
    list = []
    for i in dict:
        if dict[i] not in list:
            list.append(dict[i])
    list.sort()
    for i in list:
        for j in dict:
            if dict[j] == i:
                new_graph.insert_edge(j[0], j[1], i)
                if new_graph.contains_cycle():
                    new_graph.delete_edge(j[0], j[1])
    return new_graph


if __name__ == "__main__":
    g = GraphAM(6)
    g.insert_edge(0, 1)
    g.insert_edge(0, 2)
    g.insert_edge(1, 2)
    g.insert_edge(2, 3)
    g.insert_edge(3, 4)
    g.insert_edge(4, 1)
    g.display()
    g.delete_edge(1, 2)
    topological_sort(g)
    g.display()
    

    g = GraphAM(6, weighted=True, directed=True)
    g.insert_edge(0, 1, 4)
    g.insert_edge(0, 2, 3)
    g.insert_edge(1, 2, 2)
    g.insert_edge(2, 3, 1)
    g.insert_edge(3, 4, 5)
    g.insert_edge(4, 1, 4)  
    g.display()
    kruskals(g).display()

