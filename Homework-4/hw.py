import networkx as nx
import math
import matplotlib.pyplot as plt
from collections import Counter

mov_code = 0
title_ind = 1
actor_ind = 2
something_ind = 3
role_ind = 4
def read_data():
	actors = set()
	movies_list = {}

	with open("casts.csv") as f:
		lines = f.read().split("\n")
		lines = [line.split(";") for line in lines]
	f.close()
	for line in lines:
		if len(line) > 1:
			movie, actor = line[mov_code].strip('"'), line[actor_ind].strip(('"'))
			if (len(movie) > 1) and (len(actor) > 1):

				actors.add(actor)

				if movie in movies_list.keys():
					acts = movies_list[movie]
					movies_list[movie] = ",".join([acts, actor])
				else :
					movies_list[movie] = actor

	print(actors)
	print(movies_list)
	return actors, movies_list

actors, movies = read_data()

g = nx.Graph()
g.add_nodes_from(actors)
edges = set()
for k, v in movies.items():
	values = v.split(",")
	for i in range(len(values) - 1):
		for j in range(1+i, len(values)):
			edges.add((values[i], values[j]))
g.add_edges_from(edges)
#nx.draw(g)
#plt.show()

def calc_centraility(g, centralities):
	for centralitiy in centralities:
		i = centralitiy(g)
		top_counted = Counter(i).most_common()
		print(" Type : ", centralitiy.__name__)
		for k in top_counted[:10]:
			print(k)


def bacon_for_all(g):
	bacon_numbers = {}
	not_con = set()
	for n in g.nodes:
		try:
			number = nx.shortest_path_length(g, n, "Kevin Bacon")
			#print(n, " : ", number)
			bacon_numbers[n] = number
		except:
			not_con.add(n)
	print("Not connected nodes : ", len(not_con))
	return bacon_numbers

nx.write_gexf(g, "graph.gexf")
nx.draw(g)
plt.savefig("picture_graph.png")
plt.show()

print("------------------- Analyzis -------------------")

print("--------------- General Statistics -------------")
num_edges = len(g.edges())
num_nodes = len(g.nodes())
density = (2*num_nodes)/(num_edges * (num_edges - 1))
print("\n Number of nodes : \n    ",
	  len(g.nodes))
print(" Number of edges : \n    ",
	  len(g.edges))
print(" Density of graph : \n    ",
	  density)
print(" Number of components : \n    ",
	  len([c for c in nx.connected_components(g)]))
centralities = [
	nx.degree_centrality,
	nx.closeness_centrality, # Takes long time
	nx.betweenness_centrality, # Takes long time
	nx.eigenvector_centrality # Takes long time
]
print(" Centralities / Key Players :")
calc_centraility(g, centralities)

print(" Bacon numbers : ")
b_dict = bacon_for_all(g)
bc = Counter(b_dict).most_common()
print("10 worst :")
print(bc[:10])
print("10 best :")
print(bc[len(bc)-10:])
print("Average :\n", sum(b_dict.values())/len(b_dict.values()))
