#@author: UgurHorasan
import random as rn

class Edge():
    def __init__(self,s,t,weight):
        self.s = s
        self.t = t
        self.weight = weight

    def return_weight(self):
        return self.weight

    def __str__(self):
        return "{} - {} = {}".format(self.s, self.t,self.weight)

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
graph.show_info()

class Agent:
    def __init__(self,graph,start):
        self.graph = graph
        self.start = start
        self.route = []
        self.total_distance = 0
        self.current_place = self.graph.nodes[self.start]
        self.route.append(self.current_place.name)
        self.edge_list = self.graph.list_of_edges
        self.route_and_distance = {}

    def move(self):
        self.possible_paths = {edge.t : edge.weight for edge in self.edge_list if edge.s is self.current_place.name if edge.t not in self.route}
        self.selected_path = rn.choices(list(self.possible_paths.keys()),[1/len(list(self.possible_paths.keys())) for i in range(len(list(self.possible_paths.keys())))],k=1)[0]
        self.current_place = self.graph.nodes[self.selected_path]
        self.route.append(self.current_place.name)
        self.total_distance += self.possible_paths.get(self.current_place.name)

    def change(self,route):
        self.chosen1 = ""
        self.chosen2 = ""
        self.index_chosen1 = 0
        self.index_chosen2 = 0
        while True:
            self.chosen1 = rn.choice(route)
            self.index_chosen1 = route.index(self.chosen1)
            self.chosen2 = rn.choice(route)
            self.index_chosen2 = route.index(self.chosen2)
            if self.index_chosen1 == 0 or self.index_chosen2 == 0 or self.index_chosen1 == self.index_chosen2:
                continue
            else:
                break
        route[self.index_chosen1] = self.chosen2
        route[self.index_chosen2] = self.chosen1
        self.route = route
        self.total_distance = 0
        for i in range(len(self.route)-1):
            for edge in self.edge_list:
                if self.route[i] == edge.s and self.route[i+1] == edge.t:
                    self.total_distance += edge.weight
        self.route_and_distance.clear()
        self.route_and_distance[str(self.route)] = self.total_distance
        print("Route and Distance:",self.route_and_distance)

    def finish(self):
        while len(self.route) != len(self.graph.node_names):
            self.move()
        self.route_and_distance[str(self.route)] = self.total_distance
        if len(self.route) == len(self.graph.node_names):
            self.possible_paths = {edge.t: edge.weight for edge in self.edge_list if edge.s is self.current_place.name
                                   if edge.t is self.start}
            self.selected_path = rn.choices(list(self.possible_paths.keys()),
                                            [1 / len(list(self.possible_paths.keys())) for i in
                                             range(len(list(self.possible_paths.keys())))], k=1)[0]
            self.current_place = self.graph.nodes[self.selected_path]
            self.route.append(self.current_place.name)
            self.total_distance += self.possible_paths.get(self.current_place.name)

class Algorithm:
    def __init__(self,graph,size,iteration,start):
        self.graph = graph
        self.size = size
        self.iteration = iteration
        self.start = start
        self.s_distance = 10000
        self.smallest = []
        self.smallest_route_and_distance = {}
        self.goo()

    def goo(self):
        agent_list = [Agent(graph,self.start) for i in range(self.size)]
        for j in range(len(agent_list)):
            agent_list[j].finish()
            if len(self.smallest) == 0:
                self.smallest = agent_list[j].route
                self.s_distance = agent_list[j].total_distance
            elif agent_list[j].total_distance < self.s_distance:
                self.smallest = agent_list[j].route
                self.s_distance = agent_list[j].total_distance
            #print(agent_list[j].route, agent_list[j].total_distance)
        print("*****************************************")
        print("smallest route:",self.smallest,"smallest distance:",self.s_distance)
        print("*****************************************")

        for ite in range(self.iteration):
            for i in range(len(agent_list)):
                print(agent_list[i].route)
                agent_list[i].change(self.smallest)
                print("route and distance:", agent_list[i].route_and_distance)
                if agent_list[i].total_distance < self.s_distance:
                    self.s_distance = agent_list[i].total_distance
                    self.smallest = agent_list[i].route
                print("shortest:",self.smallest,self.s_distance)
        self.smallest_route_and_distance[str(self.smallest)] = self.s_distance
        print("**********************************************************")
        print("Final Smallest Route and Distance:",self.smallest_route_and_distance)


algorithm = Algorithm(graph,10,100,'A')