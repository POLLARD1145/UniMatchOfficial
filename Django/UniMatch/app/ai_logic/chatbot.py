import testbot as nlp_bot

def get_response(user_input):
    nlp_response = nlp_bot.preprocess_message(user_input)

    chat_response =  nlp_response
    return chat_response
