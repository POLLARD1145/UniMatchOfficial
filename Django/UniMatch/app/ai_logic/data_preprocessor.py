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
with open('../UniMatch/app/ai_logic/jsonfiles/intents.json') as file:
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

model = SVC(kernel='linear')
model.fit(X_train_tfidf, y_train)

# Define the bot response
def get_response(intents_list, intents_json):
    tag = intents_list
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def predict_class(sentence):
    sentence_tfidf = vectorizer.transform([preprocess_sentence(sentence)])
    prediction = model.predict(sentence_tfidf)
    return prediction[0]

# allow call by just using the message
def get_message(user_input):
    predicted_class = predict_class(user_input)
    response = get_response(predicted_class, intents)
    return response

