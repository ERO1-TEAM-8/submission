import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

import geopy.distance 

import folium

from networkx.algorithms.matching import max_weight_matching



def multigraph_to_max_weight_graph(G):
    F = nx.Graph()
    for u, v, data in G.edges(data=True):
        if F.has_edge(u, v):
            F[u][v]['weight'] = max(data.get('weight', 1), F[u][v]['weight'])
        else:
            F.add_edge(u, v, weight=data.get('weight', 1))
    return F



def add_augmenting_path_to_graph(graph, min_weight_pairs):
    """
    Add the min weight matching edges to the original graph
    Parameters:
        graph: NetworkX graph (original graph from trailmap)
        min_weight_pairs: list[tuples] of node pairs from min weight matching
    Returns:
        augmented NetworkX graph
    """
    # We need to make the augmented graph a MultiGraph so we can add parallel edges
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in min_weight_pairs:
        graph_aug.add_edge(pair[0],
                           pair[1],
                           attr_dict={'distance': nx.dijkstra_path_length(graph, pair[0], pair[1]),
                                      'trail': 'augmented'}
                          )
    return graph_aug


def create_eulerian_circuit(graph_augmented, graph_original, starting_node=None):
    """Create the eulerian path using only edges from the original graph."""
    euler_circuit = []
    naive_circuit = list(nx.eulerian_circuit(graph_augmented, source=starting_node))

    for edge in naive_circuit:
        edge_data = graph_augmented.get_edge_data(edge[0], edge[1])    

        if 'trail' in edge_data[0] and edge_data[0]['trail'] != 'augmented':
            # If `edge` exists in original graph, grab the edge attributes and add to eulerian circuit.
            edge_att = graph_original[edge[0]][edge[1]]
            euler_circuit.append((edge[0], edge[1], edge_att))
        else:
            aug_path = nx.shortest_path(graph_original, edge[0], edge[1], weight='distance')
            aug_path_pairs = list(zip(aug_path[:-1], aug_path[1:]))

            # If `edge` does not exist in original graph, find the shortest path between its nodes and
            #  add the edge attributes for each link in the shortest path.
            for edge_aug in aug_path_pairs:
                edge_aug_att = graph_original[edge_aug[0]][edge_aug[1]]
                euler_circuit.append((edge_aug[0], edge_aug[1], edge_aug_att))

    return euler_circuit



#Get the shortest path of  circuit : opti
def drone2(G, starting_node=None):
    # Convert G to max-weight graph
    G_max_weight = multigraph_to_max_weight_graph(G)
    # Apply max_weight_matching
    matching = max_weight_matching(G_max_weight, maxcardinality=False, weight='weight')
    
    # Add the min weight matching edges to G
    G_aug = add_augmenting_path_to_graph(G, matching)
    
    # Make the graph Eulerian
    e_graph = nx.eulerize(G_aug)
    
    # Create the Eulerian circuit
    circuit = create_eulerian_circuit(e_graph, G, starting_node)

    return circuit



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
    return cost 
