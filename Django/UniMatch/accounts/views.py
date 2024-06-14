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
