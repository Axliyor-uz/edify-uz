from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICE)

    class Meta:
        model = User
        fields = ['username', 'role','password1', 'password2']