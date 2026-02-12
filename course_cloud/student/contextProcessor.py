from student.models import Cart

def cartCount(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user_object=request.user).count()
        return {"cartCount":count}
    return {"cartCount":0}