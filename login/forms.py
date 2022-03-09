from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username', max_length=20)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
