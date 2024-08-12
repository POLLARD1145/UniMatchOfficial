import json
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load data from a JSON file
def load_university_data(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Load university programs data from JSON file
file_path = 'app/ai_logic/jsonfiles/university_program.json'

data = load_university_data(file_path)

def get_user_recommended_programs(user_profile):
    # Extract relevant information from the user's profile
    return recommend_programs(user_profile=user_profile, data=data)

# Function to recommend programs based on user profile
def recommend_programs(user_profile, data):
    # Flatten the data into a DataFrame
    programs = []
    for university, courses in data.items():
        for course in courses:
            programs.append({
                "university": university,
                "name": course["name"],
                "description": course["description"],
                "level": course["level"],
                "interests": course["interests"]
            })

    df = pd.DataFrame(programs)

    # Combine program attributes for vectorization
    df['combined_features'] = df.apply(lambda x: f"{x['description']} {x['level']} {x['interests']}", axis=1)

    # Combine user profile into a single string
    user_profile_text = f"{user_profile['interests']} {user_profile['academic_results']} {user_profile['hobbies']}"

    # Vectorize both combined program features and user profile using TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_features'])

    # Vectorize the user profile text
    user_profile_vector = tfidf_vectorizer.transform([user_profile_text])

    # Compute cosine similarity between the user profile and all programs
    cosine_sim = cosine_similarity(user_profile_vector, tfidf_matrix)

    # Add similarity scores to the DataFrame
    df['similarity'] = cosine_sim.flatten()

    # Recommend top programs based on similarity scores
    recommended_programs = df.sort_values(by='similarity', ascending=False)

    # Return the top 3 recommended programs with similarity scores
    return recommended_programs[['university', 'name', 'similarity']].head(3)

# Function to get interests from chatbot and recommend programs
def recommend_based_on_interests(interests, hobbies, data):
    # Construct a mock user profile based on interests
    user_profile = {
        "interests": ", ".join(interests),
        "academic_results": "average",  # Can be adjusted based on chatbot input
        "hobbies": ", ".join(hobbies),  # Can be adjusted based on chatbot input
    }
    
    # Get recommended programs
    recommended_programs = recommend_programs(user_profile, data)
    
    # Return the top recommended programs
    return recommended_programs

# Example usage: get interests from chatbot and recommend programs
if __name__ == "__main__":
    # Mock user interests and hobbies
    chatbot_interests = ["education", "ai"]
    chatbot_hobbies = ["reading", "coding"]

    # Get recommendations based on interests and hobbies
    recommended_programs = recommend_based_on_interests(chatbot_interests, chatbot_hobbies, data)

    # Display the recommended programs
    print("Recommended Programs Based on Interests and Hobbies:")
    print(recommended_programs)
