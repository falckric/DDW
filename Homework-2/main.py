from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelBinarizer

import numpy as np

def check(vectorizer, corpus, query, num, type, top_num=100, p=True):
	corpus.append(query)
	matrix = vectorizer.fit_transform(corpus)
	sim_cosine = np.array(cosine_similarity(matrix[len(corpus) - 1],
											matrix[0:(len(corpus) - 1)])[0])
	sim_euc = np.array(euclidean_distances(matrix[len(corpus) - 1],
												matrix[0:(len(corpus) - 1)])[0])
	top_cosine = sim_cosine.argsort()[-min(top_num, len(sim_cosine)):][::-1] + 1
	top_euc = sim_euc.argsort()[-min(top_num, len(sim_cosine)):][::-1] + 1

	corpus.pop(len(corpus) - 1)

	if p:
		print("   ", type)
		print("Querry ", str(num))
		print("Top", str(top_num))
		print("Cosine\n", top_cosine)
		print("Euclidian\n", top_euc)

	return top_cosine, top_euc#sim_cosine, sim_euc

def eval(results, cos, euc, type, p=False):
	cos_truePos = 0
	euc_truePos = 0
	for i in cos:
		if i in results:
			cos_truePos += 1
	for i in euc:
		if i in results:
			euc_truePos += 1

	cos_pre = cos_truePos/len(cos)
	cos_rec = cos_truePos/len(results)
	cos_f = 0
	try:
		cos_f = (2 * cos_pre * cos_rec)/(cos_pre + cos_rec)
	except:
		pass


	euc_pre = euc_truePos/(len(euc))
	euc_rec = euc_truePos/len(results)
	euc_f = 0
	try:
		euc_f = (2 * euc_pre * euc_rec)/(euc_rec + euc_pre)
	except:
		pass

	d = {
		"cosine_pre": cos_pre,
		"cosine_rec": cos_rec,
		"cosine_f": cos_f,
		"euclid_pre": euc_pre,
		"euclid_rec": euc_rec,
		"euclid_f": euc_f
	}

	if p:
		print("    ", type, " Evaluation \n")
		print("Cosine")
		print("Presission : ", cos_pre)
		print("Recall : ", cos_rec)
		print("F-measure : ", cos_f, "\n")

		print("Euclidian")
		print("Presission : ", euc_pre)
		print("Recall : ", euc_rec)
		print("F-measure : ", euc_f, "\n")

	return d




# prepare corpus
corpus = []
queries = []
results = []
for d in range(1400):
	f = open("./d/" + str(d + 1) + ".txt")
	corpus.append(f.read())
# add query to corpus
for q in range(225):
	f = open("./q/" + str(q + 1) + ".txt")
	g = open("./r/" + str(q + 1) + ".txt")
	queries.append(f.read())
	results.append(g.read())

results = [r.split("\n") for r in results]
print(results[0])
for i in range(len(results)):
	for j in range(len(results[i])-1):
		k = results[i][j]
		try:results[i][j] = int(k)
		except:print(k, len(k))

# init vectorizer
tfidf_vectorizer = TfidfVectorizer()
puretf_vectorizer = CountVectorizer()

# TF-IDF
tfidf_cosine = []
tfidf_euc = []
print("   ---   Starting querries TF-IDF   ---")
for i in range(20):#len(queries)):
	cos, euc = check(tfidf_vectorizer, corpus, queries[i], i+1, "TF-IDF", top_num=10, p=False)
	tfidf_cosine.append(cos)
	tfidf_euc.append(euc)
print("   ---   Ended   ---")

print("   ---   Starting querries Pure TF   ---")
# Pure TF
pure_cosine = []
pure_euc = []
for i in range(10):#len(queries)):
	cos, euc = check(puretf_vectorizer, corpus, queries[i], i+1, "Pure TF", top_num=1000, p=False)
	pure_cosine.append(cos)
	pure_euc.append(euc)
print("   ---   Ended   ---")
# Eval

res_cos = []
res_euc = []
print(tfidf_cosine[0])
print(tfidf_euc[0])
print(results[0])
"   ---   Starting eval TF-IDF   ---"
ev_tfidf = []
for i in range(len(tfidf_cosine)):
	ev_tfidf.append(eval(results[i], tfidf_cosine[i], tfidf_euc[i], "TF-IDF", p=False))
"   ---   Ended   ---"
"   ---   Starting eval PureTF   ---"
ev_puretf = []
for i in range(len(pure_cosine)):
	ev_puretf.append(eval(results[i], pure_cosine[i], pure_euc[i], "PureTF", p=False))
"   ---   Ended   ---"
print("TF-IDF")
for i in range(len(ev_tfidf)):
	#print(str(i+1), " : ", ev_tfidf[i])
	s = str(i+1) + " : "
	for k, v in ev_tfidf[i].items():
		s += "\n   " + str(k) + " : " + str(v)
	print(s)
print("PureTF")
for i in range(len(ev_puretf)):
	s = str(i + 1) + " : "
	for k, v in ev_puretf[i].items():
		s += "\n   " + str(k) + " : " + str(v)
	print(s)


