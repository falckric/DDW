import networkx as nx
import nltk
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from collections import Counter

def read(file):
	text = None
	with open(file, "r") as f:
		text = f.read()
	f.close()
	return text

def task():
	'''adj_list_file = "_alcohol/graph/adj_list"
	inv_adj_list_file = "_alcohol/graph/inv_adj_list"
	nodes_file = "_alcohol/graph/nodes"

	adj_list = read(adj_list_file)
	inv_adj_list = read(inv_adj_list_file)
	nodes = read(nodes_file)'''

	text = read("Data/data")

	banned_things = ".,':;"

	# process text and convert to a graph
	sentences = [[t for t in nltk.word_tokenize(sentence)] for sentence in nltk.sent_tokenize(text)]
	all_diff_words = set()
	edges = set()
	for k in sentences:
		for i in k:
			if i not in banned_things:
				all_diff_words.add(i)
	for k in sentences:
		for i in range(len(k)-1):
			for j in range(i+1, len(k)):
				if (k[i] not in banned_things) and (k[j] not in banned_things):
					edges.add((k[i], k[j]))

	G = nx.Graph()
	G.add_nodes_from(all_diff_words)
	G.add_edges_from(edges)

	nx.draw(G)
	plt.show()

	print(G.nodes(data=True))

	# Statistics
	num_edges = len(G.edges())
	num_nodes = len(G.nodes())
	density = (2*num_nodes)/(num_edges * (num_edges - 1))
	print("Number of nodes : \n", num_nodes)
	print("Number of edges : \n", num_edges)
	print("Density of graph : \n", density)
	# TODO : eval connectivity
	print("Components of graph : \n", [c for c in nx.connected_components(G)])

	# Metrics
	centralities = [
		nx.degree_centrality,
		nx.closeness_centrality,
		nx.betweenness_centrality,
		nx.eigenvector_centrality
	]
	print(" Centralities / Key Players")
	for centralitiy in centralities:
		i = centralitiy(G)
		top_counted = Counter(i).most_common()
		print(centralitiy.__name__)
		print(top_counted[:10])

	communities = {node: cid + 1 for cid, community in enumerate(nx.algorithms.community.k_clique_communities(G, 3)) for
				   node in community}
	com = {}
	for k, v in communities.items():
		if v not in com.keys():
			com[v] = k
		else:
			t = com[v]
			com[v] = " ".join([t, k])
	print(" Communities :")
	for k, v in com.items():
		print(k, " : ", v)

	# Visualisation
	# TODO : Visualise key players
	# TODO : Visualise clusters / comunities
	# TODO : Visualise importance of edges (weight)

	'''# visualise
	plt.figure(figsize=(20, 10))
	pos = graphviz_layout(G, prog="fdp") # graphviz_layout(G, prog="fdp")
	nx.draw(G, pos,
			labels={v: str(v) for v in G},
			cmap=plt.get_cmap("bwr"),
			node_color=[G.degree(v) for v in G],
			font_size=12
			)
	plt.show()

	# write to GEXF
	nx.write_gexf(G, "export.gexf")
'''
if __name__ == "__main__":
	task()
