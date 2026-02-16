from student.models import Cart,Order

def cartCount(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user_object=request.user).count()
        return {"cartCount":count}
    return {"cartCount":0}

def courseCount(request):
    if request.user.is_authenticated:
        ordercount=Order.objects.filter(student=request.user,is_paid=True).count()
        return {"courseCount":ordercount}
    return {"courseCount":0}