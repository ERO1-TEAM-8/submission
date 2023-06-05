import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopy.distance 
import math


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
        
type1_cost = 500
type2_cost = 800  
type1_km = 1.1
type2_km = 1.3
type1_post8 = 1.3
type2_post8 = 1.5
type1_speed = 10
type2_speed = 20

def opti_type(km, workh, days):
    cost1 = opti_one(km, workh, type1_speed, type1_km, type1_cost, type1_post8)
    cost2 = opti_one(km, workh, type2_speed, type2_km, type2_cost, type2_post8)
    if cost1 < cost2:
        repeat = math.ceil(km / (type1_speed * workh))
        cost = cost1
    else:
        repeat = math.ceil(km / (type2_speed * workh))
        cost = cost2
    
    div_num = repeat / days
    return cost, div_num

def opti_one(km, workh, speed, tkm, cost, post8):
    onedaykm = speed * workh
    repeat = math.floor(km / onedaykm)
    if workh <= 8:
        daycost = cost + tkm * onedaykm
    else:
        daycost = cost + tkm * speed * 8 + post8 * speed * (workh - 8)
    total_cost = repeat * daycost
    last = km % onedaykm
    if last / speed <= 8:
        total_cost += cost + tkm * last
    else:
        total_cost += cost + tkm * speed * 8 + post8 * (last - speed * 8)
    return total_cost
    

def cost_snow_removal(G , circuit):
    print("The cost of the snowplow type I: " + str(type1_cost) + " $"
           + "\n The cost of the snowplow type II: " + str(type2_cost) + " $")
    cost1 =  type1_cost
    cost2 =  type2_cost
    print("------------Adding cost to edges-----------------")
    for i in range(len(circuit)):
        node1 = circuit[i][0]
        node2 = circuit[i][1]
        # Get the coordinates of the nodes
        coords_1 = (G.nodes[node1]['y'], G.nodes[node1]['x'])
        coords_2 = (G.nodes[node2]['y'], G.nodes[node2]['x'])
        
        # Calculate and print the distance+ cost
        distance = geopy.distance.geodesic(coords_1, coords_2).km
        cost1 += (distance * type1_km)
        cost2 += (distance * type2_km)

    if cost1 < cost2:
        print("We are using the snowplow type I, the cost will be: " + str(cost1) + " $")
        return cost1
    print("We are using the snowplow type II, the cost will be: " + str(cost2) + " $")
    return cost2

def snow_removal_km(G, circuit):
    distance = 0
    circuit_km = []
    for (u, v) in range(circuit):
        coords_1 = (G.nodes[u]['y'], G.nodes[u]['x'])
        coords_2 = (G.nodes[v]['y'], G.nodes[v]['x'])
        
        d = geopy.distance.geodesic(coords_1, coords_2).km
        circuit_km.append(d)
        distance += d
    return (distance, circuit_km)

def partition_postman_route(num_parts, circuit, total_km, circuit_km):
    subpaths = []
    subpath = []
    target_km = total_km / num_parts
    subpath_km = 0
    for i in range(len(circuit)):
        edge_km = circuit_km[i]
        subpath.append(circuit[i])
        subpath_km += edge_km

        if subpath_km + edge_km >= target_km and subpath:
            subpaths.append(subpath)
            subpath = []
            subpath_km = 0

    if subpath:
        subpaths.append(subpath)

    return subpaths

