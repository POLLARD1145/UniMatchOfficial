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
prompt = "Which university offers the best program for Cyber Security in Zambia?"
response = generate_response(prompt)
print(response)
