from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm

class InstructorForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"placeholder":"Enter First Name","class":"form-control"}),
            "email":forms.EmailInput(attrs={"placeholder":"Enter Email ID","class":"form-control"}),
            "username":forms.TextInput(attrs={"placeholder":"Enter Userame","class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"placeholder":"Enter Password","class":"form-control"}),
            "password2":forms.PasswordInput(attrs={"placeholder":"Re-Enter Password","class":"form-control"})
        }
        
    def save(self, commit = True):
        user=super().save(commit = False)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.role="Instructor"
        if commit:
            user.save()
        return user