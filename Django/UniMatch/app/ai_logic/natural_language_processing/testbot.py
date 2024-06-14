import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

text = "Hello world! This is an NLP tutorial."
print(word_tokenize(text))
print(sent_tokenize(text))


import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

tokens = [token.text for token in doc]
sentences = [sent.text for sent in doc.sents]
print(tokens)
print(sentences)
