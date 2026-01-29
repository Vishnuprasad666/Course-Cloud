from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","email","username","password1","password2"]


class StudentSignInForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"placeholder":"Enter Your Username","class":"border border-2 my-2 rounded"}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"placeholder":"Enter Your Password","class":"border border-2 my-2 rounded"}))
