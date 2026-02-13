from django.urls import path
from student.views import *


urlpatterns=[
    path('signup',StudentCreationView.as_view(),name='student-signup'),
    path('student-home',HomeView.as_view(),name='home'),
    path('course-details/<int:pk>',CourseDetailsView.as_view(),name='course'),
    path('addtocart/<int:pk>',AddtoCartView.as_view(),name='addtocart'),
    path('cartsummery',CartSummeryView.as_view(),name='cart-summery'),
    path('removefromcart/<int:pk>',RemoveFromCartView.as_view(),name='remove-cart'),
    path('order',PlaceOrderView.as_view(),name='order'),
    path('my-courses',MyCourseView.as_view(),name='mycourses'),
    path('lesson/<int:pk>',ViewLessonView.as_view(),name='lesson')
    
]