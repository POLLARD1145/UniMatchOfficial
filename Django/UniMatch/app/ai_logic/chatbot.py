import testbot as nlp_bot


def handle_list_programs(data):
    # List all available programs from the data
    programs = []
    for university, courses in data.items():
        for course in courses:
            programs.append(f"{course['name']} at {university}")
    response = "Here are all the available programs:\n" + "\n".join(programs)
    return response


def get_response(user_input, userid):
    
    nlp_response = nlp_bot.preprocess_message(user_input, userid)

    chat_response =  nlp_response
    return chat_response
