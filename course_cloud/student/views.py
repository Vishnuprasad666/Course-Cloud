from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.views import View
from student.forms import *
from django.contrib import messages
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView
from django.contrib.auth import authenticate,login,logout
from instructor.models import *
from student.models import *

# Create your views here.


# class StudentCreationView(View):
#     template_name="student-registration.html"
#     form_class=StudentCreationForm
#     success_url='signin'
#     def get(self,request,*args,**kwargs):
#         form=self.form_class
#         return render(request,self.template_name,{'form':form})
#     def post(self,request,*args,**kwargs):
#         form_data=self.form_class(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             messages.success(request,"Student Sign Up Successfull")
#             return redirect(self.success_url)
#         return render(request,self.template_name,{'form':form_data})
        
# class StudentSignInView(View):
#     def get(self,request):
#         return render(request,'student_login.html')


class StudentCreationView(CreateView):
    template_name="student-registration.html"
    form_class=StudentCreationForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"User Signup Successfull")
        return super().form_valid(form)

class StudentSignInView(FormView):
    template_name='student_login.html'
    form_class=StudentSignInForm
    def post(self,request,*args,**kwargs):
        form_data=self.form_class(data=request.POST)
        if form_data.is_valid():
            username=form_data.cleaned_data.get("username")
            password=form_data.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                if user.role=="Student":
                    messages.success(request,"successfully signed in")
                    return redirect('home')
                elif user.role=="Instructor":
                    return redirect(reverse("admin:index"))
            else:
                messages.warning(request,"Invalid Username or Password")
                return redirect('signin')
        messages.error(request,"Invalid Input Recieved!!")
        return render(request,"student_login.html",{"form":form_data})

class HomeView(ListView):
    template_name="home.html"
    queryset=Course.objects.all()
    context_object_name="data"

class CourseDetailsView(DetailView):
    template_name='courseDetails.html'
    queryset=Course.objects.all()
    # context_object_name
    # pk_url_kwarg

class AddtoCartView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('pk')
        course=Course.objects.get(id=cid)
        user=request.user
        print(course)
        print(user)
        try:
            Cart.objects.get_or_create(course_object=course,user_object=user)
            return redirect('home')
        except:
            print("already added to cart")
            messages.info(request,"Course already added to cart!")
            return redirect('course',pk=cid)
