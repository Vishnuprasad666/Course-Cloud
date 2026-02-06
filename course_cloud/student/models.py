from django.db import models
from instructor.models import User,Course
# Create your models here.


class Cart(models.Model):
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="cart_course")
    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart_course_user")
    added_at=models.DateTimeField(auto_now_add=True)