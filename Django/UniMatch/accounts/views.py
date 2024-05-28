from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Views go here

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user_account/register.html', {'form': form})

def login(request):
    return render(request=request, template_name="user_account/login.html")