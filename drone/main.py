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
import sys


#----------------------Utilities---------------------#

def change_color(G, circuit , color):
    for i in range(len(circuit)):
        G.add_edge(circuit[i][0],circuit[i][1], color)
    return G

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

def generate_gif(G,circuit,path):
    node_positions = nx.spring_layout(G)  
    visit_colors = {
    1: 'black',
    2: 'red',
    3: 'blue',
    4: 'green',
    5: 'yellow',
    6: 'orange',
    7: 'purple',
    8: 'pink',
    9: 'brown',
    10: 'gray',
    11: 'cyan',
    12: 'magenta',
    13: 'lime',
    14: 'teal',
    15: 'lavender',
    16: 'tan',
    17: 'azure',
    18: 'olive',
    19: 'maroon',
    20: 'navy',
    21: 'aquamarine',
    22: 'turquoise',
    23: 'gold',
    24: 'orchid',
    25: 'crimson',
    26: 'indigo',
    27: 'silver',
    28: 'violet',
    29: 'coral',
    30: 'skyblue',
    31: 'salmon',
    32: 'khaki',
    33: 'darkgreen',
    34: 'hotpink',
    35: 'thistle',
    36: 'lightgray',
    37: 'darkorange',
    38: 'darkviolet',
    39: 'limegreen',
    40: 'darkblue',
    41: 'goldenrod',
    42: 'sienna',
    43: 'mediumorchid',
    44: 'royalblue',
    45: 'palegreen',
    46: 'firebrick',
    47: 'darkkhaki',
    48: 'mediumslateblue',
    49: 'mediumseagreen',
    50: 'darkslategray',
    51: 'indianred',
    52: 'darkslateblue',
    53: 'mediumturquoise',
    54: 'cadetblue',
    55: 'steelblue',
    56: 'orangered',
    57: 'slateblue',
    58: 'darkolivegreen',
    59: 'tomato',
    60: 'darkgoldenrod',
    61: 'mediumaquamarine',
    62: 'cornflowerblue',
    63: 'darkorchid',
    64: 'mediumpurple',
    65: 'darksalmon',
    66: 'beige',
    67: 'blueviolet',
    68: 'azure',
    69: 'lightsteelblue',
    70: 'oldlace',
    71: 'lawngreen',
    72: 'lightseagreen',
    73: 'lightpink',
    74: 'palevioletred',
    75: 'lightsalmon',
    76: 'darkseagreen',
    77: 'lightskyblue',
    78: 'greenyellow',
    }

    edge_cnter = {}
    

    # ensure the directory for the images exists
    if not os.path.exists(path +'/png/'):
        os.makedirs(path+'/png/')

    if not os.path.exists(path+'/gif/'):
        os.makedirs(path+'/gif/')

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
            # Explicitly form a tuple of the two nodes defining the edge
            edge_tuple = (edge_i[0], edge_i[1])
            visits_i = edge_cnter[frozenset(edge_tuple)]
            g_i.add_edge(edge_i[0], edge_i[1], visits_i=visits_i)
        g_i_edge_colors = [visit_colors[e[2].get('visits_i', 1)] for e in g_i.edges(data=True)]

        nx.draw_networkx_nodes(g_i, pos=node_positions, node_size=6, alpha=0.6, node_color='lightgray', linewidths=0.1)
        nx.draw_networkx_edges(g_i, pos=node_positions, edge_color=g_i_edge_colors, alpha=0.8)

        plt.axis('off')
        plt.savefig(path+'/png/img{}.png'.format(i), dpi=120, bbox_inches='tight')
        plt.close()


def pyvis_graph(G ,circuit):
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
    

def nx_graph(G , title , circuit ,cost):
    G = change_color(G, circuit , 'r')
    plt.figure(figsize=(8, 6))
    plt.title(title+'\n Total cost:' + str(cost) + " $")
    nx.draw(G, node_size=10, node_color='black', edge_color='red', alpha=1.0, width=1.0, with_labels=False)

#----------------------MAIN----------------------#

#Outremont, Montreal, Canada
#Leynhac, France
def main(city):
    # real graph
    Graph = ox.graph_from_place(city, network_type='all')  # OPTI :certified:
    G = Graph.to_undirected()
    circuit = drone(G)
    cost = cost_drone(G, circuit)

    # OPTI
    Graph2 = ox.graph_from_place(city, network_type='all')  # OPTI :certified:
    G2 = Graph2.to_undirected()
    circuit2 = drone2(G2)
    cost2 = cost_drone(G, circuit2)

    print("Plotting graph ...")

    # plot graph: option
    nx_graph(G, f"{city}\nModel Drone Normal:", circuit, cost)
    nx_graph(G2, f"{city}\nModel Drone CPP OPTI:", circuit2, cost2)
    plt.show()

    # pyvis: option
    print("Generating HTML Graph ...")
    pyvis_graph(G2, circuit2)

    print("Generating gif ...")

    # animation
    generate_gif(G, circuit, "circuit_drone")
    make_circuit_video('circuit_drone/png/', 'circuit_drone/gif/circuit_drone.gif', fps=7)
    #generate_gif(G2, circuit2, "circuit_drone2")
    #make_circuit_video('circuit_drone2/png/', 'circuit_drone2/gif/circuit_drone2.gif', fps=7)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        main(city)
    else:
        print("Please provide a city as an argument.")