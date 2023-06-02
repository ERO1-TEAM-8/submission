from  drone import * 

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import pandas as pd

from pyvis.network import Network

from IPython.display import IFrame




#----------------------Add colors----------------------#

def change_color(G, circuit , color):
    for i in range(len(circuit)):
        G.add_edge(circuit[i][0],circuit[i][1], color)
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


def max_weight_graph(G):
    G_max = nx.Graph()

    for u, v, data in G.edges(data=True):
        if G_max.has_edge(u,v):
            # compare the 'weight' attribute and keep the edge with the highest weight
            if data['weight'] > G_max[u][v]['weight']:
                G_max[u][v]['weight'] = data['weight']
        else:
            G_max.add_edge(u, v, weight=data['weight'])

    return G_max

#----------------------MAIN----------------------#

def main():
    #real graph

    #pyvis


    Graph = ox.graph_from_place("Leynhac, France", network_type='all') # OPTI :certified:
    G= Graph.to_undirected()
    circuit = drone(G)
    cost =cost_drone(G, circuit)
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    # loop over nodes, add them to the pyvis network, and style them
    for node in G.nodes():
        net.add_node(
        node,
        color="yellow",
        size=10,
        title="Node: " + str(node),
        label="Node " + str(node)
    )

# loop over edges, add them to the pyvis network, and style them
    for edge in G.edges():
        net.add_edge(
        edge[0], 
        edge[1], 
        color="white", 
        width=0.5
    )
    for i in range(len(circuit)):
        net.add_edge(
        circuit[i][0], 
        circuit[i][1], 
        color="red", 
        width=1
    )

    # Add some global settings
    net.barnes_hut()
    net.set_edge_smooth('dynamic')
    net.show_buttons(filter_=['physics'])
    net.show("network.html")

    # In    a Jupyter notebook
    IFrame('network.html', width=800, height=600)

    #plot graph : option

    G = change_color(G, circuit , 'r')
    colors = nx.get_edge_attributes(G, 'color').values()
    plt.figure(figsize=(8, 6))
    #plot cost as title
    plt.title('Model Drone: Total cost:' + str(cost) + " $")
    nx.draw(G , node_size=10, node_color='black', alpha=1.0, width=1.0, with_labels=False)
    plt.show()


    #for u, v, data in G.edges(data=True):
    #data['weight'] = data.get('weight', 0)  # If 'weight' is not in the dictionary, default to 0
    #G_max = max_weight_graph(G)
    #odd_matching_dupes = nx.max_weight_matching(G_max)
    #odd_matching = [tuple(sorted(edge)) for edge in odd_matching_dupes]
    #g_odd_complete_min_edges = nx.Graph(odd_matching)
    #nx.draw(g_odd_complete_min_edges, node_size=20, edge_color='blue', node_color='red')
    #plt.title('Min Weight Matching on Complete Graph')
    #plt.axis('off')
    #plt.show()
    

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