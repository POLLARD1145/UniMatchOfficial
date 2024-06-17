import app.ai_logic.natural_language_processing.testbot as nlp_bot

def get_response(user_input):
    nlp_response = nlp_bot.preprocess_message(user_input)

    chat_response = f"Hello, how are you doing today? You said {user_input}" + nlp_response
    return chat_response
