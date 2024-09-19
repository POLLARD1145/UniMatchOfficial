
def generate_response(prompt):
    # The knowledge base about Zambian universities and their programs
    knowledge_base = """
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
    
    # Craft the final prompt by including the knowledge base
    full_prompt = f"As UniMatch, a recommender system for Zambian public universities, such as unza, cbu, mulungushi,kapasa makasa and mukuba university as well as kapasa makasa {prompt}"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    payload = {
        "inputs": full_prompt,
        "options": {"max_length": 150}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    generated_text = response.json()[0]['generated_text']
    return generated_text

# Example usage
prompt = "Which university offers the best program for cyber security in Zambia?"
response = generate_response(prompt)
print(response)

