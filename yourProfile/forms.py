# forms.py
from django import forms
from login.models import *
  
class AvaForm(forms.ModelForm):
  
    class Meta:
        model = Profile
        fields = ['userAva']