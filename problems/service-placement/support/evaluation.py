"""
SPDX-FileCopyrightText: 2024 Noé Godinho <noe@dei.uc.pt>

SPDX-License-Identifier: Apache-2.0
"""


import math
import networkx as nx


def read_problem(filename):
    G = nx.Graph()
    requests = []

    with open(filename + ".txt", 'r') as f:
        num_nodes = int(f.readline().strip())

        for _ in range(num_nodes):
            values = f.readline().strip().split(",")
            node = int(values[0])
            cpu = int(values[1])
            ram = int(values[2])
            processing = float(values[3])

            G.add_node(node)
            G.nodes[node]['cpu'] = cpu
            G.nodes[node]['ram'] = ram
            G.nodes[node]['processing'] = processing

        num_edges = int(f.readline().strip())

        for _ in range(num_edges):
            values = f.readline().strip().split(",")
            u = int(values[0])
            v = int(values[1])
            bandwidth = int(values[2])
            latency = float(values[3])
            G.add_edge(u, v)
            G.edges[u, v]['bandwidth'] = bandwidth
            G.edges[u, v]['latency'] = latency

        num_requests = int(f.readline().strip())

        for i in range(num_requests):
            source, destination, bandwidth = map(int, f.readline().strip().split(","))
            num_services = int(f.readline().strip())
            services = []

            for j in range(num_services):
                cpu, ram = map(int, f.readline().strip().split(","))
                services.append({'cpu': cpu, 'ram': ram})
            
            requests.append({'source': source, 'destination': destination, 'bandwidth': bandwidth, 'services': services})

    return G, requests


def read_solution(filename, requests):
    solution = []

    with open(filename + ".txt", 'r') as f:
        for i in range(len(requests)):
            path = list(map(int, f.readline().strip().split(",")))
            nodes = []

            for j in range(len(requests[i]['services'])):
                node = int(f.readline().strip())
                nodes.append(node)
            
            solution.append({'path': path, 'nodes': nodes})

    return solution


def evaluate_solution(filename_problem, filename_solution):
    G, requests = read_problem(filename_problem)
    solution = read_solution(filename_solution, requests)

    return calc_value(G, requests, solution, 'latency', 'processing')


def calc_value(G, requests, solution, edge_metric, node_metric):
    value = 0
    cpu = [0] * G.number_of_nodes()
    ram = [0] * G.number_of_nodes()
    bandwidth = {(u, v): 0 for u, v in G.edges()}

    if len(requests) != len(solution) or len(solution) == 0:
        return math.inf

    for i in range(len(requests)):
        path = solution[i]['path']
        nodes = solution[i]['nodes']

        if len(path) <= 1 or not nx.is_path(G, path):
            return math.inf

        if path[0] != requests[i]['source'] or path[-1] != requests[i]['destination']:
            return math.inf

        if len(requests[i]['services']) == 0:
            return math.inf

        for j in range(len(path)-1):
            u = path[j]
            v = path[j+1]
            value += G.edges[u, v][edge_metric]
            bandwidth[u, v] += requests[i]['bandwidth']

            if bandwidth[u, v] > G.edges[u, v]['bandwidth']:
                return math.inf

        for j in range(len(requests[i]['services'])):
            node = nodes[j]

            if not G.has_node(node):
                return math.inf

            value += G.nodes[node][node_metric]
            cpu[node] += requests[i]['services'][j]['cpu']
            ram[node] += requests[i]['services'][j]['ram']

            if cpu[node] > G.nodes[node]['cpu'] or ram[node] > G.nodes[node]['ram']:
                return math.inf

    return value


if __name__ == '__main__':
    print(evaluate_solution("../data/base", "../data/solution_base"))