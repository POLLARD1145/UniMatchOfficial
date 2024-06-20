import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import json

nltk.download('stopwords')
nltk.download('punkt')

def prepocess_sentence(sentence):
    stopwords_list = set(stopwords.words('english'))
    tokens = word_tokenize(sentence.lower())
    filtered_tokens = [word for word in tokens if word.isalnum and word not in stopwords_list]
    return filtered_tokens

def preprocess_doc(document):
    sentences = sent_tokenize(document)
    preprocessed_sentences = [prepocess_sentence(sentence) for sentence in sentences]
    return preprocessed_sentences

#loading the intents
with open('../app/ai_logic/jsonfiles/intents.json') as file:
    intents = json.load(file)
    