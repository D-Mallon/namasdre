from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    medical_conditions = forms.CharField(
    max_length=300, 
    label='Medical or Physical Conditions (please let us know any relevant details)',
    widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'medical-conditions-input'})
)


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "medical_conditions"]
