from django.urls import path
from student.views import *


urlpatterns=[
    path('signup',StudentCreationView.as_view(),name='student-signup'),
    path('student-home',HomeView.as_view(),name='home'),
    path('course-details/<int:pk>',CourseDetailsView.as_view(),name='course')
]