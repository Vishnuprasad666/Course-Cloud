from django.urls import path
from student.views import *


urlpatterns=[
    path('signup',StudentCreationView.as_view(),name='student-signup')
]