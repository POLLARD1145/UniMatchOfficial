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
from app.ai_logic import unirank_web as uw, recommender
from app.ai_logic.chatbot import Chatbot

# Create your views here.

def index(request):
    return render(request=request,template_name="index.html")

def chat(request):
    return render(request=request,template_name="chatbot/index.html")

# Assuming you have models for these
from accounts.models import Hobby, Interest, Education

def chat(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not logged in, render the template without context
        return render(request, template_name="chatbot/index.html")

    # Retrieve user details from the database
    hobbies = Hobby.objects.filter(user=request.user)
    interests = Interest.objects.filter(user=request.user)
    
    # Get the user's education details, checking for grade 12 points
    education = Education.objects.filter(user=request.user).first()
    if education and education.grade_twelve_points is not None:
        # Rate the academic results based on grade_twelve_points
        grade_twelve_points = education.grade_twelve_points
        # Normalize grade_twelve_points to a scale where 6 is highest and 25 is lowest
        if 6 <= grade_twelve_points <= 25:
            academic_results = (25 - grade_twelve_points) / 19 * 100  # Scale to 0 - 100
        else:
            academic_results = 50  # Default to middle if out of expected range
    else:
        academic_results = 50  # Default to average if no education record

    # Construct user profile for the recommender
    user_profile = {
        "interests": ", ".join([interest.name for interest in interests]),
        "academic_results": academic_results,
        "hobbies": ", ".join([hobby.name for hobby in hobbies])
    }

    # Get recommended programs based on user profile
    recommended_programs_df = recommender.get_user_recommended_programs(user_profile)

    # Convert DataFrame to a list of dictionaries
    recommended_programs = recommended_programs_df.to_dict(orient='records')

    # Pass recommended programs to the template
    context = {
        'recommended_programs': recommended_programs,
        'user': request.user,
        'hobbies': hobbies,
        'interests': interests,
    }

    return render(request, template_name="chatbot/index.html", context=context)

def universities(request):
    from .ai_logic import qualifications_data as qd
    institutions_data = qd.get_program_and_university()

    # Get the search query from the request
    query = request.GET.get('query', '').lower()

    if query:
        # Filter institutions and programs based on the search query
        filtered_data = {}
        for institution, programs in institutions_data.items():
            # Check if the institution name or any program name matches the query
            if query in institution.lower() or any(query in program.lower() for program in programs):
                filtered_data[institution] = [program for program in programs if query in program.lower()]

        institutions_data = filtered_data
    return render(request, 'universities.html', {'institutions_data': institutions_data})
    

# Enhanced sample data with levels and descriptions
# Path to your JSON file
file_path = 'app/ai_logic/jsonfiles/zambia_public_university.json'

def load_universities_data():
    """ Load universities data from the JSON file. """
    with open(file_path, 'r') as json_file:
        return json.load(json_file)
    
universities_data = load_universities_data()

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
            # Initialize the chatbot
            chatbot = Chatbot()

            # Get the user's message
            data = json.loads(request.body)
            user_message = data.get('message', '')
            user_id = request.user.id

            # Get bot response
            bot_response = chatbot.get_response(user_message, user_id)

            # Check if feedback is needed based on accuracy
            feedback_requested = False
            if chatbot.low_accuracy:
                # Request feedback
                feedback_requested = True

            return JsonResponse({'botMessage': bot_response, 'feedbackRequested': feedback_requested})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)