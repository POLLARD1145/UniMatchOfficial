from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Views go here

def login(request):
    return render(request=request, template_name="user_account/login.html")

def user_details(request):
    return render(request=request, template_name="user_account/user_details.html")

# accounts/views.py
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

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
    success_url = reverse_lazy('profile')
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user
