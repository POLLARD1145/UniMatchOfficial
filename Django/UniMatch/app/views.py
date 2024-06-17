from django.shortcuts import render
from app.ai_logic import chatbot
from app.ai_logic.data_extraction import unirank_web as uw
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return render(request=request,template_name="index.html")

def chat(request):
    return render(request=request,template_name="chatbot/index.html")

def universities(request):
    unilist = uw.get_rank_list_all()
    context = {'Universities': unilist}
    return render(request=request,template_name="universities.html", context=context)

    
@csrf_exempt
def get_bot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Simulate bot response
            bot_message = f"You said: {user_message}. This is the message from the bot."

            return JsonResponse({'botMessage': bot_message})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
