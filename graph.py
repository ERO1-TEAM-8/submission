#USED TO  GET THE GRAPH OF THE CITY
import osmnx as ox
#USED TO CREATE THE GRAPH OF THE CITY
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt
import folium

# Define the sectors for snow removal planning

sectors_graph = []

def drone(G):
    e_graph = nx.eulerize(G.copy())
    circuit = list(nx.eulerian_circuit(e_graph))
    return circuit #ce circuit la

def change_color(G, circuit):
    for i in range(len(circuit)):
        G.add_edge(circuit[i][0],circuit[i][1], color = 'r')
    return G


#Color each sector with a different color of the graph
def color_sector(G):
    # Define the colors for each sector
    colors = ["red", "blue", "green", "yellow", "orange"]
    # Color each sector with a different color of the graph
    for i in range(len(sectors)):
        for node in G.nodes():
            if str(node) in sectors[i]:
                G.nodes[node]['color'] = colors[i]
    return G



def snow_removal(Gs):
    # Find the shortest paths for snowplow snow removal in each sector
    circuit = []
    for G in Gs:
        circuit.append(drone(G))
    return circuit
        
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


# calculer la distance entre les noeuds du circuit

# calculer le cout de drone/km


# Define the cost model parameters
fixed_cost_drone = 100
cost_per_km_drone = 0.01
fixed_cost_snowplow_type1 = 500
cost_per_km_snowplow_type1 = 1.1
hourly_cost_type1_first8hours = 1.1
hourly_cost_type1_after8hours = 1.3
average_speed_type1 = 10



def cost_drone(G, circuit):
    cost = 0
    for i in range(len(circuit)):
        #print cost per edge using resistance distance 
        print(" The cost of the edge " + str(circuit[i][0]) + " - " + str(circuit[i][1]) + " is: " + str(nx.resistance_distance(G, circuit[i][0], circuit[i][1]) * cost_per_km_drone) + " $")
        cost += nx.resistance_distance(G, circuit[i][0], circuit[i][1]) * cost_per_km_drone
        #plot the cost of the drone  on the edge  
        nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G),  edge_labels={(circuit[i][0], circuit[i][1]): (nx.resistance_distance(G, circuit[i][0], circuit[i][1])) * cost_per_km_drone})
    cost += fixed_cost_drone    
    #print adding fixed cost of drone
    print(" The fixed cost of the drone is: " + str(fixed_cost_drone) + " $")
    print(" The total cost of the drone is: " + str(cost) + " $")
    return cost


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


def main():
    #real graph
    sectors = ["Outremont", "Verdun", "Saint-Léonard", "Rivière-des-prairies-pointe-aux-trembles", "Le Plateau-Mont-Royal"]
    Gs = []
    for i in range(len(sectors)):
        Graph = ox.graph_from_place(sectors[i] + ", Montreal, Canada", network_type='all') # OPTI :certified:
        Graphundirected = Graph.to_undirected()
        Gs.append(Graphundirected)
    

    #demo graph
    #G = nx.Graph()
    #G.add_nodes_from([1, 2, 3, 4, 5])
    #G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (1, 5)])

    #main:
    drone_circuits = []
    for G in Gs:
        print(G)
        drone_circuits.append(drone(G))
    #cost_drone(G, circut)
    snow_circuits = snow_removal(Gs)
    for c in snow_circuits:
        print(c)
    #cost_snow_removal(G, snow_removal(G))
    #nx.draw(
   #    G, nx.spring_layout(G), edge_color=colors, width=1, linewidths=1,
   #    node_size=500, node_color='pink', alpha=0.9,
   #    labels={node: node for node in G.nodes()}
   #)
   # plt.show()
    ox.plot_graph(ox.project_graph(G))



if __name__ == "__main__":
      main()