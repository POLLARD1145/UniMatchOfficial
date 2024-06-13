from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name='home'),
    path("login/", views.CustomLoginView.as_view(), name='login'),
    path("details/", views.user_details, name='details'),
]
