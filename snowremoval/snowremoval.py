#USED TO  GET THE GRAPH OF THE CITY
import osmnx as ox
#USED TO CREATE THE GRAPH OF THE CITY
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt
from itertools import combinations



# Define the cost model parameters
fixed_cost_snowplow_type1 = 500
cost_per_km_snowplow_type1 = 1.1
hourly_cost_type1_first8hours = 1.1
hourly_cost_type1_after8hours = 1.3
average_speed_type1 = 10


#il faut calculer le sum de tout les edges presents dans le circuit
# multiplier par le cout de drone/km => on a le cout du dronage

#supposons que les drones revoie une nouvelle graphe a deneiger
#ensuite pour snowplow: probleme de transport + cou

def eulerize_directed_graph(graph):
    in_degrees = graph.in_degree()
    out_degrees = graph.out_degree()
    start_nodes = [node for node in graph if out_degrees[node] > in_degrees[node]]
    end_nodes = [node for node in graph if in_degrees[node] > out_degrees[node]]

    if start_nodes == [] and end_nodes == []:
        return graph
    
    eulerized_graph = graph.copy()
    dummy_node = "dummy"
    eulerized_graph.add_node(dummy_node)

    for node in start_nodes:
        eulerized_graph.add_edge(dummy_node, node)

    for node in end_nodes:
        eulerized_graph.add_edge(node, dummy_node)
    #Gp =eulerized_graph.copy()
    #best_matching = nx.Graph(list(nx.max_weight_matching(Gp)))
    #for n,m in best_matching.edges():
    #    path = Gp[m][n]["path"]
    #    eulerized_graph.add_edges_from(nx.utils.pairwise(path))
    return eulerized_graph

def to_eulerian_directed(G, eulerized_graph):
    eulerian_circuit = list(nx.eulerian_circuit(eulerized_graph)) #
    if eulerian_circuit[0][0] == "dummy":
        eulerian_circuit = eulerian_circuit[1:]
    for i in range(len(eulerian_circuit) - 1):
        if eulerian_circuit[i][1] == "dummy":
            short_path = nx.shortest_path(G, eulerian_circuit[i][0], eulerian_circuit[i+1][1])
            short_list = []
            for x in range(len(short_path) - 1):
                short_list.append((short_path[x], short_path[x+1]))
            eulerian_circuit[i:i+2] = short_list
    if eulerian_circuit[len(eulerian_circuit) - 1][1] == "dummy":
        eulerian_circuit = eulerian_circuit[:len(eulerian_circuit) - 1]
    return eulerian_circuit


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
#pos = nx.spring_layout(G2)
#nx.draw_networkx(G2, arrows=True, **options)
#plt.show()


        
def cost_snow_removal(G, snowplow_paths):

    '''
    # Define the cost model parameters
    fixed_cost_drone = 100
    cost_per_km_drone = 0.01
    fixed_cost_snowplow_type1 = 500
    cost_per_km_snowplow_type1 = 1.1
    hourly_cost_type1_first8hours = 1.1
    hourly_cost_type1_after8hours = 1.3
    average_speed_type1 = 10
    # Calculate the cost of snow removal operations
    cost_snow_removal = 0
    for sector in sectors:
        for i in range(len(snowplow_paths[sector])):
            if i < 8:
                cost_snow_removal += nx.resistance_distance(G, snowplow_paths[sector][i], snowplow_paths[sector][i+1]) * cost_per_km_snowplow_type1 
            else:
                cost_snow_removal += nx.resistance_distance(G, snowplow_paths[sector][i], snowplow_paths[sector][i+1]) * cost_per_km_snowplow_type1 * 1.3
    cost_snow_removal += fixed_cost_snowplow_type1
    return cost_snow_removal
    '''



