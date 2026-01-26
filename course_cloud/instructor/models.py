from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    ROLE_OPTIONS=[
        ("Instructor","Instructor"),
        ("Student","Student")
    ]

    role=models.CharField(max_length=20, choices=ROLE_OPTIONS, default="Student")


class InstructorProfile(models.Model):
    owner=models.OneToOneField(User, on_delete=models.CASCADE, related_name="instructor_profile")
    expertise=models.CharField(max_length=100, null=True)
    picture=models.ImageField(upload_to="Instructor_profile_picture", default="Instructor_profile_picture/default.png")
    about=models.CharField(max_length=500, null=True)

from django.db.models.signals import post_save

def create_instructor_profile(sender,instance,created,**kwargs):
    if created and instance.role=="Instructor":
        InstructorProfile.objects.create(owner=instance)

post_save.connect(create_instructor_profile,User)

class Category(models.Model):
    name=models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=7)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="course")
    is_free=models.BooleanField(default=False)
    picture=models.ImageField(upload_to="course_images",null=True,default="course_images/default_course.png")
    thumbnail=models.TextField()
    category_object=models.ManyToManyField(Category)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class Module(models.Model):
    title=models.CharField(max_length=200)
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="module")
    order=models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    title=models.CharField(max_length=200)
    module_object=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lesson")
    video=models.TextField()
    order=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.module_object.title} + {self.title}"