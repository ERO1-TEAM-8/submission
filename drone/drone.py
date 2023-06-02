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


'''
def main():
    #real graph
    sectors = ["Outremont"]#, "Verdun", "Saint-Léonard", "Rivière-des-prairies-pointe-aux-trembles", "Le Plateau-Mont-Royal"]#
    north = 40.806522
    south = 40.802587
    east = -73.941300
    west = -73.946182
    
    Gs = []
    #for i in range(len(sectors)):
    #    Graph = ox.graph_from_place(sectors[i] + ", Montreal, Canada", network_type='all') # OPTI :certified:
    #    Graphundirected = Graph.to_undirected()
    #    Gs.append(Graphundirected)
    #Graph = ox.graph_from_bbox(north, south, east, west, network_type='all') # OPTI :certified:
    Graph = ox.graph_from_place("Saint Laurent de Mure, France", network_type='all') # OPTI :certified:
    Graphundirected = Graph.to_undirected()
    Gs.append(Graphundirected)


    #main:
    #get drone cost 
    drone_circuits = []
    for G in Gs:
        print(G)
        drone_circuits.append(drone(G))
        cost_drone(G, drone_circuits[0])
    
    ox.plot_graph(ox.project_graph(G))

      

     #demo graph

    
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5])
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (1, 5)])

    #plot graph 
    nx.draw(
       G, nx.spring_layout(G), width=1, linewidths=1,
       node_size=500, node_color='pink', alpha=0.9,
       labels={node: node for node in G.nodes()}
   )
   
    
    
if __name__ == "__main__":
      main()

'''