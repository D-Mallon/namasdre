from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    medical_conditions = forms.CharField(max_length=300)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "medical_conditions"]