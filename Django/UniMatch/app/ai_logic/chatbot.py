import matplotlib
matplotlib.use('Agg')  # Ensure this is added at the top of your script
import json
import os
import pandas as pd
import random
import re
import nltk
from nltk import pos_tag
import pickle
import matplotlib.pyplot as plt
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
        self.image_folder = "./static/images/generated"
        self.programs_and_universities = {
            "Computer Science": ["University of Zambia", "Copperbelt University", "Mulungushi University"],
            "Computer Engineering": ["University of Zambia", "Copperbelt University", "Mulungushi University"],
            "Software Engineering": ["University of Zambia"],
            "Information Technology": ["Copperbelt University", "Mulungushi University"],
            "Information Systems": ["Copperbelt University"],
            "Cyber Security": ["Mulungushi University", "Kapasa Makasa University"],
            "ICT with Education": ["Kwame Nkrumah University", "Kapasa Makasa University"]
        }
        self.program_shortcut_mapping = {
            "cs": "Computer Science",
            "computer science": "Computer Science",
            "cyber security": "Cyber Security",
            "Cybersec": "Cyber Security",
            "cybersec": "Cyber Security",
            "cyber security": "Cyber Security",
            "ce": "Computer Engineering",
            "ict": "ICT with Education",
            "ict with education": "ICT with Education",
            "computer engineering": "Computer Engineering",
            "se": "Software Engineering",
            "software engineering": "Software Engineering",
            "it": "Information Technology",
            "information technology": "Information Technology",
            "is": "Information Systems",
            "information systems": "Information Systems",
            "cse": "Computer Systems Engineering",
            "computer systems engineering": "Computer Systems Engineering",
            "info tech": "Information Technology",
            "info sys": "Information Systems",
            "ds": "Data Science",
            "data science": "Data Science",
            "cysec": "Cyber Security",
            "ml": "Machine Learning",
            "machine learning": "Machine Learning",
            "ai": "Artificial Intelligence",
            "artificial intelligence": "Artificial Intelligence",
            "net sec": "Network Security",
            "network security": "Network Security",
            "cs eng": "Computer Science and Engineering",
            "computer science and engineering": "Computer Science and Engineering",
            "it sec": "Information Technology Security",
            "information technology security": "Information Technology Security",
            "sys admin": "Systems Administration",
            "systems administration": "Systems Administration",
            "comp eng": "Computer Engineering",
            "info sec": "Information Security",
            "information security": "Information Security",
            "soft dev": "Software Development",
            "software development": "Software Development",
            "data eng": "Data Engineering",
            "data engineering": "Data Engineering"
        }
        # Structure for programs and their top-ranked universities
        self.program_rankings = {
            "Cyber Security": {
                "Mulungushi University": 1,
                "Kapasa Makasa Univerity": 2
            },
            "Computer Science": {
                "University of Zambia": 1,
                "Copperbelt University": 2,
                "Mulungushi University": 3,
                "Kwame Nkrumah University": 4
            },
            "Computer Engineering": {
                "Copperbelt University": 1,
                "University of Zambia": 2,
                "Mulungushi University": 3
            },
            "Software Engineering": {
                "University of Zambia": 1
            },
            "Information Technology": {
                "Copperbelt University": 1,
                "Kwame Nkrumah University": 2,
                "Mulungushi University": 3
            },
            "Information Systems": {
                "Copperbelt University": 1,
                "Kwame Nkrumah University": 2,
                "Mulungushi University": 3
            },
            "Data Science": {
                "Mulungushi University": 1
            }
        }
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
            "get_ict_programs_response": self.get_ict_programs_response,
            "program_inquiry": self._program_inquiry,
            "best_university_for_study": self._get_best_university_response
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
                    phrases = [
                        "Before I can help you with matching the right university for you, kindly provide me with the following information. What are your strengths?",
                        "Sure! To assist you better, I'd like to know more about you. Could you tell me about your strengths?",
                        "Of course! Let's start by getting to know you better. What would you say are your strengths?",
                        "I'm here to help you find the best match. First, could you share your strengths with me?",
                        "Let's begin by understanding your strong points. Can you tell me about your strengths?",
                        "To ensure I recommend the best fit, I'd like to know about your strengths. What are they?",
                        "Great! To guide you effectively, I'll need to know your strengths first. What are they?",
                        "Before proceeding, I'd like to know more about you. Could you tell me your strengths?",
                        "I'd be happy to assist you! But first, let's talk about your strengths. What are they?",
                        "Let's start the process by discussing your strengths. What do you consider to be your strongest qualities?"
                    ]
                    
                    return random.choice(phrases)
                elif predicted_intent == "get_ict_programs_response":
                    session["stage"] = "collecting_university_name"
                    return self.get_ict_programs_response(user_message)
                elif predicted_intent == "academic_calendar":
                    return self._academic_calendar(user_message)
                elif predicted_intent == "program_inquiry":
                    return self._program_inquiry(user_message)
                elif predicted_intent == "best_university_for_study":
                    return self._get_best_university_response(user_message)
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
   
    def _program_inquiry(self, user_message=None):
        # Example list of programs and universities offering them
        self.programs_and_universities = {
            "Computer Science": ["University of Zambia", "Copperbelt University", "Mulungushi University"],
            "Computer Engineering": ["University of Zambia", "Copperbelt University", "Mulungushi University"],
            "Software Engineering": ["University of Zambia"],
            "Information Technology": ["Copperbelt University", "Mulungushi University"],
            "Information Systems": ["Copperbelt University"],
            "Cyber Security": ["Mulungushi University", "Kapasa Makasa University"],
            "ICT with Education": ["Kwame Nkrumah University", "Kapasa Makasa University"]
        }

        # Program synonyms mapping
        program_mapping = self.program_shortcut_mapping


        def filter_universities_for_program(program):
            # Get universities offering the identified program
            if program in self.programs_and_universities:
                return self.programs_and_universities[program]
            else:
                return []

        def generate_response(program, universities):
            response_phrases = [
                f"You can pursue **{program}** at the following universities: {'\n- **'.join(universities)}",
                f"Here are some great places to study **{program}**: {', **'.join(universities)}",
                f"If you're interested in **{program}**, you can study at these universities: {', '.join(universities)}.",
                f"Looking to study **{program}**? Consider these universities: {', '.join(universities)}.",
                f"**{program}** is offered at: {', '.join(universities)}.",
                f"For **{program}**, check out these universities: {', '.join(universities)}.",
                f"You'll find **{program}** programs at: {', '.join(universities)}.",
                f"The following universities offer **{program}**: {', '.join(universities)}.",
                f"These universities provide **{program}** courses: {', '.join(universities)}.",
                f"If you're aiming for a degree in **{program}**, consider these institutions: {', '.join(universities)}."
            ]
            return random.choice(response_phrases)
        
        # Example usage:
        program = self.identify_program(user_message)
        if program:
            universities = filter_universities_for_program(program)
            if universities:
                return generate_response(program, universities)
            else:
                return "Sorry, it seems we don't have information on universities offering that program."
        else:
            return "Sorry, I couldn't identify the program you're asking about."


    # Function to visualize program rankings and save the chart as an image
    def visualize_and_save_program_rankings(self, program_rankings):
        for program, rankings in program_rankings.items():
            universities = list(rankings.keys())
            ranks = list(rankings.values())

            plt.figure(figsize=(10, 6))
            plt.barh(universities, ranks, color='skyblue')
            plt.xlabel('Rank')
            plt.ylabel('University')
            plt.title(f'{program} Rankings')
            plt.gca().invert_yaxis()  # Higher rank (1) at the top
            plt.savefig(f'{program}_rankings.png')  # Save chart as image
            plt.close()  # Close the figure after saving



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

    def identify_program(self, user_input):
        """
        Identifies and returns the program name based on the user input.
        Matches both known program shortcuts and full forms with substrings in the user input.
        """
        program_mapping = self.program_shortcut_mapping
        # Save the charts as images
        #self.visualize_and_save_program_rankings(self.program_rankings)

        user_input = user_input.lower()
        for program_key, program_name in program_mapping.items():
            # Check if either the shortcut or the full form is a substring in the user input
            if program_key in user_input or program_name.lower() in user_input:
                return program_name
        return "Sorry, I couldn't identify the program you're asking about."

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
    

    def generate_ranking_chart(self, program_name):
        # Remove spaces from the program name
        safe_program_name = program_name.replace(" ", "_")

        # Get rankings and reverse the ranks to give larger portions to smaller ranks
        rankings = self.program_rankings[program_name]
        universities = list(rankings.keys())
        ranks = list(rankings.values())

        # Invert the ranks for the pie chart (smaller rank -> larger portion)
        inverted_ranks = [1 / rank for rank in ranks]
        
        # Generate pie chart
        plt.figure(figsize=(4, 4))
        plt.pie(inverted_ranks, labels=universities, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(universities))))
        plt.title(f'{program_name} Rankings')

        # Add a legend
        plt.legend(universities, title="Universities", loc="upper left", bbox_to_anchor=(1, 1))

        # Save the image
        image_path = os.path.join(self.image_folder, f'{safe_program_name}_rankings.png')
        image_path = image_path.replace('\\', '/')
        plt.savefig(image_path, bbox_inches='tight')
        plt.close()

        # Return the relative path for use in the HTML
        return f'../static/images/generated/{safe_program_name}_rankings.png'


    def _get_best_university_response(self, user_input):
        """
        Returns the best university for the specified program based on the user's input.
        """
        # Detect the program name from user input
        detected_program = self.identify_program(user_input)

        if detected_program:
            # Check if the detected program exists in the rankings
            if detected_program in self.program_rankings:
                # Get the top-ranked university for the detected program
                top_university = None
                top_rank = float('inf')
                for university, rank in self.program_rankings[detected_program].items():
                    if rank < top_rank:
                        top_rank = rank
                        top_university = university

                if top_university:
                    # Generate the chart
                    chart_path = self.generate_ranking_chart(detected_program)

                    response_templates = [
                        f"The top university for studying **{detected_program.replace('_', ' ')}** is **{top_university}**. Here are the rankings:\n![Rankings]({chart_path})",
                        f"When it comes to **{detected_program.replace('_', ' ')}**, **{top_university}** stands out as the best. Check the rankings:\n![Rankings]({chart_path})",
                        f"If you're looking for the best university for **{detected_program.replace('_', ' ')}**, **{top_university}** is your top choice. See the full rankings:\n![Rankings]({chart_path})",
                        f"For the program in **{detected_program.replace('_', ' ')}**, **{top_university}** is ranked the highest. Here's how others rank:\n![Rankings]({chart_path})",
                        f"The leading university for **{detected_program.replace('_', ' ')}** is **{top_university}**. Take a look at the full rankings:\n![Rankings]({chart_path})"
                    ]
                    return random.choice(response_templates)
                else:
                    return "I couldn't find the best university for the specified program."
            else:
                return "The specified program is not recognized in our rankings."
        else:
            return "I'm sorry, I couldn't determine the program you're asking about. Please specify the program (e.g., Computer Science, Software Engineering, Information Technology)."
     
    def _list_universities(self, user_details=None):
        import qualifications_data as qd
        universities = qd.get_list_of_universities()
        return "Here is the list of universities in Zambia:\n- " + "\n- ".join(universities)

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

        # Different phrasings for the recommendation
        recommendations = [
            f"Based on the information you've provided, you should pursue **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"Given your background, we recommend **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"With your strengths and interests, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** would be a great fit.",
            f"Our analysis suggests you study **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"Considering your profile, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** is highly recommended.",
            f"Looking at your details, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** is an ideal match.",
            f"Based on what you've shared, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** would be perfect for you.",
            f"Our recommendation: Study **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}**.",
            f"For you, **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** stands out as a great option.",
            f"Your strengths and interests make **{recommended_programs.iloc[0]['name']}** at **{recommended_programs.iloc[0]['university']}** a solid choice."
        ]

        # Randomly select a recommendation response
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
