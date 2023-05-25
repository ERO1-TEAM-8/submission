import osmnx as ox
#USED TO CREATE THE GRAPH and to plot it and to get the nodes and edges of the graph + find shortest path
import networkx as nx
#USED TO plot data on the graph
import matplotlib.pyplot as plt


"""
2 Problem
People from Montréal are concerned with snowplowing operations. [Vé20], but increasing the allowed funds is still a delicate point for the city council [Lef19], and it is now an objective to reduce these operations cost, while still providing an effecient snowplow service to the inhabitants. The city tasks your company with a study. The goal is to minimize the cost of a typical snowplowing day. Your team’s role is to find a short enough path for the snowplows around the Montréal road network, while still remove snow from the whole given zone.
It is understood that snow levels show great variance around the city. It is not necessary to snowplow around the whole city. Your boss asks you to perform an aerial analysis via drone. This way we can detect what sector needs snowplowing the most.
Your mission is :
1. to find shortest path(s) for the drone aerial check of the road network. It has to check the whole network
to have enough data 1 ;
2. to find paths for snowplows to remove snow from identified sector (see section 3 Handout constraints).
Note : snowplows go through two-way roads only once to remove snow.
3. to propose a cost model for snow removing operations given the number of snowplows available.
Also, the municipality would like to invest in high performance snowplows, called type II, that can remove snow faster but at a greater cost (see section 4 Data). Simulations are asked to compare the associated cost for different options.
3 Handout constraints
Your handout has to fulfill the following constraints and contain :
1. an AUTHORS file with the list of authors ;
2. a README file with all the necessary instructions to install and run your work, as well as a description of your handout structure ;
3. a pdf file of at most 4 pages that synthesises your team thinking and must contain :
— a summary of used data, as well as the studied perimeter (which constraints are taken into account) — hypotheses ans model choices,
— kept solutions, its indicators, comparison between scenarios,
— identified limits of the model(s)
4. a script running a demo of your solution ;
5. a subtree dealing with the drone flight ;
6. a subtree dealing with the snow removal planning, on the following sectors : — Outremont,
— Verdun,
— Saint-Léonard,
— Rivière-des-prairies-pointe-aux-trembles, — et Le Plateau-Mont-Royal.
4 Data
Municipality gives you the following data :
— Super Drone :
— Fixed cost : 100 $/day
— Cost per Km : 0.01 $/km
— Snowplows :
— Fixed cost : type I : 500$/day, type II : 800 $/day
— CostperKm:typeI:1.1$/km,typeII:1.3$/km
— Hourlycostforfirst8hours:typeI:1.1$/h,typeII:1.3$/h
— Hourly cost for after the first 8 hours : type I : 1.3 $/h, type II : 1.5 $/h — Average speed : type I : 10 km/h, type II : 20 km/h


"""



city = ["Montreal, Canada"]


# Define the perimeter or zone to study (e.g., Montréal city boundary)
perimeter = ox.graph_from_place(city)

# Define the sectors for snow removal planning
sectors = ["Outremont", "Verdun", "Saint-Léonard", "Rivière-des-prairies-pointe-aux-trembles", "Le Plateau-Mont-Royal"]

graph = ox.graph_from_place(city, network_type="all_private", retain_all=True, which_result=2)


graphes = []
for ville in city:
    graphes.append(ox.graph_from_place(ville, network_type='all'))

for i in range(len(graphes)):
    ox.plot_graph(ox.project_graph(graphes[i]))


#TODO: Find the start and end nodes for the drone flight

#TODO:  Find the shortest path for the drone flight


#TODO:Find the shortest paths for snowplow snow removal in each sector

# Define the cost model parameters
fixed_cost_drone = 100
cost_per_km_drone = 0.01
fixed_cost_snowplow_type1 = 500
cost_per_km_snowplow_type1 = 1.1
hourly_cost_type1_first8hours = 1.1
hourly_cost_type1_after8hours = 1.3
average_speed_type1 = 10
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