import json

with open("app/ai_logic/jsonfiles/zambian_universities_and_programs.json") as file:
    data = json.load(file)

with open("app/ai_logic/jsonfiles/zambia_public_university.json") as file:
    public_uni = json.load(file)

with open("app/ai_logic/jsonfiles/opening_dates.json") as file:
    uni_calander = json.load(file)

def get_list_of_universities():
    return list(data.keys())
def get_program_and_university():
    return data
def get_public_universities():
    return public_uni
def get_opening_dates():
    return uni_calander