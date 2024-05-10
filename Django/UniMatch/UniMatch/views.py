from django.shortcuts import render

# Views go here

def index(request):
    return render(request=request,template_name="index.html")