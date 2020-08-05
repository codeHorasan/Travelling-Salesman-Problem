#@author: ugur_

import matplotlib.pyplot as plt
import random as rn
import numpy as np
import math

def create_random_nodes(length,limit=300):
    strings = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    comp_list = []
    list_of_names = []
    list_of_coor = []
    
    for i in range(length):
        r_string = ''.join(rn.choice(strings) for i in range(5))
        list_of_names.append(r_string)
    
    
    for i in range(length):
        ran_x = np.random.choice(limit)
        ran_y = np.random.choice(limit)
        while (ran_x,ran_y) in list_of_coor:
            ran_x = np.random.choice(limit)
            ran_y = np.random.choice(limit)
        list_of_coor.append((ran_x,ran_y))
        
    
    x_list = []
    y_list = []
    
    for x,y in list_of_coor:
        x_list.append(x)
        y_list.append(y)
    
    figure1 = plt.figure()
    
    axes = figure1.add_axes([0,0,1,1])
    axes.scatter(x_list,y_list)
    plt.plot()
    plt.show()
    
    for i in range(length):
        tup = (list_of_names[i],list_of_coor[i][0],list_of_coor[i][1])
        comp_list.append(tup)
    
    edge_list = []
    
    for name,x,y in comp_list:
        for i in range(len(list_of_coor)):
            if x == list_of_coor[i][0] and y == list_of_coor[i][1]:
                continue
            edge_list.append((name,list_of_names[i],round(math.sqrt((list_of_coor[i][0] - x)**2 +
                              (list_of_coor[i][1] - y)**2))))
            
    return edge_list,x_list,y_list,list_of_names,list_of_coor


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
            

random_nodes = create_random_nodes(10)       
graph = Graph(random_nodes[0])
        

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
        self.nest_size = nest_size
        self.iteration = iteration
        self.apply_ACO()

    def evaporate(self,decay = 0.05):
        for edge in self.graph.list_of_edges:
            edge.phe *= (1-decay)

    def apply_ACO(self):
        list_of_ants = [Ant(self.graph,self.alpha,self.beta,delta = self.delta,start = self.start) for i in range(self.nest_size)]
        self.frequency_list = {}
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
        
        self.op_route = []
        freq = 0
        for k,v in self.frequency_list.items():
            if v>freq:
                freq=v
                self.op_route = k
        print("Optimized Route:",self.op_route,"Frequency:",freq)
        

colony = AntColony(graph,1,1,150,100)
#graph.show_info()

        
def find_coor_best(route):
    route = [r.strip('[]') for r in route]
    route = [r.strip(' ') for r in route]
    route = [r.strip(',') for r in route]
    route = [r.strip("''") for r in route]
    route = [r.strip('') for r in route]
    while "" in route:
        route.remove("")
    li = []
    s = ""
    for i in range(len(route)):
        if len(s) == 5:
            li.append(s)
            s = ""
            s = s + route[i]
        else:
            s = s + route[i]
    
    li.append(li[0])        
    
    
    x_coors = []
    y_coors = []
    
    for i in range(len(li)-1):
        for n in random_nodes[3]:
            if li[i] == n:
                x_coors.append(random_nodes[4][i][0])
                y_coors.append(random_nodes[4][i][1])
    x_coors.append(x_coors[0])
    y_coors.append(y_coors[0])
                
    return x_coors,y_coors
    
    
    
final_x,final_y = find_coor_best(colony.op_route)

figure2 = plt.figure()
axes2 = figure2.add_axes([0,0,1,1])
axes2.scatter(random_nodes[1],random_nodes[2])
plt.plot(final_x,final_y)
plt.show()