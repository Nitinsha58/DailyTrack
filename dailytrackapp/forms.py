from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class DailyTrackForm(forms.ModelForm):
    
    class Meta:
        model = DailyTrack
        fields = ['income', 'expense', 'note']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']