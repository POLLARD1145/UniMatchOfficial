# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, Hobby, Interest, Education


# Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

# Custom user change form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')

# Custom authentication form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'autocomplete': 'username',
            'aria-required': 'true',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'autocomplete': 'password',
            'aria-required': 'true',
            'placeholder': 'Password',
        })
    )

# Form for personal details
class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

# Form for education
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'field', 'institution', 'year', 'grade_twelve_points']

# Form for hobbies
class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ('name',)

# Form for interests
class InterestForm(forms.ModelForm):
    # Program choice field for selecting interest
    program = forms.ChoiceField(required=False, label="Select Program Interest", choices=[])

    class Meta:
        model = Interest
        fields = ('program',)

    def __init__(self, *args, **kwargs):
        programs = kwargs.pop('programs', [])
        super().__init__(*args, **kwargs)
        # Setting the choices for the program field
        self.fields['program'].choices = [(program, program) for program in programs]
        # Update widget attributes for styling
        self.fields['program'].widget.attrs.update({'class': 'form-control'})