from django.shortcuts import render
from app.ai_logic import chatbot
# Create your views here.

def index(request):
    return render(request=request,template_name="index.html")

def chat(request):
    return render(request=request,template_name="chatbot/index.html")

print("Hello there, I'm your personal assitant, how canI assist you today?, to exit the chat just type 'quit'")
while True:
    user_input = input("You: ")
    if(user_input == "quit"):
        print("UniMatch: Thank you, have a great day, feel free to talk to me again.")
        break
    else:
        bot_response = chatbot.get_response(user_input=user_input)
        print("UniMatch: ",bot_response)
        
    