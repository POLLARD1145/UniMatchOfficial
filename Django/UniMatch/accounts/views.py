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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Hobby, Interest
from .forms import HobbyForm, InterestForm
from django.conf import settings
from .forms import PersonalDetailsForm, EducationForm, HobbyForm, InterestForm
from django.conf import settings
from .models import CustomUser, Hobby, Interest, Education


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

@login_required
def edit_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('details')
    else:
        form = EducationForm()
    
    # Retrieve existing education details for the current user
    educations = Education.objects.filter(user=request.user)
    
    return render(request, "user_account/edit_education.html", {'form': form, 'educations': educations})

@login_required
def edit_education_detail(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('edit_education')
    else:
        form = EducationForm(instance=education)
    
    return render(request, "user_account/edit_education.html", {'form': form})

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user)
    if request.method == 'POST':
        education.delete()
        return redirect('edit_education')
    
    return redirect('edit_education')


@login_required
def edit_hobbies(request):
    if request.method == 'POST':
        form = HobbyForm(request.POST)
        if form.is_valid():
            hobby = form.save(commit=False)
            hobby.user = request.user
            hobby.save()
            return redirect('details')
    else:
        form = HobbyForm()
    
    # Retrieve existing hobbies for the current user
    hobbies = Hobby.objects.filter(user=request.user)
    
    return render(request, "user_account/edit_hobbies.html", {'form': form, 'hobbies': hobbies})

@login_required
def edit_hobby_detail(request, hobby_id):
    hobby = get_object_or_404(Hobby, id=hobby_id, user=request.user)
    if request.method == 'POST':
        form = HobbyForm(request.POST, instance=hobby)
        if form.is_valid():
            form.save()
            return redirect('edit_hobbies')
    else:
        form = HobbyForm(instance=hobby)
    
    return render(request, "user_account/edit_hobbies.html", {'form': form})

@login_required
def delete_hobby(request, hobby_id):
    hobby = get_object_or_404(Hobby, id=hobby_id, user=request.user)
    if request.method == 'POST':
        hobby.delete()
        return redirect('edit_hobbies')
    
    return redirect('edit_hobbies')


@login_required
def edit_interests(request):
    # Get the full list of programs
    all_programs = set(extract_programs())

    # Get existing interests for the user
    existing_interests = Interest.objects.filter(user=request.user)

    # Exclude programs already in the user's interests
    existing_program_names = {interest.name for interest in existing_interests}
    available_programs = list(all_programs - existing_program_names)
    
    if request.method == 'POST':
        form = InterestForm(request.POST, programs=available_programs)
        if form.is_valid():
            # Save the selected program to a new Interest instance
            selected_program = form.cleaned_data['program']
            Interest.objects.create(user=request.user, name=selected_program)
            return redirect('edit_interests')
    else:
        form = InterestForm(programs=available_programs)

    return render(request, "user_account/edit_interests.html", {
        'form': form,
        'existing_interests': existing_interests,
    })

@login_required
def edit_interest_detail(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, user=request.user)
    all_programs = set(extract_programs())

    # Exclude current interest from the exclusion list
    existing_program_names = {i.name for i in Interest.objects.filter(user=request.user) if i.id != interest_id}
    available_programs = list(all_programs - existing_program_names)

    if request.method == 'POST':
        form = InterestForm(request.POST, programs=available_programs)
        if form.is_valid():
            # Update the name of the existing interest
            interest.name = form.cleaned_data['program']
            interest.save()
            return redirect('edit_interests')
    else:
        # Initialize the form with the current interest
        form = InterestForm(initial={'program': interest.name}, programs=available_programs)

    return render(request, "user_account/edit_interests.html", {
        'form': form,
        'existing_interests': Interest.objects.filter(user=request.user),
        'editing': True,
    })

@login_required
def delete_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, user=request.user)
    if request.method == 'POST':
        interest.delete()
        return redirect('edit_interests')
    return redirect('edit_interests')


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
