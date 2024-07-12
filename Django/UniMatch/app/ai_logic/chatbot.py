import testbot as nlp_bot

def get_response(user_input, userid):
    
    nlp_response = nlp_bot.preprocess_message(user_input, userid)

    chat_response =  nlp_response
    return chat_response
