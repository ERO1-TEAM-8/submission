#USED TO  GET THE GRAPH OF THE CITY
import osmnx as ox
#USED TO CREATE THE GRAPH OF THE CITY
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt
from itertools import combinations
import folium

from drone import *

# Define the cost model parameters
fixed_cost_snowplow_type1 = 500
cost_per_km_snowplow_type1 = 1.1
hourly_cost_type1_first8hours = 1.1
hourly_cost_type1_after8hours = 1.3
average_speed_type1 = 10


#il faut calculer le sum de tout les edges presents dans le circuit
# multiplier par le cout de drone/km => on a le cout du dronage

#supposons que les drones revoie une nouvelle graphe a deneiger
#ensuite pour snowplow: probleme de transport + cout
G2 = nx.DiGraph() # ca ca permet de faire un graph oriente
G2.add_edges_from([('1', '2'), ('2', '3'), ('3', '1'), ('3', '4'), ('4', '5'), ('5', '1')])

def eulerize_preserving_direction(G):
    # Create a new graph
    eulerized_G = nx.DiGraph()

    # Iterate over each node in the original graph
    for node in G.nodes():
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)

        # If in-degree is greater than out-degree, add out-degree-in-degree additional edges
        if in_degree > out_degree:
            for _ in range(in_degree - out_degree):
                new_node = f"dummy_{node}"
                eulerized_G.add_edge(node, new_node)

        # If out-degree is greater than in-degree, add out-degree-in-degree additional edges
        elif out_degree > in_degree:
            for _ in range(out_degree - in_degree):
                new_node = f"dummy_{node}"
                eulerized_G.add_edge(new_node, node)

        # Copy existing edges from the original graph
        for successor in G.successors(node):
            eulerized_G.add_edge(node, successor)

    return eulerized_G

options = {
    'node_color': 'yellow',
    'node_size': 500,
    'width': 2,
    'arrowstyle': '-|>',
    'arrowsize': 12,
}

def has_eulerian_circuit(G):
    # Check if the graph is strongly connected
    for node in G.nodes():
        if 'dummy_' in node:
            continue
        if G.in_degree(node) != G.out_degree(node):
            return False

    if not nx.is_strongly_connected(G):
        print(1)
        return False

    # Check if each node has equal in-degree and out-degree

    return True

#print(has_eulerian_circuit(G))
#print(has_eulerian_circuit(nx.eulerize(G)))
#print(has_eulerian_circuit(G2))
#print(list(nx.eulerian_circuit(eulerize_preserving_direction(G2))))
#print(eulerize_preserving_direction(G2).edges)
#G2 = eulerize_preserving_direction(G2)
pos = nx.spring_layout(G2)
nx.draw_networkx(G2, arrows=True, **options)
plt.show()



def snow_removal(Gs):
    # Find the shortest paths for snowplow snow removal in each sector
    circuit = []
    for G in Gs:
        circuit.append(drone(G))
    return circuit
        
def cost_snow_removal(G, snowplow_paths):
    #TODO



# multiplier par le cout de drone/km => on a le cout du dronage

#supposons que les drones revoie une nouvelle graphe a deneiger
#ensuite pour snowplow: probleme de transport + cout


#ox.plot_graph(ox.project_graph(G))

#TODO:Find the shortest paths for snowplow snow removal in each sector


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


