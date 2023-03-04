from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email']

class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['photo_profile']

class UploadUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
