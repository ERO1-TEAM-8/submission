#USED TO  GET THE GRAPH OF THE CITY
import osmnx as ox
#USED TO CREATE THE GRAPH OF THE CITY
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt
from itertools import combinations

import geopy.distance 

import folium



#Get the shortest path of  circuit 
def drone(G):
    e_graph = nx.eulerize(G.copy())
    #min weight
    circuit = list(nx.eulerian_circuit(e_graph))
    return circuit 

# Define the cost of drone 
fixed_cost_drone = 100 
cost_per_km_drone = 0.01


def cost_drone(G , circuit):
    #Print fixed cost 
    print(" The fixed cost of the drone is: " + str(fixed_cost_drone) + " $")
    cost =  fixed_cost_drone
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

        #Plot cost on edge
        #nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G),  edge_labels={(circuit[i][0], circuit[i][1]):
        #                distance * cost_per_km_drone})

    print(" The total cost of the drone is: " + str(cost) + " $")
    return cost 
