import osmnx as ox
#USED TO CREATE THE GRAPH and to plot it and to get the nodes and edges of the graph + find shortest path
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt

#ville = "Outremont, Montreal, Canada"
#Graph = ox.graph_from_place(ville, network_type='all')
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (1, 5)])

G = G.to_undirected()

def drone(G):
    e_graph = nx.eulerize(G.copy())
    circuit = list(nx.eulerian_circuit(e_graph))
    return circuit

def change_color(G, circuit):
    for i in range(len(circuit)):
        G.add_edge(circuit[i][0],circuit[i][1], color = 'r')
    return G
G = change_color(G, drone(G))
colors = nx.get_edge_attributes(G, 'color').values()
nx.draw(G, edge_color=colors)
ox.plot_graph(ox.project_graph(G))

#TODO:Find the shortest paths for snowplow snow removal in each sector

# Define the cost model parameters
fixed_cost_drone = 100
cost_per_km_drone = 0.01
fixed_cost_snowplow_type1 = 500
cost_per_km_snowplow_type1 = 1.1
hourly_cost_type1_first8hours = 1.1
hourly_cost_type1_after8hours = 1.3
average_speed_type1 = 10
#TODO: ADD THE OTHER PARAMETERS

#TODO:Calculate the cost of snow removal operations

#TODO:Print the cost of snow removal operations

#TODO: Perform simulations and compare costs for different options

#TODO:Simulation option 1: Using type I snowplows

#TODO:Simulation option 2: Using type II snowplows

#TODO:Compare the costs of different options

#TODO:Save the results or visualize the paths

#TODO:Save the drone flight path

#TODO:Save the snowplow paths for each sector

#TODO:Visualize the drone flight

#TODO:Visualize the snowplow paths for each sector

#TODO:Visualize the drone flight and snowplow paths for each sector

#......