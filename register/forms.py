from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from core.models import Profile

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
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, medical_conditions=self.cleaned_data.get('medical_conditions'))
        return user

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
        if 'password' in self.fields:
            del self.fields['password']  # Remove password field
        try:
            self.fields['medical_conditions'].initial = self.instance.profile.medical_conditions
        except Profile.DoesNotExist:
            self.fields['medical_conditions'].initial = ""

    def save(self, commit=True):
        user = super(ProfileUpdateForm, self).save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.medical_conditions = self.cleaned_data.get('medical_conditions')
            profile.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False  # Make old password optional initially
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False  # Make new password1 optional initially
    )
    new_password2 = forms.CharField(
        label="Please repeat new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False  # Make new password2 optional initially
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password or new_password1 or new_password2:
            if not old_password:
                self.add_error('old_password', 'This field is required if you want to change your password.')
            if not new_password1:
                self.add_error('new_password1', 'This field is required if you want to change your password.')
            if not new_password2:
                self.add_error('new_password2', 'This field is required if you want to change your password.')
            if new_password1 and new_password2 and new_password1 != new_password2:
                self.add_error('new_password2', 'The two password fields didn’t match.')

        return cleaned_data