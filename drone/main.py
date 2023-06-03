from  drone import * 

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import pandas as pd

from pyvis.network import Network

from IPython.display import IFrame

import copy
import os
import glob
import numpy as np
import imageio


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
    node_positions = nx.spring_layout(G)  # compute node positions
    plt.figure(figsize=(8, 6))
    #plot cost as title
    plt.title('Model Drone: Total cost:' + str(cost) + " $")
    nx.draw(G, pos=node_positions, node_size=10, node_color='black', alpha=1.0, width=1.0, with_labels=False)
    plt.show()

    # Animation part
    visit_colors = {1:'black', 2:'red', 3:'blue'}
    edge_cnter = {}
    

    # ensure the directory for the images exists
    if not os.path.exists('fig/png/'):
        os.makedirs('fig/png/')

    if not os.path.exists('fig/gif/'):
        os.makedirs('fig/gif/')

    for i, e in enumerate(circuit, start=1):
        edge = frozenset([e[0], e[1]])
        if edge in edge_cnter:
            edge_cnter[edge] += 1
        else:
            edge_cnter[edge] = 1

        # Full graph (faded in background)
        nx.draw_networkx(G, pos=node_positions, node_size=6, node_color='gray', with_labels=False, alpha=0.07)

        # Edges walked as of iteration i
        circuit_i = copy.deepcopy(circuit[0:i])
        g_i = nx.Graph()
        for edge_i in circuit_i:
            visits_i = edge_cnter[frozenset(edge_i)]
            g_i.add_edge(edge_i[0], edge_i[1], visits_i=visits_i)
        g_i_edge_colors = [visit_colors[e[2].get('visits_i', 1)] for e in g_i.edges(data=True)]

        nx.draw_networkx_nodes(g_i, pos=node_positions, node_size=6, alpha=0.6, node_color='lightgray', linewidths=0.1)
        nx.draw_networkx_edges(g_i, pos=node_positions, edge_color=g_i_edge_colors, alpha=0.8)

        plt.axis('off')
        plt.savefig('fig/png/img{}.png'.format(i), dpi=120, bbox_inches='tight')
        plt.close()



    # Function to create animation from the generated images
    def make_circuit_video(image_path, movie_filename, fps=5):
    # sorting filenames in order
        filenames = glob.glob(image_path + 'img*.png')
        filenames_sort_indices = np.argsort([int(os.path.basename(filename).split('.')[0][3:]) for filename in filenames])
        filenames = [filenames[i] for i in filenames_sort_indices]

        # make movie
        with imageio.get_writer(movie_filename, mode='I', duration=1000/fps) as writer:
            for filename in filenames:
                image = imageio.v2.imread(filename)
                writer.append_data(image)

    make_circuit_video('fig/png/', 'fig/gif/cpp_route_animation.gif', fps=3)

if __name__ == "__main__":
      main()