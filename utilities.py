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

#----------------------Eulerian----------------------#
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
