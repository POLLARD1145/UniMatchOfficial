import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
#local/custom imports
import app.ai_logic.data_extraction.unirank_web as uni_rank


def preprocess_message(message):
    rank = 5
    tokens = [token for token in word_tokenize(message)]
    response = message
    for token in tokens:
        if token == "rank":
            rank_list = uni_rank.get_rank_list(rank)
            response = "\n- ".join([f"{i+1}. {uni}" for i, uni in enumerate(rank_list)])
    
    return response
    