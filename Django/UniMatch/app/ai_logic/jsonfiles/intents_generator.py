import json
import random

# Load existing intents from JSON file Django/UniMatch/app/ai_logic/jsonfiles/intents.json
with open('../UniMatch/app/ai_logic/jsonfiles/intents.json', 'r') as file:
    data = json.load(file)

existing_intents = data["intents"]

# Core categories and sample data for new intents
new_categories = {
    "scholarships": {
        "patterns": ["Are there scholarships for ICT programs?", "ICT scholarships", "Funding for ICT studies", "Financial aid for ICT degrees"],
        "responses": ["Yes, there are scholarships available for ICT programs at various universities. Would you like information on scholarships for a specific university?", "Scholarships for ICT programs are offered by several universities and organizations. Do you have a particular university or scholarship program in mind?"]
    },
    "program_duration": {
        "patterns": ["How long are the ICT programs?", "Duration of ICT courses", "ICT degree length", "Length of ICT studies"],
        "responses": ["The duration of ICT programs typically ranges from 3 to 4 years for undergraduate degrees. Postgraduate programs may take 1 to 2 years. Do you need information on a specific program?", "ICT undergraduate degrees usually take 3 to 4 years to complete. Are you looking for details on undergraduate or postgraduate program durations?"]
    },
    # Add more categories and data here...
}

def create_intents(categories, num_variations=5):
    intents = []
    for tag, data in categories.items():
        patterns = data['patterns']
        responses = data['responses']
        for i in range(num_variations):
            intent = {
                "tag": f"{tag}_{i}",
                "patterns": random.sample(patterns, min(len(patterns), 3)),
                "responses": random.sample(responses, min(len(responses), 2))
            }
            intents.append(intent)
    return intents

# Generate new intents
num_intents_per_category = 2  # Adjust as needed
new_intents = create_intents(new_categories, num_variations=num_intents_per_category)

# Append new intents to existing intents
existing_intents.extend(new_intents)

# Save the updated intents back to the JSON file
with open('../UniMatch/app/ai_logic/jsonfiles/intents.json', 'w') as file:
    json.dump({"intents": existing_intents}, file, indent=4)

print(f"Appended {len(new_intents)} new intents. Total intents: {len(existing_intents)}")
