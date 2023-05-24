import osmnx as ox

noms_villes = ["Montreal, Canada"]

graphes = []
for ville in noms_villes:
    graphes.append(ox.graph_from_place(ville, network_type='all'))

for i in range(len(graphes)):
    ox.plot_graph(ox.project_graph(graphes[i]))