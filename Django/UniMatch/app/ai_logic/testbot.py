import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
#local/custom imports
import unirank_web as uni_rank
import data_preprocessor as preprocessor


def preprocess_message(message, user):
    rank = 5
    tokens = [token for token in word_tokenize(message)]
    response = ""
    for token in tokens:
        if token.__contains__("rank"):
            rank_list = uni_rank.get_rank_list(rank)
            response = """Here is the list of the top 5 universities in Zambia as of UniRank
            \n- """+"\n".join([f"{i+1}. {uni}" for i, uni in enumerate(rank_list["name"])])
        elif token.__contains__("list"):
            rank_list = uni_rank.get_rank_list_all()
            response = """Here is the list of universities in Zambia
            \n- """+"\n".join([f"{i+1}. {uni}" for i, uni in enumerate(rank_list["name"])])
        else:
            response = preprocessor.get_message(message,user_id=user)
    return response
    
if __name__ == "main":
    #do nothing
    preprocess_message("Hello", 12)