from .models import Cart, CartItem
from .views import get_cart_id

'''
write a function to check if the user is logged in and if the user is logged in, then returns the total number of items in the cart for that user
and if user is not logged in, then returns the total number of items in the cart for that session
'''
def carts_count(request):
    total_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=get_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                total_count += cart_item.quantity
        except Cart.DoesNotExist:
            total_count = 0
    return dict(total_count=total_count)



