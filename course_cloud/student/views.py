from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.views import View
from student.forms import *
from django.contrib import messages
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView
from django.contrib.auth import authenticate,login,logout
from instructor.models import *
from student.models import *
import razorpay

RAZR_KEY_ID=""
RAZR_SECRET_KEy=""

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

# class HomeView(ListView):
#     template_name="home.html"
#     queryset=Course.objects.all()
#     context_object_name="data"
    
    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     qs=Order.objects.filter(student=self.request.user,is_paid=True)
    #     context["purchased_orders"]=qs
    #     print(context)
    #     return context
    
class HomeView(View):
    def get(self,request):
        allcourses_qs=Course.objects.all()
        purchases=Order.objects.filter(student=request.user, is_paid=True).values_list("course_object", flat=True)
        print(purchases)
        return render(request,"home.html",{"data":allcourses_qs,"Purchased_courses":purchases})

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
        

class CartSummeryView(View):
    def get(self,request,*args,**kwargs):
        qs=Cart.objects.filter(user_object=request.user)
        cart_total=0
        for i in qs:
            cart_total+=i.course_object.price
        return render(request,"cartsummery.html",{"data":qs,"cart_total":cart_total})
    

class RemoveFromCartView(View):
    def get(self,request,**kwargs):
        cart_id=kwargs.get('pk')
        Cart.objects.get(id=cart_id).delete()
        return redirect('cart-summery')

class PlaceOrderView(View):
    def get(self,request):
        qs=Cart.objects.filter(user_object=request.user)
        student=request.user
        cart_total=0
        for i in qs:
            cart_total+=i.course_object.price
        order=Order.objects.create(student=student,total=cart_total)
        for i in qs:
            order.course_object.add(i.course_object)
        qs.delete()
        if cart_total>0:
            #authenticate
            client=razorpay.Client(auth=(RAZR_KEY_ID,RAZR_SECRET_KEy))
            #payment-order creation
            data={ "amount":int(cart_total), "currency":"INR", "recipt":"order_recipt_11" }
            payment=client.order.create(data=data)
            print(payment,"++++++++")
            order.razr_pay_order_id.get('id')
            order.save()
            context={
                "razr_key_id":RAZR_KEY_ID,
                "amount":int(cart_total),
                "razr_pay_id":payment.get('id')
            }
            return render(request,"payment.html",{"data":context})
        return redirect('home')
    

class MyCourseView(View):
    def get(self,request):
        qs=Order.objects.filter(student=request.user,is_paid=True)
        return render(request,"my-courses.html",{"courses":qs })

class ViewLessonView(View):
    def get(self,request,**kwargs):
        course=Course.objects.get(id=kwargs.get('pk'))
        query_params=request.GET # {"module":1,"lesson":2}
        module_id=query_params.get('module') if "module" in query_params else Module.objects.filter(course_object=course).first().id
        module_object=Module.objects.get(id=module_id, course_object=course)
        lesson_id=query_params.get('lesson') if "lesson" in query_params else Lesson.objects.filter(module_object=module_object).first().id
        lesson=Lesson.objects.get(id=lesson_id, module_object=module_object)
        print(module_id,'********')
        print(lesson_id,'********')
        return render(request,"viewlesson.html",{"course":course ,"lesson":lesson}) 