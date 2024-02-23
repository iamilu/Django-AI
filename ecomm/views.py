from django.shortcuts import render
from carts.models import Cart, CartItem
from store.models import Product, ReviewRating
from carts.views import get_cart_id

# Create your views here.
'''
write an index view to check if the session id present in Cart Model, and if not present then add it in Cart Model
also grab the product list from Product Model and rating from Review Rating Model and pass it in context to index.html page
'''
def index(request):
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=get_cart_id(request))
        cart.save()
    
    products = Product.objects.filter(is_available=True)

    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)
