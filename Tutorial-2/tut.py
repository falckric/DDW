from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud

d = path.dirname(__file__)
text = open(path.join(d, 'doc.txt')).read()

wordcloud = WordCloud().generate(text)

plt.figure()
plt._imsave(wordcloud)
plt.axis("off")
plt.show()