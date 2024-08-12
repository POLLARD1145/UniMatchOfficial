from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name='home'),
    path("login/", views.CustomLoginView.as_view(), name='login'),
    path("details/", views.user_details, name='details'),
    path("edit_user_details/", views.edit_details, name='edit_details'),
    path('account/edit-personal-details/', views.edit_personal_details, name='edit_personal_details'),
    path('account/edit-education/', views.edit_education, name='edit_education'),
    path('edit_education_detail/<int:education_id>/', views.edit_education_detail, name='edit_education_detail'),
    path('delete_education/<int:education_id>/', views.delete_education, name='delete_education'),
    path('account/edit-hobbies/', views.edit_hobbies, name='edit_hobbies'),
    path('edit_hobby/<int:hobby_id>/', views.edit_hobby_detail, name='edit_hobby_detail'),
    path('delete_hobby/<int:hobby_id>/', views.delete_hobby, name='delete_hobby'),
    path('account/edit-interests/', views.edit_interests, name='edit_interests'),
    path('edit_interest/<int:interest_id>/', views.edit_interest_detail, name='edit_interest_detail'),
    path('delete_interest/<int:interest_id>/', views.delete_interest, name='delete_interest'),
]
