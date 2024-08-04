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


# Enhanced sample data with levels and descriptions
universities_data = {
    "University of Zambia": [
        {"name": "Software Engineering (SE)", "description": "Focus on designing, developing, and maintaining software systems.", "level": "Degree"},
        {"name": "Computer Systems Engineering (CSE)", "description": "Combines computer science and electrical engineering for system design.", "level": "Degree"},
        {"name": "Bachelor of Science in Computer Science", "description": "Comprehensive program covering algorithms, data structures, and software design.", "level": "Degree"}
    ],
    "Copperbelt University": [
        {"name": "Diploma in Information Technology", "description": "Entry-level program in IT, focusing on basic skills and knowledge.", "level": "Diploma"},
        {"name": "Bachelor of Science in Computer Science", "description": "Focuses on computational theory, programming, and problem-solving.", "level": "Degree"},
        {"name": "Bachelor of Science in Information System", "description": "Study of systems that manage, process, and analyze data.", "level": "Degree"},
        {"name": "Masters of Science in Computer Science", "description": "Advanced studies in computer science research and applications.", "level": "Masters"},
        {"name": "PhD in Computer Science", "description": "Research-focused program aimed at creating new knowledge in the field.", "level": "Doctorate"}
    ],
    "Mulungushi University": [
        {"name": "Bachelor of Science (BSc) in Computer Science", "description": "Foundational program in computer science principles and applications.", "level": "Degree"},
        {"name": "Bachelor of Science (BSc) in Information Technology", "description": "Covers a wide range of topics in IT with a practical approach.", "level": "Degree"},
        {"name": "Bachelor of Science (BSc) in Information Systems", "description": "Focuses on information systems design, development, and management.", "level": "Degree"},
        {"name": "Bachelor of Science (BSc) in Data Science", "description": "Introduces data analysis, machine learning, and big data technologies.", "level": "Degree"},
        {"name": "Bachelor of Science (BSc) in Cyber Security", "description": "Teaches security principles, risk management, and cyber threat prevention.", "level": "Degree"}
    ],
    "Kwame Nkrumah University": [
        {"name": "Bachelor of ICT with Education", "description": "Integrates ICT skills with educational practices for teaching roles.", "level": "Degree"}
    ],
    "Kapasa Makasa University": [
        {"name": "Bachelor of ICT with Education", "description": "Prepares students for educational roles in ICT.", "level": "Degree"}
    ]
}

def general_recommendations(request):
    # Extract all programs, university names, and levels
    all_programs = {program['name'] for programs in universities_data.values() for program in programs}
    all_universities = universities_data.keys()
    all_levels = {program['level'] for programs in universities_data.values() for program in programs}
    
    # Get query parameters for filtering
    selected_program = request.GET.get('program')
    selected_university = request.GET.get('university')
    selected_level = request.GET.get('level')

    # Start with all data
    filtered_universities = universities_data

    # Apply program filter if selected
    if selected_program:
        filtered_universities = {
            uni: [prog for prog in progs if selected_program == prog['name']]
            for uni, progs in filtered_universities.items()
        }
        filtered_universities = {uni: progs for uni, progs in filtered_universities.items() if progs}
    
    # Apply university filter if selected
    if selected_university:
        filtered_universities = {
            uni: progs for uni, progs in filtered_universities.items() if selected_university == uni
        }

    # Apply level filter if selected
    if selected_level:
        filtered_universities = {
            uni: [prog for prog in progs if selected_level == prog['level']]
            for uni, progs in filtered_universities.items()
        }
        filtered_universities = {uni: progs for uni, progs in filtered_universities.items() if progs}

    context = {
        'programs': sorted(all_programs),
        'universities': sorted(all_universities),
        'levels': sorted(all_levels),
        'filtered_universities': filtered_universities,
        'selected_program': selected_program,
        'selected_university': selected_university,
        'selected_level': selected_level,
    }

    return render(request, 'general_recommendations.html', context)



 #fetching and sending messages to the backend   
@csrf_exempt
def get_bot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            user_id =  request.user.id

            # Simulate bot response
            bot_message = chatbot.get_response(user_message,user_id)

            return JsonResponse({'botMessage': bot_message})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
