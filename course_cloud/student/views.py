from django.shortcuts import render,redirect
from django.views import View
from student.forms import *
from django.contrib import messages

# Create your views here.


class StudentCreationView(View):
    def get(self,request,*args,**kwargs):
        form=StudentCreationForm()
        return render(request,'student-registration.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form_data=StudentCreationForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"Student Sign Up Successfull")
            return redirect('student-signup')
        return render(request,'student-registration.html',{'form':form_data})
        