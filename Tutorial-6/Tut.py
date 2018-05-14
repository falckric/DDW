from math import sqrt
from numpy import genfromtxt
import numpy as np
from collections import Counter
import math

persons = {}
keyes = []
cosine_matrix = []
pearson_matrix = []


def loadData():
	data = genfromtxt('small-dataset.csv', delimiter=',', dtype=None)
	print(data)
	return data

# computes similarity between two users based on the cosine similarity metric
def user_sim_cosine_sim(person1, person2):
	top = sum([person1[i]*person2[i] for i in range(len(person2))])
	bot = (sqrt(sum([a**2 for a in person1]))) * (sqrt(sum([b**2 for b in person2])))
	return top / bot

# computes similarity between two users based on the pearson similarity metric
def user_sim_pearson_corr(person1, person2):
	mean1 = np.mean(person1)
	mean2 = np.mean(person2)
	top = sum([(person1[i]-mean1)*(person2[i]-mean2) for i in range(len(person1))])
	bot = (sqrt(sum((person1[i] - mean1)**2 for i in range(len(person1))))) * (sqrt(sum((person2[i] - mean2)**2 for i in range(len(person2)))))
	return top/bot
# returns top-K similar users for the given
def most_similar_users(person, number_of_users):
	index = keyes.index(person)
	mat = pearson_matrix[index]
	all_users = pearson_matrix[index]
	all_users.pop(index)

	c = Counter(all_users).most_common(number_of_users)

	users = [keyes[mat.index(i[0])] for i in c]
	return users

# generate recommendations for the given user
def user_recommendations(person):
	sim_users = most_similar_users(person, 3)
	index = keyes.index(person)
	items_to_rec = [i for i in range(len(persons[person])) if persons[person][i] == 0]
	recs = {}
	sim_mat = pearson_matrix
	for i in items_to_rec:
		top = sum([persons[u][i] * sim_mat[index][keyes.index(u)] for u in sim_users])
		bot = sum([sim_mat[index][keyes.index(u)] for u in sim_users])
		recs[i+1] = top / bot
	return recs

data = loadData()

persons_list = []
for d in data :
	persons[d[0]] = [d[i] for i in range(1, len(d))]
for d in data:
	person = []
	person.append(d[0])
	person.append([d[i] for i in range(0, len(d))])
	#person.append(np.mean(np.array(person[1])))

print(persons)
keyes = [k for k in persons.keys()]

for i in keyes:
	line = []
	p_line = []
	for j in keyes:
		line.append(user_sim_cosine_sim(persons[i], persons[j]))
		p_line.append(user_sim_pearson_corr(persons[i], persons[j]))
	cosine_matrix.append(line)
	pearson_matrix.append(p_line)
print(np.array(cosine_matrix))
print(np.array(pearson_matrix))
for k in keyes:
	print(k, " - " , user_recommendations(k))