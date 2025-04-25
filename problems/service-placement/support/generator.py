"""
SPDX-FileCopyrightText: 2024 Noé Godinho <noe@dei.uc.pt>

SPDX-License-Identifier: Apache-2.0
"""


import matplotlib.pyplot as plt
import networkx as nx
import random


def visualise_graph(G):
    pos = {0: [0, 0.25], 1: [1, 0.5], 2: [1, 0], 3: [2, 0.5], 4: [2, 0], 5: [3, 0.25]}
    nx.draw(G, pos=pos, with_labels=True)

    plt.show()


def generate_problem(filename, edge_probability=1):
    G = nx.Graph()
    connected = False

    while not connected:
        num_nodes = random.randint(5, 100)
        
        for i in range(num_nodes):
            G.add_node(i)
            G.nodes[i]['cpu'] = random.randint(100, 1000)
            G.nodes[i]['ram'] = random.randint(100, 1000)
            G.nodes[i]['processing'] = random.random()

        for u in range(num_nodes):
            for v in range(num_nodes):
                if u != v:
                    if random.random() < edge_probability:
                        G.add_edge(u, v)
                        G.edges[u, v]['bandwidth'] = random.randint(100, 1000)
                        G.edges[u, v]['latency'] = random.random()

        connected = nx.is_connected(G)

    requests = []
    num_requests = random.randint(1, 100)
    for i in range(num_requests):
        source = random.randint(0, num_nodes-1)
        destination = random.randint(0, num_nodes-1)
        while destination == source:
            destination = random.randint(0, num_nodes-1)

        num_services = random.randint(1, 50)
        services = []
        for j in range(num_services):
            services.append({'cpu': random.randint(10, 100), 'ram': random.randint(10, 100)})

        requests.append({'source': source, 'destination': destination, 'bandwidth': random.randint(10, 100), 'services': services})

    write_to_file(G, requests, filename)


def generate_base_problem():
    G = nx.Graph()

    for i in range(6):
        G.add_node(i)
        G.nodes[i]['cpu'] = 1000
        G.nodes[i]['ram'] = 512
        G.nodes[i]['processing'] = 0.1
    
    G.add_edge(0,1)
    G.edges[0,1]['bandwidth'] = 1000
    G.edges[0,1]['latency'] = 0.1
    G.add_edge(0,2)
    G.edges[0,2]['bandwidth'] = 1000
    G.edges[0,2]['latency'] = 0.2
    G.add_edge(1,3)
    G.edges[1,3]['bandwidth'] = 100
    G.edges[1,3]['latency'] = 0.1
    G.add_edge(1,4)
    G.edges[1,4]['bandwidth'] = 1000
    G.edges[1,4]['latency'] = 0.2
    G.add_edge(2,4)
    G.edges[2,4]['bandwidth'] = 1000
    G.edges[2,4]['latency'] = 0.2
    G.add_edge(3,5)
    G.edges[3,5]['bandwidth'] = 1000
    G.edges[3,5]['latency'] = 0.1
    G.add_edge(4,5)
    G.edges[4,5]['bandwidth'] = 1000
    G.edges[4,5]['latency'] = 0.2

    requests = [{'source': 0, 'destination': 5, 'bandwidth': 500, 'services': [{'cpu': 100, 'ram': 100}]}, {'source': 0, 'destination': 5, 'bandwidth': 100, 'services': [{'cpu': 100, 'ram': 100}, {'cpu': 100, 'ram': 100}]}]

    write_to_file(G, requests, "../data/base")
    generate_solution_base_problem()

    visualise_graph(G)


def generate_solution_base_problem():
    with open("../data/solution_base.txt", 'w') as file:
        file.write("0,1,4,5\n")
        file.write("0\n")
        file.write("0,1,3,5\n")
        file.write("0\n")
        file.write("0\n")


def write_to_file(G, requests, filename):
    with open(filename + ".txt", 'w') as file:
        file.write(str(G.number_of_nodes()) + "\n")
        for i in list(G.nodes):
            string = str(i) + "," + str(G.nodes[i]['cpu']) + "," + str(G.nodes[i]['ram']) + "," + str(G.nodes[i]['processing']) + "\n"
            file.write(string)
        
        file.write(str(G.number_of_edges()) + "\n")
        for (i,j) in list(G.edges):
            string = str(i) + "," + str(j) + "," + str(G.edges[i,j]['bandwidth']) + "," + str(G.edges[i,j]['latency']) + "\n"
            file.write(string)

        file.write(str(len(requests)) + "\n")
        for i in range(len(requests)):
            file.write(str(requests[i]['source']) + "," + str(requests[i]['destination']) + "," + str(requests[i]['bandwidth']) + "\n")
            file.write(str(len(requests[i]['services'])) + "\n")
            
            for j in range(len(requests[i]['services'])):
                file.write(str(requests[i]['services'][j]['cpu']) + "," + str(requests[i]['services'][j]['ram']) + "\n")


if __name__ == '__main__':
    generate_base_problem()
    generate_problem("../data/graph")
