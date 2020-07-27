#@author: UgurHorasan
import random as rn

class Edge():
    def __init__(self,s,t,weight):
        self.s = s
        self.t = t
        self.weight = weight
        self.phe = 1

    def return_weight(self):
        return self.weight

    def __str__(self):
        return "{} - {} = {}, phe = {}".format(self.s, self.t,self.weight,self.phe)

class Node():
    def __init__(self,name):
        self.name = name
        self.neighbors = []

class Graph():
    def __init__(self,edge_list):
        self.edge_list = edge_list
        self.list_of_edges = []
        self.create_nodes()
        self.create_graph()
    def create_nodes(self):
        self.node_names = list(set([s for s,t,d in self.edge_list] + [t for s,t,d in self.edge_list]))
        self.nodes = {n : Node(n) for n in self.node_names}
    def create_graph(self):
        for s,t,d in self.edge_list:
            e = Edge(s,t,d)
            self.list_of_edges.append(e)
            self.add_edges(e)
    def add_edges(self,edge):
        self.nodes[edge.s].neighbors.append(edge)
    def show_info(self):
        for edge in self.list_of_edges:
            print(edge)

edge_list = [("A","B",15),("A","C",22),("A","D",35),("A","E",42),("A","F",17),("A","G",45),
             ("B","A",15),("B","C",27),("B","D",28),("B","E",30),("B","F",21),("B","G",8),
             ("C","A",22),("C","B",27),("C","D",9),("C","E",17),("C","F",12),("C","G",42),
             ("D","A",35),("D","B",28),("D","C",9),("D","E",7),("D","F",5),("D","G",23),
             ("E","A",42),("E","B",30),("E","C",17),("E","D",7),("E","F",10),("E","G",18),
             ("F","A",17),("F","B",21),("F","C",12),("F","D",5),("F","E",10),("F","G",12),
             ("G","A",45),("G","B",8),("G","C",42),("G","D",23),("G","E",18),("G","F",12)]
graph = Graph(edge_list)

class Ant():
    def __init__(self,graph,alpha,beta,start,delta):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.route = []
        self.start = start
        self.current_node = graph.nodes[start]
        self.all_visited = False
        self.finished = False
        self.total_distance = 0
        self.edge_list = self.graph.list_of_edges
        self.route.append(self.current_node.name)

    def move(self):
        if self.all_visited == True:
            self.possible_path = {edge.t: (edge.weight, edge.phe) for edge in self.edge_list if edge.t is self.start}
        else:
            self.possible_path = {edge.t: (edge.weight, edge.phe) for edge in self.edge_list if edge.s is self.current_node.name if edge.t not in self.route}
        self.sum_of_possibilities = 0
        self.list_for_sum = [t for n,t in self.possible_path.items()]
        for weight,phe in self.list_for_sum:
            self.sum_of_possibilities += (phe**self.alpha) / (weight**self.beta)
        self.possibilities = {x : (z**self.alpha / y**self.beta) / self.sum_of_possibilities for x,(y,z) in self.possible_path.items()}
        self.selected_path = rn.choices(list(self.possibilities.keys()),self.possibilities.values(), k=1)[0]
        self.route.append(self.selected_path)
        self.current_node = self.graph.nodes[self.selected_path]

    def go_to_target(self):
        while self.finished != True:
            self.move()
            n1, n2 = self.route[-1], self.route[-2]
            dis = [edge.return_weight() for edge in self.graph.list_of_edges if edge.s == n2 and edge.t == n1]
            self.total_distance += dis[0]
            if len(self.graph.node_names) == len(set(self.route)):
                self.all_visited = True
            if self.all_visited == True and self.route[0] == self.route[-1]:
                self.finished = True

    def deposit(self):
        edges_of_route = []
        for i in range(len(self.route)-1):
            edge = ((self.route[i],self.route[i+1]))
            edges_of_route.append(edge)
        my_list = [edge for edge in edges_of_route]
        for e in self.graph.list_of_edges:
            for i in range(len(my_list)):
                if e.s == my_list[i][0] and e.t == my_list[i][1]:
                    e.phe += self.delta/self.total_distance


class AntColony():
    def __init__(self,graph,alpha,beta,nest_size,iteration,delta=1):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.start = rn.choices(self.graph.node_names,[1/len(self.graph.node_names) for i in range(len(self.graph.node_names))],k=1)[0]
        #self.start = 'A'
        self.nest_size = nest_size
        self.iteration = iteration
        self.optimal_route = ()
        self.apply_ACO()

    def evaporate(self,decay = 0.05):
        for edge in self.graph.list_of_edges:
            edge.phe *= (1-decay)

    def apply_ACO(self):
        list_of_ants = [Ant(self.graph,self.alpha,self.beta,delta = self.delta,start = self.start) for i in range(self.nest_size)]
        self.frequency_list = {}
        self.distance_list = {}
        self.info_list = {}
        for ite in range(self.iteration):
            for ant in list_of_ants:
                ant.go_to_target()
                if ite == self.iteration-1:
                    if str(ant.route) not in list(self.frequency_list.keys()):
                        self.frequency_list[str(ant.route)] = 1
                    else:
                        self.frequency_list[str(ant.route)] += 1
            for ants in list_of_ants:
                ants.deposit()
            self.evaporate()
            list_of_ants = [Ant(self.graph, self.alpha, self.beta, delta=self.delta, start=self.start) for i in range(self.nest_size)]

        for x in list(self.frequency_list.keys()):
            x = list(x)
            x = [a.strip('[]') for a in x]
            x = [a.strip(' ') for a in x]
            x = [a.strip(',') for a in x]
            x = [a.strip("''") for a in x]
            x = [a.strip('') for a in x]
            while "" in x:
                x.remove("")
            sum = 0
            for i in range(len(x) - 1):
                a,b = x[i],x[i+1]
                for j in self.graph.list_of_edges:
                    if j.s == a and j.t == b:
                        sum += j.weight
            self.distance_list[str(x)] = sum

        for a,b in self.distance_list.items():
            for c,d in self.frequency_list.items():
                if a == c:
                    self.info_list[a] = {b:d}

        for k,v in self.info_list.items():
            string1 = k
            for a,b in v.items():
                string2 = "Distance: {} -- Frequency: {}".format(a,b)
            print("Route:",string1,string2)

        list_for_min = [list(b.keys()) for a, b in self.info_list.items()]
        self.minimum = min(list_for_min)[0]

        for k,v in self.info_list.items():
            for v2 in v.keys():
                if v2 == self.minimum:
                    self.optimal_route = (k,v2)

        print("*********************************************")
        print("Optimal Route:",self.optimal_route[0],"Optimal Distance:",self.optimal_route[1])

colony = AntColony(graph,1,1,50,100)
graph.show_info()