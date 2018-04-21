import nltk
import wikipedia
from collections import Counter
from string import punctuation

text = None

with open("text") as f:
	text = f.read()

text = wikipedia.page("Czech Republic").content

words = nltk.word_tokenize(text)
sentences = len(nltk.sent_tokenize(text))

print(" Number of sentences : ")
print(sentences)

nopunc = [token for token in words if token not in punctuation]

text_pos = nltk.pos_tag(nopunc)
grammar = "NP: {<DT>?<JJ>*<NN|NNS>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(text_pos)
#print(result)
#result.draw()
print("\n POS tagged :")
pos_c = Counter(text_pos)
print(pos_c.most_common()[:10])

# normal NER
ne_chunked = nltk.ne_chunk(text_pos, binary=False)
def extract_entities(ne_chunked):
	data = {}
	for e in ne_chunked:
		if isinstance(e, nltk.tree.Tree):
			text = " ".join([word for word, tag in e.leaves()])
			ent = e.label()
			data[text] = ent
		else:
			continue
	return data

extracted = extract_entities(ne_chunked)
print("\n Normal ne_chuncked : ")
extr_Counter = Counter(extracted)
print(extr_Counter.most_common()[:10])

# Custom NER
entity = []
custom_data = {}

#print("\n Patterns :")
for t in text_pos:
	if (t[1].startswith("NN") or (t[1].startswith("JJ"))): # or (entity and t[1].startswith("IN"))):
		entity.append(t)
		custom_data[t[0]] = t[1]
	else:
		if (entity) and entity[-1][1].startswith("IN"):
			entity.pop()
		if (entity and " ".join(e[0] for e in entity)[0].isupper()):
			if (len(entity) > 1) :
				pass#print(" ".join(e[0] for e in entity))
		entity = []

print("\n Custom classifier :")
cust_c = Counter(custom_data)
print(cust_c.most_common()[:10])

print("\n   ---   Wikipedia    ---\n")

wiki_res = wikipedia.search("Norway")
wiki_page = wikipedia.page("Sword")
wiki_sentences = nltk.sent_tokenize(wiki_page.summary)
wiki_first_sentence = nltk.word_tokenize(wiki_sentences[0])
#print(wiki_first_sentence)
wiki_pos = nltk.pos_tag(wiki_first_sentence)
#print(wiki_pos)

wiki_dict = {}
entity = []
print(" Info from first line about swords : ")
for t in wiki_pos:
	if (
				(t[1].startswith("NN")
				 or
					 (entity and t[1].startswith("DT"))
				 or
					 (entity and t[1].startswith("VB"))
				 or
					 (entity and t[1].startswith("JJ"))
				 or
					 (entity and t[1].startswith("IN"))
				 )
	):
		entity.append(t)
		wiki_dict[t[0]] = t[1]
	else:
		if (entity) and entity[-1][1].startswith("IN"):
			entity.pop()
		if (entity and " ".join(e[0] for e in entity)[0]):#.isupper()):
			print(" ".join(e[0] for e in entity))
			break
		entity = []
# TODO : POS tagging DONE
# TODO : NER w/entity clasification DONE
# TODO : NER w/custom patterns DONE
# TODO : Implement custom entity classification

