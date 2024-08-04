from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name='home'),
    path("login/", views.CustomLoginView.as_view(), name='login'),
    path("details/", views.user_details, name='details'),
    path("edit_user_details/", views.edit_details, name='edit_details'),
    path('account/edit-personal-details/', views.edit_personal_details, name='edit_personal_details'),
    path('account/edit-education/', views.edit_education, name='edit_education'),
    path('account/edit-hobbies/', views.edit_hobbies, name='edit_hobbies'),
    path('account/edit-interests/', views.edit_interests, name='edit_interests'),
]
