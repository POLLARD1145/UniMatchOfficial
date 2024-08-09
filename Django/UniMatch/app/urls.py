from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name='home'),
    path("chat/", views.chat, name='chatbot'),
    path("universities/", views.universities, name='chatbot'),
    path("get_bot_response/", views.get_bot_response, name='chatbot'),
    path("general-recommendations/", views.general_recommendations, name='general_recommendations'),
    
]
