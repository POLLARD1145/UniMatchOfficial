import json
import os
import pandas as pd
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from textblob import TextBlob
import recommender

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class Chatbot:
    def __init__(self):
        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()
        
        # Initialize data and models
        self.data = self._load_data()
        self.pipeline, self.low_accuracy = self._train_model()
        self.user_sessions = {}
        self.feedback_storage = []
        self.intent_to_function = {
            "recommend_programs": self._recommend_programs,
            "list_programs": self._list_programs,
            "rank_universities": self._rank_universities,
            "list_universities": self._list_universities,
            "get_program_details": self._get_program_details,
            "admission_requirements": self._admission_requirements,
            "tuition_fees": self._tuition_fees,
            "campus_facilities": self._campus_facilities,
            "academic_calendar": self._academic_calendar,
            "scholarship_info": self._scholarship_info
        }

    def _load_data(self):
        # Load data from a JSON file
        file_path = os.path.join(os.path.dirname(__file__), 'jsonfiles/intents.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Transform JSON data into a DataFrame
        patterns = []
        intents = []
        responses = {}
        
        for intent in data['intents']:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                intents.append(intent['tag'])
            
            responses[intent['tag']] = intent['responses']
        
        self.responses = responses
        return pd.DataFrame({'queries': patterns, 'intents': intents})

    def _preprocess_text(self, text):
        # Correct typos using TextBlob
        corrected_text = str(TextBlob(text).correct())

        # Tokenize the text
        tokens = word_tokenize(corrected_text.lower())
        # Lemmatize and remove stopwords
        lemmatized_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalpha() and token not in stopwords.words('english')
        ]
        return " ".join(lemmatized_tokens)

    def _train_model(self):
        # Preprocess dataset
        df = self.data
        df['processed_queries'] = df['queries'].apply(self._preprocess_text)

        # Use a pipeline to handle the entire process
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression(max_iter=1000))
        ])

        # Set parameters for grid search
        parameters = {
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__C': [0.1, 1.0, 10.0],
            'clf__solver': ['lbfgs', 'liblinear']
        }

        # Grid search for hyperparameter tuning
        grid_search = GridSearchCV(pipeline, parameters, cv=5, scoring='accuracy')
        grid_search.fit(df['processed_queries'], df['intents'])

        # Evaluate the best model
        best_pipeline = grid_search.best_estimator_
        y_pred = best_pipeline.predict(df['processed_queries'])
        accuracy = accuracy_score(df['intents'], y_pred)
        print("Best Model Accuracy:", accuracy)
        print("Classification Report:\n", classification_report(df['intents'], y_pred))

        # Determine if feedback is needed based on accuracy
        low_accuracy = accuracy < 0.80

        return best_pipeline, low_accuracy

    def manage_session(self, user_id):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "stage": "initial",
                "details": {}
            }
        return self.user_sessions[user_id]

    def get_user_details(self, user_id):
        # Mockup functions for user details
        hobbies = self.get_user_hobbies(user_id)
        interests = self.get_user_interests(user_id)
        return {"hobbies": hobbies, "interests": interests}

    def get_user_hobbies(self, user_id):
        #get hobbies from the database
        from accounts.models import Hobby
        # Query the Hobby model for the given user_id
        hobbies = Hobby.objects.filter(user_id=user_id).values_list('name', flat=True)

        # Convert the QuerySet to a list
        return list(hobbies)

    def get_user_interests(self, user_id):
        # Database: Return a list of interests
        from accounts.models import Interest
        # Query the Interest model for the given user_id
        interests = Interest.objects.filter(user_id=user_id).values_list('name', flat=True)
        return list(interests)

    def get_response(self, user_message, user_id):
        # Manage user session
        session = self.manage_session(user_id)
        user_details = self.get_user_details(user_id)

        # Preprocess the user message
        processed_message = self._preprocess_text(user_message)

        # Use the pipeline to predict the intent
        predicted_intent = self.pipeline.predict([processed_message])[0]

        # Handle responses based on the current session stage
        if session["stage"] == "initial":
            if predicted_intent in self.intent_to_function:
                return self.intent_to_function[predicted_intent](user_details)
            else:
                # Randomly choose a response from the predefined ones
                return random.choice(self.responses.get(predicted_intent, ["I'm sorry, I didn't understand that. Can you please rephrase?"]))
        
        elif session["stage"] == "collecting_details":
            if "strengths" not in session["details"]:
                session["details"]["strengths"] = user_message
                return "Thank you! Now, could you tell me about your weaknesses?"
            elif "weaknesses" not in session["details"]:
                session["details"]["weaknesses"] = user_message
                return "Got it! What are your interests?"
            elif "interests" not in session["details"]:
                # Use stored interests if available, else take user input
                session["details"]["interests"] = user_details.get('interests') or user_message
                return "Interesting! Lastly, what are your hobbies?"
            elif "hobbies" not in session["details"]:
                # Use stored hobbies if available, else take user input
                session["details"]["hobbies"] = user_details.get('hobbies') or user_message
                session["stage"] = "initial"
                # Now we have all the details, provide a recommendation
                return self._recommend_programs(session["details"])

        return "I'm sorry, I didn't understand that. Can you please rephrase?"

    # Placeholder functions for program listing, university ranking, and other features
    def _list_programs(self, user_details=None):
        programs = [
            "Bachelor of Science in Computer Science",
            "Bachelor of Software Engineering",
            "Bachelor of Information Systems",
            "Diploma in Information Technology"
        ]
        return "Here is the list of available programs:\n" + "\n".join(programs)

    def _rank_universities(self, user_details=None):
        universities = [
            "1. University of Zambia",
            "2. Copperbelt University",
            "3. Mulungushi University"
        ]
        return "Here is the ranking of universities in Zambia:\n" + "\n".join(universities)

    def _list_universities(self, user_details=None):
        universities = [
            "University of Zambia",
            "Copperbelt University",
            "Mulungushi University",
            "Kwame Nkrumah University",
            "Kapasa Makasa University"
        ]
        return "Here is the list of universities in Zambia:\n" + "\n".join(universities)

    def _get_program_details(self, user_details=None):
        # Simulate fetching details for a specific program
        return "The Bachelor of Science in Computer Science is a program focused on algorithms, data structures, and software development."

    def _admission_requirements(self, user_details=None):
        # Simulate providing admission requirements
        return "Admission to engineering programs requires a minimum of five O-Level credits, including Mathematics and English."

    def _tuition_fees(self, user_details=None):
        # Simulate providing information on tuition fees
        return "The tuition fee for the medicine program is approximately $2,000 per year."

    def _campus_facilities(self, user_details=None):
        # Simulate describing campus facilities
        return "The campus offers a library, sports facilities, research labs, and student housing."

    def _academic_calendar(self, user_details=None):
        # Simulate providing the academic calendar
        return "The academic year begins in September and ends in June, with breaks in December and April."

    def _scholarship_info(self, user_details=None):
        # Simulate providing scholarship information
        return "Scholarships are available based on academic merit and financial need. Applications are open in April each year."

    def _recommend_programs(self, user_details):
        # Use the recommender module to get program recommendations
        recommended_programs = recommender.recommend_based_on_interests(
            interests=user_details.get('interests', []),
            hobbies=user_details.get('hobbies', []),
            data=recommender.data
        )
        
        response = f"Based on your strengths {user_details.get('strengths', '')}, " \
                f"weaknesses {user_details.get('weaknesses', '')}, " \
                f"interests in {user_details.get('interests', '')}, " \
                f"and hobbies of {user_details.get('hobbies', '')}, " \
                f"we recommend the following programs:\n"
        
        for _, row in recommended_programs.iterrows():
            response += f"{row['name']} at {row['university']}.\n"
            
        response += "\nYou can update your details in the system to get more accurate recommendations."
        
        return response


    # Function to collect user feedback on responses
    def collect_feedback(self, user_message, bot_response):
        # Ask for feedback only if the model performance is low
        if self.low_accuracy:
            print(f"Bot: {bot_response}")
            rating = input("Please rate the accuracy of this response (1-5): ")
            if int(rating) <= 3:
                feedback = input("What would have been a more accurate response? (Optional): ")
                
                # Store the feedback
                self.feedback_storage.append({
                    "user_message": user_message,
                    "bot_response": bot_response,
                    "rating": rating,
                    "feedback": feedback
                })

                print("Thank you for your feedback!")

# Example usage
if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = Chatbot()

    # Example usage with user messages
    user_id = 1  # Simulated user ID for session management
    messages = [
        "Can you recommend some programs for me?",
        "I am good at problem solving.",
        "I struggle with time management.",
        "I am interested in technology and innovation.",
        "I enjoy playing video games and reading."
    ]

    for message in messages:
        print(f"User: {message}")
        bot_response = chatbot.get_response(message, user_id)
        print(f"Bot: {bot_response}")
        chatbot.collect_feedback(message, bot_response)

    # Output feedback storage to see collected feedback
    print("\nCollected Feedback:")
    for feedback in chatbot.feedback_storage:
        print(feedback)
