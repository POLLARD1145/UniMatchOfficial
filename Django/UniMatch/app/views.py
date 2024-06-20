from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
#local imports
#add ai_logic to the system path for imports
import sys
import os
# Add the subdirectory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_logic'))
#import now
from .ai_logic import chatbot as chatbot, unirank_web as uw

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
            bot_message = chatbot.get_response(user_message)

            return JsonResponse({'botMessage': bot_message})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
