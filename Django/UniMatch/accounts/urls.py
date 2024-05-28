from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='home'),
    path("login/", views.login, name='login'),
]
