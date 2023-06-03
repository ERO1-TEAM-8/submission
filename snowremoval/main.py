from snowremoval import *
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
import contextily as ctx


#----------------------MAIN----------------------#
sectors = []


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
    #for G in Gs:
        #circuit = drone(G)
        #drone_circuits.append(circuit)
        #cost_drone(G, drone_circuits[0])
        #G = change_color(G, circuit , 'r')
        #colors = nx.get_edge_attributes(G, 'color').values()
        #plt.figure(figsize=(8, 6))
        #plt.title('Model Drone')
        #nx.draw(G, edge_color=colors , node_size=10, node_color='black', alpha=1.0, width=1.0, with_labels=False)


        #for u, v, data in G.edges(data=True):
         #   data['weight'] = data.get('weight', 0)  # If 'weight' is not in the dictionary, default to 0
        #G_max = max_weight_graph(G)
        #odd_matching_dupes = nx.max_weight_matching(G_max)
        #odd_matching = [tuple(sorted(edge)) for edge in odd_matching_dupes]
        #g_odd_complete_min_edges = nx.Graph(odd_matching)
        #nx.draw(g_odd_complete_min_edges, node_size=20, edge_color='blue', node_color='red')
        #plt.title('Min Weight Matching on Complete Graph')
        #plt.axis('off')
        #plt.show()
    
    
    #cost_drone(G, circut)
    #snow_circuits = snow_removal(Gs)
    #for c in snow_circuits:
    #    print(c)

    #plt.title('Model Snow Removal')
    G2 = eulerize_directed_graph(Graph)
    circuit2 =to_eulerian_directed(Graph, G2)

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    # loop over nodes, add them to the pyvis network, and style them
    for node in G2.nodes():
        net.add_node(
        node,
        color="yellow",
        size=10,
        title="Node: " + str(node),
        label="Node " + str(node)
    )

# loop over edges, add them to the pyvis network, and style them
    for edge in G2.edges():
        net.add_edge(
        edge[0], 
        edge[1], 
        color="white", 
        width=0.5
    )
    for i in range(len(circuit2)):
        net.add_edge(
        circuit2[i][0], 
        circuit2[i][1], 
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
 

    

    node_positions = nx.spring_layout(G2)  # compute node positions
    plt.figure(figsize=(8, 6))
    #plot cost as title
    #plt.title('Model Drone: Total cost:' + str(cost) + " $")
    nx.draw(G2 , node_size=10, node_color='black', alpha=1.0, width=1.0, with_labels=False)
    # Plot the graph without displaying it
    fig, ax = ox.plot_graph(G2, show=False, close=False)

    # Add the basemap
    ctx.add_basemap(ax, zoom=12, url=ctx.providers.Stamen.TonerLite)
    plt.show()
    



    # Animation part
    visit_colors = {1:'black', 2:'red', 3:'blue'}
    edge_cnter = {}
    

    # ensure the directory for the images exists
    if not os.path.exists('fig/png/'):
        os.makedirs('fig/png/')

    if not os.path.exists('fig/gif/'):
        os.makedirs('fig/gif/')

    for i, e in enumerate(circuit2, start=1):
        edge = frozenset([e[0], e[1]])
        if edge in edge_cnter:
            edge_cnter[edge] += 1
        else:
            edge_cnter[edge] = 1

        # Full graph (faded in background)
        nx.draw_networkx(G2, pos=node_positions, node_size=6, node_color='gray', with_labels=False, alpha=0.07)

        # Edges walked as of iteration i
        circuit_i = copy.deepcopy(circuit2[0:i])
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