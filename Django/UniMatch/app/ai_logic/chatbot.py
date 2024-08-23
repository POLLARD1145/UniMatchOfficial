import json
import os
import pandas as pd
import random
import nltk
from nltk import pos_tag
import pickle
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
from nltk import pos_tag, word_tokenize, ne_chunk
from nltk.util import ngrams
from collections import Counter



# Download necessary NLTK data
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')

class Chatbot:
    def __init__(self):
        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()

        # Initialize data and models
        self.data = self._load_data()
        self.pipeline, self.low_accuracy = self._load_or_train_model()
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
            "scholarship_info": self._scholarship_info,
            "get_ict_programs_response": self.get_ict_programs_response
        }

    def _load_or_train_model(self):
        model_path = os.path.join(os.path.dirname(__file__), 'ai_models/trained_model.pkl')

        # Check if the model file exists
        if os.path.exists(model_path):
            # Load the saved model
            with open(model_path, 'rb') as model_file:
                best_pipeline = pickle.load(model_file)
            print("Loaded trained model from file.")
            
            # Evaluate the loaded model
            df = self.data
            df['processed_queries'] = df['queries'].apply(self._preprocess_text)
            y_pred = best_pipeline.predict(df['processed_queries'])
            accuracy = accuracy_score(df['intents'], y_pred)
            #print("Loaded Model Accuracy:", accuracy)
            #print("Classification Report:\n", classification_report(df['intents'], y_pred))

            # Determine if feedback is needed based on accuracy
            low_accuracy = accuracy < 0.8
            return best_pipeline, low_accuracy

        else:
            # Train the model if no saved model is found
            return self._train_model()

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

        # Save the trained model to a file
        model_path = os.path.join(os.path.dirname(__file__), 'ai_models/trained_model.pkl')
        with open(model_path, 'wb') as model_file:
            pickle.dump(best_pipeline, model_file)

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
        try:
            from accounts.models import Hobby

            # Query the Hobby model for the given user_id
            hobbies = Hobby.objects.filter(user_id=user_id).values_list('name', flat=True)

            # Convert the QuerySet to a list
            return list(hobbies)
        except ModuleNotFoundError:
            return None

    def get_user_interests(self, user_id):
        try:
            # Database: Return a list of interests
            from accounts.models import Interest
            # Query the Interest model for the given user_id
            interests = Interest.objects.filter(user_id=user_id).values_list('name', flat=True)
            return list(interests)
        except:
            return None
    
    def extract_keywords(self, text):
        # Correct spelling and preprocess text
        try:
            corrected_text = str(TextBlob(text).correct())
        except Exception as e:
            corrected_text = text  # Fallback to original text if correction fails
            print(f"TextBlob correction failed: {e}")

        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(corrected_text.lower())
        tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        
        # Lemmatize tokens
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        # Extract nouns and adjectives
        tagged_tokens = pos_tag(lemmatized_tokens)
        keywords = [word for word, pos in tagged_tokens if pos in ('NN', 'JJ')]
        
        # Filter out non-hobby terms like 'love'
        relevant_keywords = [word for word in keywords if word not in ['love', 'enjoy', 'like']]
        
        # Identify common bigrams (two-word phrases)
        bigrams = [' '.join(bigram) for bigram in ngrams(lemmatized_tokens, 2)]
        
        # Filter bigrams that contain relevant keywords
        bigram_keywords = [bigram for bigram in bigrams if any(word in bigram for word in relevant_keywords)]
        
        # Combine unigrams and bigrams
        all_keywords = list(set(relevant_keywords + bigram_keywords))
        
        # Sort keywords for better readability
        all_keywords.sort()
        
        return all_keywords

    def get_response(self, user_message, user_id):
        session = self.manage_session(user_id)
        user_details = self.get_user_details(user_id)

        processed_message = self._preprocess_text(user_message)

        # Predict intent and confidence
        intent_proba = self.pipeline.predict_proba([processed_message])[0]
        predicted_intent = self.pipeline.classes_[intent_proba.argmax()]
        confidence = intent_proba.max()
        
        confidence_threshold = 0.7  # Example threshold
        # Handle responses based on the current session stage
        if session["stage"] == "initial":
            if predicted_intent in self.intent_to_function:
                if predicted_intent == "recommend_programs":
                    session["stage"] = "collecting_details"
                    return "Great! Can you tell me about your strengths?"
                elif predicted_intent == "get_ict_programs_response":
                    session["stage"] = "collecting_university_name"
                    return self.get_ict_programs_response(user_message)
                elif predicted_intent == "academic_calendar":
                    return self._academic_calendar(user_message)
                else:
                    return self.intent_to_function[predicted_intent](user_details)
            elif predicted_intent in self.data['intents'].unique():
                return random.choice(self.responses[predicted_intent])
            else:
                return "I'm sorry, I didn't understand your request. Can you please rephrase?, topics to ask on \n- recommendations for you \n- list of universities for ict."
        
        elif session["stage"] == "collecting_details":
            if "strengths" not in session["details"]:
                session["details"]["strengths"] = self.extract_keywords(user_message)
                return "Thank you! Now, could you tell me about your weaknesses?"
            elif "weaknesses" not in session["details"]:
                session["details"]["weaknesses"] = self.extract_keywords(user_message)
                return "Got it! What are your interests?"
            elif "interests" not in session["details"]:
                session["details"]["interests"] = self.extract_keywords(user_message)
                return "Interesting! Lastly, what are your hobbies?"
            elif "hobbies" not in session["details"]:
                session["details"]["hobbies"] = self.extract_keywords(user_message)
                session["stage"] = "initial"
                return self._recommend_programs(session["details"])
        elif session["stage"] == "collecting_university_name":
            session["stage"] = "initial"
            return self.get_ict_programs_response(user_message)
        else:
            if confidence < confidence_threshold:
                return "I'm sorry, I didn't understand that. Can you please rephrase?"
            else:
                return random.choice(self.responses[predicted_intent])

    # Functions for program listing, university ranking, and other features
    def get_ict_programs_response(self, user_input=None):
        import qualifications_data as qd
        ict_universities = qd.get_public_universities()
        
        if user_input:
            # Identify the university name from the user input
            university_name = self.identify_university(user_input)
            
            if university_name:
                # Search for the identified university in the list
                for uni, details in ict_universities.items():
                    if university_name.lower() in uni.lower():
                        response = f"Here is the list of ICT programs offered at {uni} (Location: {details['location']}):\n"
                        for program in details.get('programs', []):
                            response += f"- {program.get('name', 'Unknown Program Name')}: {program.get('description', 'No description available')} (Level: {program.get('level', 'Unknown')})\n"
                        return response
                # If the identified university is not found in the list
                return "I'm sorry, I couldn't find any information on that university. Kindly type the university name in full."
            
            else:
                # If no university name was identified from the user input
                return "I'm sorry, I couldn't determine the university you are asking about. Please provide more details or the full name of the university."
                
        
        else:
            # List all universities and their ICT programs if no specific university is mentioned
            response = "Here is the list of ICT programs offered by public universities in Zambia:\n"
            for uni, details in ict_universities.items():
                response += f"###### {uni} (Location: {details['location']}):\n"
                for program in details.get('programs', []):
                    response += f"- {program.get('name', 'Unknown Program Name')}: {program.get('description', 'No description available')} (Level: {program.get('level', 'Unknown')})\n"
            return response
   
    def identify_university(self, user_input):
        """
        This function identifies and returns the full university name based on the user input.
        It converts known abbreviations or short forms into their corresponding full names.
        """
        university_mapping = {
            "cbu": "Copperbelt University",
            "unza": "University of Zambia",
            "kmu": "Kapasa Makasa University",
            "mu": "Mulungushi University",
            "Mulungushi": "Mulungushi University",
            "knu": "Kwame Nkrumah University",
            "kapasa makasa": "Kapasa Makasa University",
            "kwame nkrumah": "Kwame Nkrumah University",
            "kwame": "Kwame Nkrumah University",
            "nkrumah": "Kwame Nkrumah University",
            "Copperbelt": "Copperbelt University",
            "CBU": "Copperbelt University",
            "UNZA": "University of Zambia",
            "KMU": "Kapasa Makasa University",
            "MU": "Mulungushi University",
            "KNU": "Kwame Nkrumah University",
            
        }
        user_input = user_input.lower()
        for short_form, full_name in university_mapping.items():
            if short_form in user_input:
                return full_name
        return None

    def _list_programs(self, user_details=None):
        import qualifications_data as qd
        ict_universities = qd.get_public_universities()
        response = "Here is the list of ICT programs offered by public universities in Zambia:\n"
        
        for uni, details in ict_universities.items():
            response += f"###### {uni} (Location: {details['location']})\n"
            for program in details.get('programs', []):
                if isinstance(program, dict):
                    response += f"- {program.get('name', 'Unknown Program Name')}: {program.get('description', 'No description available')} (Level: {program.get('level', 'Unknown')})\n"
                else:
                    response += f"- {program}\n"  # In case program is a string or another type
        
        return response + "\n"

    def _rank_universities(self, user_details=None):
        import unirank_web as rank
        universities_info = rank.get_rank_list(5)  # Get the top 5 universities
        
        university_list = [
            f"- **{rank}**: {name} in {town}"
            for rank, name, town in zip(
                universities_info["rank"], universities_info["name"], universities_info["town"]
            )
        ]
        
        return (
            "The top 5 universities in Zambia according to the [4icu.org](https://www.4icu.org/zm/) ranking are:\n"
            + "\n".join(university_list)
        )

    def _list_universities(self, user_details=None):
        import qualifications_data as qd
        universities = qd.get_list_of_universities()
        return "Here is the list of universities in Zambia:\n" + "\n- ".join(universities)

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

    def _academic_calendar(self, user_message=None):
        # Simulate providing the academic calendar
        import qualifications_data as qd
        universities = qd.get_opening_dates()

        if user_message:
            # Identify the university name from the user input
            university_name = self.identify_university(user_message)
            
            if university_name:
                # Check if the identified university exists in the data
                if university_name in universities:
                    uni_data = universities[university_name]
                    
                    responses = [
                        f"The academic year at **{university_name}** typically begins in {uni_data['open']} and ends in {uni_data['close']}. For mid-year breaks, you can check the university website.",
                        f"The academic year at **{university_name}** generally kicks off in {uni_data['open']} and concludes in {uni_data['close']}. Check their website for more on mid-year breaks.",
                        f"For **{university_name}**, the academic year usually begins in {uni_data['open']} and ends in {uni_data['close']}. You can find mid-year break info on their website.",
                        f"**{university_name}** commences its academic year in {uni_data['open']} and closes in {uni_data['close']}. For mid-year breaks, refer to their official site.",
                        f"The academic calendar for **{university_name}** usually starts in {uni_data['open']} and finishes in {uni_data['close']}. Visit their site for mid-year break schedules.",
                        f"**{university_name}** academic year typically begins in {uni_data['open']} and ends in {uni_data['close']}. Mid-year breaks are detailed on their website.",
                        f"At **{university_name}**, the academic year usually starts in {uni_data['open']} and ends in {uni_data['close']}. Check out their site for mid-year break information.",
                        f"**{university_name}** starts its academic year in {uni_data['open']} and concludes in {uni_data['close']}. More details, including mid-year breaks, can be found on their website.",
                        f"The academic year at **{university_name}** generally begins in {uni_data['open']} and ends around {uni_data['close']}. For more information, visit their website.",
                        f"**{university_name}** usually opens its academic year in {uni_data['open']} and wraps it up in {uni_data['close']}. Check their official site for details on mid-year breaks."
                    ]
                    
                    # Randomly select a response
                    import random
                    response = random.choice(responses)
                    response += f"\nFor the most accurate and up-to-date information, please refer to the official academic calendar available on their website: [{university_name}]({uni_data['link']})"
                    response += "\nMake sure to check these links regularly for any updates."
                    return response
                
                else:
                    return "I'm sorry, I couldn't find any information on that university. Kindly type the university name in full."
            
            else:
                # If no university name was identified from the user input
                return "I'm sorry, I couldn't determine the university you are asking about. I'm only trained on Zambian Public Universities offering ICT programs."
        
        else:
            return "I'm sorry, I couldn't determine the university you are asking about. I'm only trained on Zambian Public Universities offering ICT programs."

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
        response = ""

        if user_details.get('strengths'):
            response += f"###### Your Strengths:\n"
            response += "We noticed these standout qualities:\n"
            for strength in user_details['strengths']:
                response += f"- {strength}\n"
            response += "\n"

        if user_details.get('weaknesses'):
            response += f"###### Areas to Improve:\n"
            response += "Everyone has things to work on. Here are yours:\n"
            for weakness in user_details['weaknesses']:
                response += f"- {weakness}\n"
            response += "\n"

        if user_details.get('interests'):
            response += f"###### What Excites You:\n"
            response += "These are your key interests:\n"
            for interest in user_details['interests']:
                response += f"- {interest}\n"
            response += "\n"

        if user_details.get('hobbies'):
            response += f"###### Your Hobbies:\n"
            response += "We see you enjoy these activities:\n"
            for hobby in user_details['hobbies']:
                response += f"- {hobby}\n"
            response += "\n"

        response += "###### What you can study:\n\n"

        recommendations = [
            f"Based on the information you've provided, you should pursue **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"Given your background, we recommend **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"With your strengths and interests, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** would be a great fit.",
            f"We suggest you study **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** based on your profile.",
            f"Considering what you've shared, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** is highly recommended.",
            f"Our analysis indicates that **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** is an ideal match for you.",
            f"Your profile suggests that **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** would be a perfect choice.",
            f"You should consider studying **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"**{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** is a strong recommendation based on your provided details.",
            f"Given your interests and strengths, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** is a suitable option."
        ]

        # Randomly select a recommendation response
        import random
        response += random.choice(recommendations)

        response += "\n\n*Feel free to update your details anytime for even better recommendations!*"

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
        "top university to study computer science",
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
