from django.shortcuts import render
from app.ai_logic import chatbot
from app.ai_logic.data_extraction import unirank_web as uw
# Create your views here.

def index(request):
    return render(request=request,template_name="index.html")

def chat(request):
    return render(request=request,template_name="chatbot/index.html")

def universities(request):
    unilist = uw.get_rank_list_all()
    context = {'Universities': unilist}
    return render(request=request,template_name="universities.html", context=context)

    