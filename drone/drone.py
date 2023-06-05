import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

import geopy.distance 

import folium

from networkx.algorithms.matching import max_weight_matching

import itertools


import pandas as pd



'''
def multigraph_to_max_weight_graph(G):
    F = nx.Graph()
    for u, v, data in G.edges(data=True):
        if F.has_edge(u, v):
            F[u][v]['weight'] = max(data.get('weight', 1), F[u][v]['weight'])
        else:
            F.add_edge(u, v, weight=data.get('weight', 1))
    return F
'''


def toaug(graph, min_weight_pairs):
    """
    Add the minimum weight matching edges to the original graph.
    Parameters:
        graph: NetworkX graph (original graph from trailmap)
        min_weight_pairs: list of tuples representing node pairs from the minimum weight matching
    Returns:
        Augmented NetworkX graph
    """
    augmented_graph = nx.MultiGraph(graph.copy())
    for pair in min_weight_pairs:
        augmented_graph.add_edge(pair[0],
                                pair[1],
                                attr_dict={'distance': nx.dijkstra_path_length(graph, pair[0], pair[1]),
                                           'trail': 'augmented'}
                               )
    return augmented_graph



def shortest(graph, node_pairs, weight_name):
    """Compute the shortest distance between each pair of nodes in a graph. Return a dictionary keyed on node pairs (tuples)."""
    distances = {}
    for pair in node_pairs:
        distances[pair] = nx.dijkstra_path_length(graph, pair[0], pair[1], weight=weight_name)
    return distances


def tocomplete(edge_weights, flip_weights=True):
    """
    Create a completely connected graph using a list of vertex pairs and the shortest path distances between them.
    Parameters:
        edge_weights: list of tuples from the output of get_shortest_paths
        flip_weights: Boolean. Should we negate the edge attribute in edge_weights?
    """
    graph = nx.Graph()
    for pair, weight in edge_weights.items():
        weight_i = -weight if flip_weights else weight
        graph.add_edge(pair[0], pair[1], attr_dict={'distance': weight, 'weight': weight_i})
    return graph


def tocircuit(augmented_graph, original_graph, starting_node=None):
    """Create the Eulerian path using only edges from the original graph."""
    eulerian_circuit = []
    naive_circuit = list(nx.eulerian_circuit(augmented_graph, source=starting_node))

    for edge in naive_circuit:
        edge_data = augmented_graph.get_edge_data(edge[0], edge[1])

        if 'trail' in edge_data[0] and edge_data[0]['trail'] != 'augmented':
            # If `edge` exists in the original graph, grab the edge attributes and add them to the Eulerian circuit.
            edge_attributes = original_graph[edge[0]][edge[1]]
            eulerian_circuit.append((edge[0], edge[1], edge_attributes))
        else:
            shortest_path = nx.shortest_path(original_graph, edge[0], edge[1], weight='distance')
            shortest_path_pairs = list(zip(shortest_path[:-1], shortest_path[1:]))

            # If `edge` does not exist in the original graph, find the shortest path between its nodes and
            # add the edge attributes for each link in the shortest path.
            for edge_aug in shortest_path_pairs:
                edge_aug_attributes = original_graph[edge_aug[0]][edge_aug[1]]
                eulerian_circuit.append((edge_aug[0], edge_aug[1], edge_aug_attributes))

    return eulerian_circuit


# Drone Circuit: Optimized
def drone2(graph, starting_node=None):

    # Find nodes of odd degree
    nodes_odd_degree = [v for v, d in graph.degree() if d % 2 == 1]

    # Compute node pairs
    odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))

    # Compute shortest paths. Return a dictionary with node pairs as keys and a single value equal to the shortest path distance.
    odd_node_pairs_shortest_paths = shortest(graph, odd_node_pairs, 'distance')

    # Generate the complete graph
    g_odd_complete = tocomplete(odd_node_pairs_shortest_paths, flip_weights=True)

    # Apply the maximum weight matching
    matching = max_weight_matching(g_odd_complete, True)

    #You convert this dictionary to a list of tuples since you have an undirected graph and order does not matter.
    # Removing duplicates yields the unique 18 edge-pairs that cumulatively sum to the least possible distance.
    odd_matching = list(pd.unique([tuple(sorted([k, v])) for k, v in matching]))

    # Add the minimum weight matching edges to the graph
    augmented_graph = toaug(graph, odd_matching)

    # Create the Eulerian circuit
    circuit = tocircuit(augmented_graph, graph, starting_node)

    return circuit


# Drone Circuit: Normal
def drone(G):
    e_graph = nx.eulerize(G.copy())
    circuit = list(nx.eulerian_circuit(e_graph))
    return circuit 

# Define the cost of drone 
fixed_cost_drone = 100 
cost_per_km_drone = 0.01


def cost_drone(G , circuit):
    #Print fixed cost 
    print(" The fixed cost of the drone is: " + str(fixed_cost_drone) + " $")
    cost =  fixed_cost_drone
    COUNT=0
    print("------------Adding cost to edges-----------------")
    for i in range(len(circuit)):
        node1 = circuit[i][0]
        node2 = circuit[i][1]
        # Get the coordinates of the nodes
        coords_1 = (G.nodes[node1]['y'], G.nodes[node1]['x'])
        coords_2 = (G.nodes[node2]['y'], G.nodes[node2]['x'])
        
        # Calculate and print the distance+ cost
        distance = geopy.distance.geodesic(coords_1, coords_2).km
        print(f"The distance from node {node1} to node {node2} is {distance} km")
        print(f"The cost of the drone from  {node1} to node {node2} is {distance*cost_per_km_drone}")
        cost += (distance * cost_per_km_drone)
        COUNT+=1

        #Plot cost on edge
        #nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G),  edge_labels={(circuit[i][0], circuit[i][1]):
        #                distance * cost_per_km_drone})

    print(" The total cost of the drone is: " + str(cost) + " $")
    print(" The total number of edges is: " + str(COUNT))
    return cost , COUNT 
