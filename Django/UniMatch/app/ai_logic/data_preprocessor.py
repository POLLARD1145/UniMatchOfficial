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

from huggingface_hub import InferenceClient

# Define your Hugging Face token
HF_TOKEN = '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'  # Replace with your actual token

# Define the API endpoint for the model
MODEL_NAME = "mistralai/Mistral-Nemo-Instruct-2407"

def generate_response(prompt):
    # Initialize the InferenceClient
    client = InferenceClient(
        token=HF_TOKEN,
    )

    # Knowledge base about Zambian universities and their ICT programs
    knowledge_base = """
    UniMatch is here to help you select the best ICT programs at Zambian public universities. Here is some information about the universities and their ICT programs:

    University of Zambia (Lusaka):
    - Software Engineering (SE): Focus on designing, developing, and maintaining software systems. (Degree)
    - Computer Systems Engineering (CSE): Combines computer science and electrical engineering for system design. (Degree)
    - Bachelor of Science in Computer Science: Comprehensive program covering algorithms, data structures, and software design. (Degree)

    Copperbelt University (Kitwe):
    - Diploma in Information Technology: Entry-level program in IT, focusing on basic skills and knowledge. (Diploma)
    - Bachelor of Science in Computer Science: Focuses on computational theory, programming, and problem-solving. (Degree)
    - Bachelor of Science in Information System: Study of systems that manage, process, and analyze data. (Degree)
    - Masters of Science in Computer Science: Advanced studies in computer science research and applications. (Masters)
    - PhD in Computer Science: Research-focused program aimed at creating new knowledge in the field. (Doctorate)

    Mulungushi University (Kabwe):
    - Bachelor of Science in Computer Science: Foundational program in computer science principles and applications. (Degree)
    - Bachelor of Science in Information Technology: Covers a wide range of topics in IT with a practical approach. (Degree)
    - Bachelor of Science in Information Systems: Focuses on information systems design, development, and management. (Degree)
    - Bachelor of Science in Data Science: Introduces data analysis, machine learning, and big data technologies. (Degree)
    - Bachelor of Science in Cyber Security: Teaches security principles, risk management, and cyber threat prevention. (Degree)

    Kwame Nkrumah University (Kabwe):
    - Bachelor of ICT with Education: Integrates ICT skills with educational practices for teaching roles. (Degree)

    Kapasa Makasa University (Chinsali):
    - Bachelor of ICT with Education: Prepares students for educational roles in ICT. (Degree)
    - Bachelor of Science in Cyber Security: Teaches security principles, risk management, and cyber threat prevention. (Degree)
    """

    # Craft the full prompt
    full_prompt = f"UniMatch is a recommender system for selecting the best ICT programs in Zambian public universities. Based on the following information:\n{knowledge_base}\n\nUser query: {prompt}"

    # Perform the chat completion
    response = client.chat_completion(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=150,
        stream=False,  # Set to True if you want streaming responses
    )

    # Extract and return the response text
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    prompt = "What are the best ICT programs at the University of Zambia?"
    print(get_response(prompt))
