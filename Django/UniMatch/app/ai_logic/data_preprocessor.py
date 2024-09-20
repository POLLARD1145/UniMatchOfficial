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
        1. Copperbelt University (Kitwe):
        - Programs:
        - Diploma in Information Technology: Entry-level program in IT, focusing on basic skills and knowledge. (Diploma)
        - Bachelor of Science in Computer Science: Focuses on computational theory, programming, and problem-solving. (Degree)
        - Computer Engineering (CE): Combines computer science and electrical engineering for system design. (Degree)
        - Bachelor of Science in Information System: Study of systems that manage, process, and analyze data. (Degree)
        - Masters of Science in Computer Science: Advanced studies in computer science research and applications. (Masters)
        - PhD in Computer Science: Research-focused program aimed at creating new knowledge in the field. (Doctorate)
        - Admission Criteria: 6 to 20 points (6 to 10 points are good for top universities)
        - Application Period: November to September
        - Tuition Fees: K 22,000 to K 33,000 per academic year
        - Website: [CBU](https://www.cbu.ac.zm)

        2. University of Zambia (Lusaka):
        - Programs:
        - Software Engineering (SE): Focus on designing, developing, and maintaining software systems. (Degree)
        - Computer Systems Engineering (CSE): Combines computer science and electrical engineering for system design. (Degree)
        - Bachelor of Science in Computer Science: Comprehensive program covering algorithms, data structures, and software design. (Degree)
        - Admission Criteria: 6 to 20 points (6 to 10 points are good for top universities)
        - Application Period: February to October
        - Tuition Fees: K 22,000 to K 30,000 per academic year
        - Website: [UNZA](http://www.unza.zm)


        3. Mulungushi University (Kabwe):
        - Programs:
        - Bachelor of Science in Computer Science: Foundational program in computer science principles and applications. (Degree)
        - Bachelor of Science in Information Technology: Covers a wide range of topics in IT with a practical approach. (Degree)
        - Bachelor of Science in Information Systems: Focuses on information systems design, development, and management. (Degree)
        - Bachelor of Science in Data Science: Introduces data analysis, machine learning, and big data technologies. (Degree)
        - Bachelor of Science in Cyber Security: Teaches security principles, risk management, and cyber threat prevention. (Degree)
        - Admission Criteria: 6 to 20 points
        - Application Period: April to January
        - Website: [Mulungushi University](https://www.mu.ac.zm)

        4. Kwame Nkrumah University (Kabwe):
        - Programs:
        - Computer Science Degree
        - Bachelor of ICT with Education: Integrates ICT skills with educational practices for teaching roles. (Degree)
        - Admission Criteria: 6 to 20 points
        - Application Period: July to April
        - Website: [Kwame Nkrumah University](https://www.nkrumah.edu.zm)

        5. Kapasa Makasa University (Chinsali):
        - Programs:
        - Bachelor of ICT with Education: Prepares students for educational roles in ICT. (Degree)
        - Bachelor of Science in Cyber Security: Teaches security principles, risk management, and cyber threat prevention. (Degree)
        - Admission Criteria: 6 to 20 points
        - Application Period: January to November
        - Website: [Kapasa Makasa University](https://www.kmu.ac.zm)

        Admission Criteria for Top Universities:
        - 6 to 10 points is considered good for top universities like Copperbelt University (CBU) and University of Zambia (UNZA).
        other public
        Here are some of the programs offered at **Mukuba University** and **Palabana University** in Zambia:

### **Mukuba University**
Mukuba University primarily focuses on education and science-related fields, offering programs such as:
1. **Bachelor of Education in Chemistry**
2. **Bachelor of Education in Physics**
3. **Bachelor of Education in Biology**
4. **Bachelor of Education in Mathematics**
5. **Bachelor of Education in Agriculture Science**
6. **Bachelor of Education in Computer Science**
7. **Bachelor of Science in Mathematics**
8. **Bachelor of Science in Chemistry**

### **Palabana University**
Palabana University is known for its emphasis on agricultural sciences and offers programs like:
1. **Bachelor of Science in Animal Science**
2. **Bachelor of Science in Crop Science**
3. **Bachelor of Science in Fisheries and Aquaculture**
4. **Bachelor of Science in Agricultural Economics**
5. **Bachelor of Science in Agribusiness Management**

These programs focus on education, agriculture, and science fields. You may want to check with the respective institutions for the latest updates or additional programs they might offer.
        University virtual tour videos to

        {
            "Copperbelt University": [
                "https://www.youtube.com/watch?v=1Hz5T3zhmmQ",
                "https://www.youtube.com/watch?v=qui5QgoXzuU&pp=ygUQY2J1IGNhbXB1cyB0b3VyIA%3D%3D",
                "https://www.youtube.com/embed/1Hz5T3zhmmQ",
                "https://www.youtube.com/embed/qui5QgoXzuU&pp=ygUQY2J1IGNhbXB1cyB0b3VyIA%3D%3D"
            ],
            "University of Zambia": [
                "https://www.youtube.com/watch?v=WxNNo3NCcow&pp=ygURdW56YSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/watch?v=Rc3-VMpPD9I&pp=ygURdW56YSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/embed/WxNNo3NCcow&pp=ygURdW56YSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/embed/Rc3-VMpPD9I&pp=ygURdW56YSBjYW1wdXMgdG91ciA%3D"
            ],
            "Kapasa Makasa University": [
                "https://www.youtube.com/watch?v=nlcCdhm3cbY&pp=ygUaa2FwYXNhIG1ha2FzYSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/watch?v=yjTKex7k4NI",
                "https://www.youtube.com/embed/nlcCdhm3cbY&pp=ygUaa2FwYXNhIG1ha2FzYSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/embed/yjTKex7k4NI"
            ],
            "Mulungushi University": [
                "https://www.youtube.com/watch?v=1D18MQwL8r0&pp=ygUXbXVsdW5ndXNoaSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/watch?v=JWQvtvmJPf0&pp=ygUXbXVsdW5ndXNoaSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/embed/1D18MQwL8r0&pp=ygUXbXVsdW5ndXNoaSBjYW1wdXMgdG91ciA%3D",
                "https://www.youtube.com/embed/JWQvtvmJPf0&pp=ygUXbXVsdW5ndXNoaSBjYW1wdXMgdG91ciA%3D"
            ],
            "Kwame Nkrumah University": [
                "https://www.youtube.com/watch?v=RGy10FSiSm0&pp=ygUZa3dhbWUgbmtydW1hIGNhbXB1cyB0b3VyIA%3D%3D",
                "https://www.youtube.com/watch?v=N4hrGVoicpw",
                "https://www.youtube.com/embed/RGy10FSiSm0&pp=ygUZa3dhbWUgbmtydW1hIGNhbXB1cyB0b3VyIA%3D%3D",
                "https://www.youtube.com/embed/N4hrGVoicpw"
            ]
        }
        you can embed these videos in the responses sometimes

        """


    # Craft the full prompt
    full_prompt = f"UniMatch is a recommender system for selecting the best ICT programs in Zambian public universities. On top of the available information with the following information:\n{knowledge_base}\n\n and can not go beyond the Zambian public universities context and anything not related to universities and ict User query: {prompt}"

    # Perform the chat completion
    response = client.chat_completion(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=500,
        stream=False,  # Set to True if you want streaming responses
    )

    # Extract and return the response text
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    prompt = "What are the best ICT programs at the University of Zambia?"
    print(get_response(prompt))
