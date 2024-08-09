from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from UniMatch import settings
from .models import CustomUser, Hobby, Interest
from .forms import CustomUserCreationForm, CustomUserChangeForm,HobbyForm,InterestForm

# Import university_data from app.views
from app.views import universities_data

def extract_programs():
    """Extract a sorted list of unique programs from universities_data."""
    programs = set()
    for university in universities_data.values():
        for program in university:
            programs.add(program['name'])
    return sorted(programs)

#imports end here
# Views go here

def login(request):
    return render(request=request, template_name="user_account/login.html")

def user_details(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    hobbies = Hobby.objects.filter(user = request.user)
    interests = Interest.objects.filter(user = request.user)
    return render(request, "user_account/user_details.html",{
        'hobbies': hobbies,
        'interests' : interests
    })

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Hobby, Interest, Education
from .forms import PersonalDetailsForm, EducationForm, HobbyForm, InterestForm

def user_details(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    hobbies = Hobby.objects.filter(user=request.user)
    interests = Interest.objects.filter(user=request.user)
    education = Education.objects.filter(user=request.user)
    
    return render(request, "user_account/user_details.html", {
        'user': request.user,
        'hobbies': hobbies,
        'interests': interests,
        'education': education,
    })

# views.py
from django.shortcuts import render, redirect
from django.conf import settings
from .models import CustomUser, Hobby, Interest, Education
from .forms import PersonalDetailsForm, EducationForm, HobbyForm, InterestForm

def user_details(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    hobbies = Hobby.objects.filter(user=request.user)
    interests = Interest.objects.filter(user=request.user)
    education = Education.objects.filter(user=request.user)
    
    return render(request, "user_account/user_details.html", {
        'user': request.user,
        'hobbies': hobbies,
        'interests': interests,
        'education': education,
    })

def edit_personal_details(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    if request.method == 'POST':
        form = PersonalDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('details')
    else:
        form = PersonalDetailsForm(instance=request.user)
    
    return render(request, "user_account/edit_personal_details.html", {'form': form})

def edit_education(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('details')
    else:
        form = EducationForm()
    
    return render(request, "user_account/edit_education.html", {'form': form})

def edit_hobbies(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    if request.method == 'POST':
        form = HobbyForm(request.POST)
        if form.is_valid():
            hobby = form.save(commit=False)
            hobby.user = request.user
            hobby.save()
            return redirect('details')
    else:
        form = HobbyForm()
    
    return render(request, "user_account/edit_hobbies.html", {'form': form})


def edit_interests(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    # List of programs to be used as choices
    programs = [
        'Software Development',
        'Web Development',
        'Data Science',
        'Cyber Security',
        'Networking',
        'Cloud Computing',
        'Artificial Intelligence',
        'Internet of Things (IoT)',
        'Blockchain',
        'UX/UI Design',
        'Database Management',
        'Game Development'
    ]
    
    if request.method == 'POST':
        form = InterestForm(request.POST, programs=programs)
        if form.is_valid():
            # Get the selected program interest
            selected_program = form.cleaned_data['program']
            # Create or update interest instance
            interest, created = Interest.objects.update_or_create(
                user=request.user,
                defaults={'name': selected_program}
            )
            return redirect('details')
    else:
        # Initialize the form with the list of program choices
        form = InterestForm(programs=programs)

    # Fetch existing interests for the user
    existing_interests = Interest.objects.filter(user=request.user)

    return render(request, "user_account/edit_interests.html", {
        'form': form,
        'existing_interests': existing_interests,
    })


@login_required
def edit_details(request):
    if request.method == 'POST':
        interest_form = InterestForm(request.POST)
        hobby_form = HobbyForm(request.POST)
        if interest_form.is_valid() and hobby_form.is_valid():
            interest = interest_form.save(commit=False)
            hobby = hobby_form.save(commit=False)
            interest.user = request.user
            hobby.user = request.user
            interest.save()
            hobby.save()
            #return redirect('details')
        else:
            hobby_form = HobbyForm()
            interest_form = InterestForm()
    hobbies = Hobby.objects.filter(user = request.user)
    interests = Interest.objects.filter(user = request.user)

    return render(request, 'user_account/user_details.html',{
        'hobbies': hobbies,
        'interests': interests,
        'hobby_form' : hobby_form,
        'interest_form' : interest_form
    })


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'user_account/login.html'



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user_account/register.html'

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('details')
    template_name = 'user_account/user_details.html'

    def get_object(self):
        return self.request.user
