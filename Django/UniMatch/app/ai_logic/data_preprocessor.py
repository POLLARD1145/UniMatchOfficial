import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Ensure NLTK data is downloaded
#nltk.download('stopwords')
#nltk.download('punkt')

# Preprocessing functions
def preprocess_sentence(sentence):
    stopwords_list = set(stopwords.words('english'))
    tokens = word_tokenize(sentence.lower())
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stopwords_list]
    return filtered_tokens

def preprocess_doc(document):
    sentences = sent_tokenize(document)
    preprocessed_sentences = [preprocess_sentence(sentence) for sentence in sentences]
    return preprocessed_sentences

# Load the intents file
with open('../UniMatch/app/ai_logic/jsonfiles/intents.json', 'r') as file:
    intents = json.load(file)

# Prepare data
words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = preprocess_sentence(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(set(words))
classes = sorted(set(classes))

# Vectorize and train
X_train = [' '.join(doc[0]) for doc in documents]
y_train = [doc[1] for doc in documents]

vectorizer = TfidfVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x)
X_train_tfidf = vectorizer.fit_transform(X_train)

model = SVC(kernel='linear',probability=True)
model.fit(X_train_tfidf, y_train)

# Context dictionary to track conversation state
context = {}

def get_response(intent, intents_json, user_id):
    tag = intent
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            if 'context_set' in i:
                context[user_id] = i['context_set']
            if not 'context_filter' in i or (user_id in context and 'context_filter' in i and context[user_id] == i['context_filter']):
                result = random.choice(i['responses'])
                break
    return result

def predict_class(sentence):
    sentence_tfidf = vectorizer.transform([preprocess_sentence(sentence)])
    prediction = model.predict(sentence_tfidf)
    confidence = model.decision_function(sentence_tfidf)
    return prediction[0], confidence.max()

# allow call by just using the message
def get_message(user_input, user_id):
    predicted_class, confidence = predict_class(user_input)
    if confidence < 0.5:  # Threshold for confidence
        response = "I'm not sure I understand. Can you please rephrase?"
    else:
        response = get_response(predicted_class, intents, user_id)
    return response

# Example usage