from django.contrib import admin
from student.models import Order,Cart,Wishlist
# Register your models here.

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Wishlist)