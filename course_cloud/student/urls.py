from django.urls import path
from student.views import *


urlpatterns=[
    path('signup',StudentCreationView.as_view(),name='student-signup'),
    path('signin',StudentSignInView.as_view(),name='signin'),
    path('student-home',HomeView.as_view(),name='home')
]