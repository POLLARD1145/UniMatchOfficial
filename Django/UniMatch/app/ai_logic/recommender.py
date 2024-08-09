import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample user profile
user_profile = {
    "interests": "education,",
    "academic_results": "high",
    "hobbies": "coding, solving puzzles, technology"
}

# University programs data with associated interests
data = {
    "University of Zambia": [
        {"name": "Software Engineering (SE)", 
         "description": "Focus on designing, developing, and maintaining software systems.", 
         "level": "Degree", 
         "interests": "software development, programming, systems design, technology"},
        {"name": "Computer Systems Engineering (CSE)", 
         "description": "Combines computer science and electrical engineering for system design.", 
         "level": "Degree", 
         "interests": "hardware, systems architecture, electronics, programming"},
        {"name": "Bachelor of Science in Computer Science", 
         "description": "Comprehensive program covering algorithms, data structures, and software design.", 
         "level": "Degree", 
         "interests": "algorithms, data structures, software development, computer theory"}
    ],
    "Copperbelt University": [
        {"name": "Diploma in Information Technology", 
         "description": "Entry-level program in IT, focusing on basic skills and knowledge.", 
         "level": "Diploma", 
         "interests": "basic IT skills, computer applications, technology"},
        {"name": "Bachelor of Science in Computer Science", 
         "description": "Focuses on computational theory, programming, and problem-solving.", 
         "level": "Degree", 
         "interests": "programming, problem-solving, computational theory"},
        {"name": "Bachelor of Science in Information System", 
         "description": "Study of systems that manage, process, and analyze data.", 
         "level": "Degree", 
         "interests": "data management, information systems, data analysis"},
        {"name": "Masters of Science in Computer Science", 
         "description": "Advanced studies in computer science research and applications.", 
         "level": "Masters", 
         "interests": "research, advanced computing, algorithms"},
        {"name": "PhD in Computer Science", 
         "description": "Research-focused program aimed at creating new knowledge in the field.", 
         "level": "Doctorate", 
         "interests": "research, innovation, computing"}
    ],
    "Mulungushi University": [
        {"name": "Bachelor of Science in Computer Science", 
         "description": "Foundational program in computer science principles and applications.", 
         "level": "Degree", 
         "interests": "programming, algorithms, applications"},
        {"name": "Bachelor of Science in Information Technology", 
         "description": "Covers a wide range of topics in IT with a practical approach.", 
         "level": "Degree", 
         "interests": "IT skills, practical computing, technology"},
        {"name": "Bachelor of Science in Information Systems", 
         "description": "Focuses on information systems design, development, and management.", 
         "level": "Degree", 
         "interests": "systems design, information management, data systems"},
        {"name": "Bachelor of Science in Data Science", 
         "description": "Introduces data analysis, machine learning, and big data technologies.", 
         "level": "Degree", 
         "interests": "data science, machine learning, big data"},
        {"name": "Bachelor of Science in Cyber Security", 
         "description": "Teaches security principles, risk management, and cyber threat prevention.", 
         "level": "Degree", 
         "interests": "cybersecurity, risk management, security systems"}
    ],
    "Kwame Nkrumah University": [
        {"name": "Bachelor of ICT with Education", 
         "description": "Integrates ICT skills with educational practices for teaching roles.", 
         "level": "Degree", 
         "interests": "education, ICT, teaching"}
    ],
    "Kapasa Makasa University": [
        {"name": "Bachelor of ICT with Education", 
         "description": "Prepares students for educational roles in ICT.", 
         "level": "Degree", 
         "interests": "ICT, education, teaching"}
    ]
}

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

# Display the recommended programs with similarity scores
print("Recommended Programs:")
print(recommended_programs[['university', 'name', 'similarity']].head())
