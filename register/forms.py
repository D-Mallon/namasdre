from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    medical_conditions = forms.CharField(
        max_length=300, 
        label='Medical or Physical Conditions (please let us know any relevant details)',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'medical-conditions-input'}),
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "medical_conditions"]

class ProfileUpdateForm(UserChangeForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    medical_conditions = forms.CharField(
        max_length=300, 
        label='Medical or Physical Conditions (please let us know any relevant details)',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'medical-conditions-input'}),
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "medical_conditions"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()  # Hide the password field - prefer to use password change form below for styling reasons

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)