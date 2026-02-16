from django.urls import path
from instructor.views import *


urlpatterns = [
    path('instructor-signup',InstructorSignUpView.as_view(),name='instructor')
]