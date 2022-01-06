import pandas as pd
import matplotlib.pyplot as plt
import random
import math
import numpy as np


def read_input(name):

    data = pd.read_csv(name, sep=";")
    x = data['x'].to_list()
    y = data['y'].to_list()

    return list(zip(x, y))


def calc_km():

    return

def calc_distance(node, current_node):
    distance = math.sqrt((node[0] - current_node[0]) ** 2 + ((node[1] - current_node[1]) ** 2))

    return distance


def find_nearest_neighbor(current_node, unvisited_nodes):
    distances = [] # list of distances
    for node in unvisited_nodes:
        distance = calc_distance(node, current_node)
        distances.append(distance)

    index_min_distance = np.argmin(distances) # index of shortest distance

    return unvisited_nodes[index_min_distance], distances[index_min_distance]


def TSP_by_NN(nodes):
    # vstup - uzly
    # vystup - delka hamiltonovske kruznice, uzly v poradi kruznice

    status = ["N"]*len(nodes) # vytvoreni seznamu status pro vsechny uzly
    path_length = 0 # delka ham kruznice
    path = [] # ham kruznice


    current_node = nodes[random.randrange(0, len(nodes))] # create random starting point

    while len([i for i in status if i == "N"]) > 1:
        # set status of current node = "Z"
        node_index = nodes.index(current_node)
        status[node_index] = "Z"

        # create list of unvisited nodes
        unvisited_nodes = []
        for i in range(len(status)):
            if status[i] == "N":
                unvisited_nodes.append(nodes[i])

        next_node, distance = find_nearest_neighbor(current_node, unvisited_nodes)

        path_length += distance  # updates length of hamiltonian circuit
        path.append(current_node)  # append current node to path

        current_node = next_node

        #plt.scatter([p[0] for p in nodes], [p[1] for p in nodes])
        #plot_result(path)

    #path.append(current_node)
    path.append(path[0])
    path_length += calc_distance(path[0], current_node)

    return path, path_length


def plot_result(path):
    plt.scatter([p[0] for p in path], [p[1] for p in path])
    for i in range(len(path) - 1):
        plt.plot((path[i][0], path[i+1][0]), (path[i][1], path[i+1][1]), color="red")
    #plt.plot((path[0][0], path[-1][0]), (path[0][1], path[-1][1]), color="red") # spojeni zacatku a konce

    plt.plot()
    #plt.gca().set_aspect('equal', adjustable='box') # aby výsledek nebyl zkreslený
    plt.show()


def TSP_by_best_insertion(nodes):

    status = ["N"] * len(nodes)
    path = [] # hamiltonian circuit

    # find three nodes as the starting hamiltonian circuit
    while len(path) < 4:
        random_node = nodes[random.randrange(0, len(nodes))]
        node_index = nodes.index(random_node)
        # if node is open, append to hamiltonian circuit and set his status to closed
        if status[node_index] == "N":
            path.append(random_node)
            status[node_index] = "Z"

    # calculate length of starting ham cycle
    path_length = calc_distance(path[0], path[1]) + calc_distance(path[1], path[2]) + calc_distance(path[2], path[0])

    while len([i for i in status if i == "N"]) > 1:
        unvisited_nodes = [nodes[i] for i in range(len(status)) if status[i] == "N"]
        random_node = unvisited_nodes[random.randrange(0, len(unvisited_nodes))]

        distance_changes = []

        for i in range(len(path)):
            i2 = i + 1 if i != len(path)-1 else 0
            distance_change = calc_distance(random_node, path[i]) + calc_distance(random_node, path[i2]) - calc_distance(path[i], path[i2])
            distance_changes.append(distance_change)

        index_min_distance = np.argmin(distance_changes)

        path.insert(index_min_distance + 1, random_node)
        path_length += distance_changes[index_min_distance]
        status[nodes.index(random_node)] = "Z"
        path.append(path[0]) # for connecting during visualization

    return path, path_length

if __name__ == "__main__":

    nodes = read_input("data.csv") # vstup

    # visualize data
    #plt.scatter([p[0] for p in nodes], [p[1] for p in nodes])
    #plt.show()

    path_NN, path_length_NN = TSP_by_NN(nodes)

    paths_BN = []
    path_lengths_BN = []
    for result in range(10):
        path_BN, path_length_BN = TSP_by_best_insertion(nodes)
        paths_BN.append(path_BN)
        path_lengths_BN.append(path_length_BN)

    ## NN results
    print("NN")
    print(path_length_NN)
    plot_result(path_NN)
    
    ## BN results
    print("BN")
    print(path_lengths_BN)
    plot_result(path_BN)
