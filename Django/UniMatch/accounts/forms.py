# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'aria-required': 'true',
            })
        self.fields['email'].widget.attrs.update({'placeholder': 'name@example.com'})
        self.fields['username'].widget.attrs.update({'autocomplete': 'username', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'password', 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'confirm password', 'autocomplete': 'new-password'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, 
                               widget=forms.TextInput(attrs={
                                   'autofocus': True,
                                   'class': 'form-control',
                                    'autocomplete': 'username',
                                    'aria-required': 'true',
                                    'placeholder': 'Username',
                                    'for':'username'
                                }))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={
                                   'autofocus': True,
                                   'class': 'form-control',
                                    'autocomplete': 'password',
                                    'aria-required': 'true',
                                    'placeholder': 'Password',
                                    'for':'password'
                                }))
