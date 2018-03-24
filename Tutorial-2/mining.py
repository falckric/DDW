from nltk.corpus import stopwords
from string import punctuation
from collections import Counter
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.util import *
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def tokenCounts(tokens):
	counts = Counter(tokens)
	sortedCounts = sorted(counts.items(), key=lambda count:count[1], reverse=True)
	return sortedCounts

def extractEntities(ne_chunked):
	data = {}
	for entity in ne_chunked:
		if isinstance(entity, nltk.tree.Tree):
			text = " ".join([word for word, tag in entity.leaves()])
			ent = entity.label()
			data[text] = ent
		else:
			continue
	return data

def get_top(dict, i=3):
	list_keys = []
	list_values = []

	for _ in range(i):
		key, value = "", 0
		for k, v in dict:
			if (v > value) and (k not in list_keys):
				key, value = k, v
		list_keys.append(key)
		list_values.append(value)

	d = {}
	for _ in range(i):
		d[list_keys.pop(0)] = list_values.pop(0)

	return d

class Miner():

	text = None
	with open('text.txt', 'r') as f:
		text = f.read()

	sentences = nltk.sent_tokenize(text)
	print("All sentences : \n", sentences)

	tokens = nltk.word_tokenize(text)

	b_prep = get_top(tokenCounts(tokens), i=3)

	print("All words : \n", tokens)
	tokens = [token for token in tokens if token not in punctuation]
	print("Removed punctuation : \n", tokens)
	tokens = [token for token in tokens if token not in stopwords.words('english')]
	print("Removed stopwords : \n", tokens)
	countedTokens = tokenCounts(tokens)
	print("All words counted : \n", countedTokens)

	#Stemming
	stemmer = PorterStemmer()
	lol = stemmer.stem("rented")
	stems = {}#{token:stemmer.stem(token) for token in tokens}
	for token in tokens:
		stems[token] = stemmer.stem(token)


	print("All stems : \n", stems)

	sorted_stems = tokenCounts(stems)

	print("Stems sorted : \n", sorted_stems)
	#Lemming
	lemmatizer = WordNetLemmatizer()
	#tokens = nltk.word_tokenize(text)

	lemmas = {}#{token:lemmatizer.lemmatize(token) for token in tokens}
	for token in tokens:
		lemmas[token] = lemmatizer.lemmatize(token)


	sorted_lems = tokenCounts(lemmas)
	print("Lems sorted : \n", sorted_lems)
	# Part of speech
	tagged = nltk.pos_tag(tokens)

	# Entity rec
	ne_chunked = nltk.ne_chunk(tagged, binary=True)
	sorted_ne = extractEntities(ne_chunked)

	print("Entities : \n", sorted_ne)

	a_prep = get_top(tokenCounts(tokens), i=3)

	# sentiment Analysis
	vader_analyzer = SentimentIntensityAnalyzer()
	print("Polarity scores : \n", vader_analyzer.polarity_scores(text))

	wordcloud = WordCloud().generate(text)

	print("\n\n\n")
	print("Before prep : \n", b_prep)
	print("After prep : \n", a_prep)

	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()


if __name__ == "__main__":
	Miner()