import pandas as pd
from collections import Counter


def frequentItems(transactions, support):
	counter = Counter()
	for trans in transactions:
		counter.update(frozenset([t]) for t in trans)
	return set(item for item in counter if counter[item] / len(transactions) >= support), counter


def generateCandidates(L, k):
	candidates = set()
	for a in L:
		for b in L:
			union = a | b
			if len(union) == k and a != b:
				candidates.add(union)
	return candidates


def filterCandidates(transactions, itemsets, support):
	counter = Counter()
	for trans in transactions:
		subsets = [itemset for itemset in itemsets if itemset.issubset(trans)]
		counter.update(subsets)
	return set(item for item in counter if counter[item] / len(transactions) >= support), counter


def genereateRules(frequentItemsets, supports, minConfidence):
	for i in frequentItemsets:
		for c in i:
			sup = 0
			fc = frozenset({c})
			i_c = i-fc #frozenset({i-fc})
			try:
				sup = supports[i] / supports[i_c]
			except:
				pass
			if sup >= minConfidence:
				print("{} -> {} - support : {} - confidence : {}".format(i - fc, c, supports[fc], sup))

def generateLiftRules(frequentItemsets, supports, minConfidence):
	for i in frequentItemsets:
		for c in i:
			sup = 0
			fc = frozenset({c})
			i_c = i-fc #frozenset({i-fc})
			try:
				sup = supports[i] / (supports[i_c] * supports[fc])
			except:
				pass
			if sup >= minConfidence:
				print("{} -> {} - support : {} - confidence : {}".format(i - fc, c, supports[fc], sup))

def apriori(transactions, support):
    result = list()
    resultc = Counter()
    candidates, counter = frequentItems(transactions, support)
    result += candidates
    resultc += counter
    k = 2
    while candidates:
        candidates = generateCandidates(candidates, k)
        candidates,counter = filterCandidates(transactions, candidates, support)
        result += candidates
        resultc += counter
        k += 1
    resultc = {item:(resultc[item]/len(transactions)) for item in resultc}
    return result, resultc

df = pd.read_csv("./bank-data.csv")
del df["id"]
df["income"] = pd.cut(df["income"], 10)
dataset = []
for index, row in df.iterrows():
	row = [col + "=" + str(row[col]) for col in list(df)]
	dataset.append(row)
frequentItemsets, supports = apriori(dataset, 0.3)
print("Normal Ruleset")
genereateRules(frequentItemsets, supports, 0.5)
print("Lift Ruleset")
generateLiftRules(frequentItemsets, supports, 0.5)