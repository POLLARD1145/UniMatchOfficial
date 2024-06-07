from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name='home'),
    path("chat/", views.chat, name='chatbot'),
    path("universities/", views.universities, name='chatbot'),
]
