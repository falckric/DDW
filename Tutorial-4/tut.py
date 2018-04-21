import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def get_num(str):
	nums = str.split(":")
	return int(nums[0]), int(nums[1])

def read_data(file):
	table = None
	info = []
	with open(file, "r") as f:
		tall = int(f.readline())
		table = np.zeros((tall, tall))
		info = f.read().splitlines()
		info = [c.split(" ") for c in info]
		#print(info)
	f.close()

	for i in range(len(info)):
		for c in info[i]:
			if len(c) > 1:
				index, val = get_num(c)
				table[i][index] = val
	print("Initialized Matrix :\n{}\n".format(table))

	G = nx.Graph(table)
	nx.draw(G)
	plt.show()
	return table

def createS(H):
	S = None
	add = np.array(H)
	for i in range(len(add)):
		s = sum(add[i])
		if s == 0:
			add[i] = 1 / len(add[i])
		else:
			add[i] = 0

	S = np.add(H, add)

	print("S:\n{}\n".format(S))
	return (S)

def createH(table):
	H = np.zeros((len(table), len(table)))

	for i in range(len(table)):
		tot = sum(table[i])
		for j in range(len(table[i])):
			tall = table[i][j]
			if tall > 0:
				H[i][j] = tall / tot



	print("H:\n{}\n".format(H))
	return (H)

def createG(S, alpha):
	G = None
	altS = alpha*np.array(S)
	e = np.ones((len(S), len(S)))
	add = (1-alpha)*(1/len(S))*(np.matmul(e, e.transpose()))

	G = np.add(altS, add)

	print("G:\n{}\n".format(G))
	return (G)

def computePR(M, iter):
	pi = np.ones((len(M), len(M)))
	for i in range(iter):
		pi = np.matmul(pi, M)
	print("PR ", iter," iterations :\n{}\n".format(pi))

for i in range(1, 5):
	print("------------------ ", i, " ------------------")
	inputFile = "./data/test"+ str(i) +".txt"
	table = read_data(inputFile)
	alpha = 0.9
	iterations = 2

	H = createH(table)
	computePR(H, iterations)

	S = createS(H)
	computePR(S, iterations)

	G = createG(S, alpha)
	computePR(G, iterations)

for i in range(1,16):
	pass