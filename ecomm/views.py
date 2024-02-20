from django.shortcuts import render
from carts.models import Cart, CartItem
from store.models import Product

# Create your views here.
'''
write a view to get the list of products from Product model and pass it to the index.html template
'''
def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'index.html', context)