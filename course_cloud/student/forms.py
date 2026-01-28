from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","email","username","password1","password2"]


class StudentSignInForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput())
    password=forms.CharField(max_length=100,widget=forms.PasswordInput())
