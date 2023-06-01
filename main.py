from drone import *
from snowremoval import *

#USED TO  GET THE GRAPH OF THE CITY
import osmnx as ox
#USED TO CREATE THE GRAPH OF THE CITY
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt
from itertools import combinations


sectors = []


#----------------------Add colors----------------------#

def change_color(G, circuit):
    for i in range(len(circuit)):
        G.add_edge(circuit[i][0],circuit[i][1], color = 'r')
    return G

def total_len(G, circuit):
    total = 0
    for i in range(len(circuit)):
        total += G.edges[circuit[i][0], circuit[i][1]].get('length')
    #total = total * 0.01
    return total

#Color each sector with a different color of the graph
def color_sector(G , sectors):
    # Define the colors for each sector
    colors = ["red", "blue", "green", "yellow", "orange"]
    # Color each sector with a different color of the graph
    for i in range(len(sectors)):
        for node in G.nodes():
            if str(node) in sectors[i]:
                G.nodes[node]['color'] = colors[i]
    return G

def is_eulerian_digraph(digraph):
    # Create a directed graph from the given graph
    for node in digraph.nodes:
        if digraph.in_degree(node) != digraph.out_degree(node):
            return False
    return True
#----------------------MAIN----------------------#

def main():
    #real graph
    sectors = ["Outremont"]#, "Verdun", "Saint-Léonard", "Rivière-des-prairies-pointe-aux-trembles", "Le Plateau-Mont-Royal"]#
    Gs = []
    #for i in range(len(sectors)):
     #   Graph = ox.graph_from_place(sectors[i] + ", Montreal, Canada", network_type='all') # OPTI :certified:
      #  Graphundirected = Graph.to_undirected()
       # Gs.append(Graphundirected)
    Graph = ox.graph_from_place("Leynhac, France", network_type='all') # OPTI :certified:
    
    Graphundirected = Graph.to_undirected()
    Gs.append(Graphundirected)
    drone_circuits = []
    for G in Gs:
        drone_circuits.append(drone(G))
        cost_drone(G, drone_circuits[0])
        G = change_color(G, drone(G))
        
        colors = nx.get_edge_attributes(G, 'color').values()
        nx.draw(G, edge_color=colors)
        plt.show()
    
    
    #cost_drone(G, circut)
    #snow_circuits = snow_removal(Gs)
    #for c in snow_circuits:
    #    print(c)
    
    G2 = eulerize_directed_graph(Graph)
    print(to_eulerian_directed(Graph, G2))
    #cost_snow_removal(G, snow_removal(G))

   

    #demo graph

    '''
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3, 4, 5])
        G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (1, 5)])
        cost_drone(G, drone(G))
            #nx.draw(
   #    G, nx.spring_layout(G), edge_color=colors, width=1, linewidths=1,
   #    node_size=500, node_color='pink', alpha=0.9,
   #    labels={node: node for node in G.nodes()}
   #)
    '''

   # plt.show()
   # ox.plot_graph(ox.project_graph(G))



if __name__ == "__main__":
      main()