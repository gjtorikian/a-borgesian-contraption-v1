import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

f = open('borges.txt', 'r')
text = f.read()

phrases = sent_tokenize(text)
words = word_tokenize(text)

print(int(len(words) / len(phrases)))
