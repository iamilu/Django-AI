from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required

# Create your views here.
'''
write a function to get the session id, then check if it is valid for the current session and return it
and if it is not valid then create a new session id and return it
'''
def get_cart_id(request):
    session_id = request.session.session_key
    if session_id is None:
        session_id = request.session.create()
    return session_id

'''
write a view cart to get the cart items, total, tax, grand total, qunatity using Cart Item Model
using the user detail when the user is authenticated and when the user is not authenticated by using the session id
'''

def cart(request):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except CartItem.DoesNotExist:
        pass
    
    total = 0
    quantity = 0
    for item in cart_items:
        total += item.product.price * item.quantity
        quantity += item.quantity
    
    tax = round(0.05 * total,2)
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'quantity': quantity,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)

'''
write a add_cart view to add the product to the CartItem Model and also grouping the cart item based on Product Variation
'''
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    '''
    write code to get product variation and store it in product_variation list and then check if the product_variation list is empty or not
    '''
    product_variation = []
    if request.method == 'POST':
        for key in request.POST:
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, product=product)
        
        if cart_items.exists():
            existing_variation_list = []
            existing_cart_item_id_list = []
            for cart_item in cart_items:
                existing_variation = cart_item.variation.all()
                existing_variation_list.append(list(existing_variation))
                existing_cart_item_id_list.append(cart_item.id)

            # if current product variation present, then increment the cart item by 1
            if product_variation in existing_variation_list:
                existing_variation_index = existing_variation_list.index(product_variation)
                existing_cart_item_id = existing_cart_item_id_list[existing_variation_index]
                cart_item = CartItem.objects.get(id=existing_cart_item_id)
                cart_item.quantity += 1
                cart_item.save()
            
            # if current product variation is not present, then add new cart item
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    user=request.user,
                    quantity=1
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                cart_item.save()

        # if cart item is not present, then add new cart item
        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=request.user,
                quantity=1
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
    
    else:
        try:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = get_cart_id(request)
            )   
        cart.save()

        cart_items = CartItem.objects.filter(cart=cart, product=product)

        if cart_items.exists():
            existing_variation_list = []
            existing_cart_item_id_list = []
            for cart_item in cart_items:
                existing_variation = cart_item.variation.all()
                existing_variation_list.append(list(existing_variation))
                existing_cart_item_id_list.append(cart_item.id)

            # if current product variation present, then increment the cart item by 1
            if product_variation in existing_variation_list:
                existing_variation_index = existing_variation_list.index(product_variation)
                existing_cart_item_id = existing_cart_item_id_list[existing_variation_index]
                cart_item = CartItem.objects.get(id=existing_cart_item_id)
                cart_item.quantity += 1
                cart_item.save()

            # if current product variation is not present, then add new cart item
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    cart = cart,
                    quantity = 1
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                cart_item.save()

        # if cart item is not present, then add new cart item
        else:
            cart_item = CartItem.objects.create(
                product = product,
                cart = cart,
                quantity = 1
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()

    return redirect('cart')

'''
write a remove_cart view to remove a signle cart item from the CartItem model
'''
def remove_cart(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

'''
write a remove_cart_item view to remove a whole cart item from the CartItem model
'''
def remove_cart_item(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
        
        cart_item.delete()
    except:
        pass
    return redirect('cart')

'''
write a checkout view to check out the cart items and redirect to the checkout page only if the user is logged in
'''
@login_required(login_url='login')
def checkout(request):

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except CartItem.DoesNotExist:
        cart_items = []
    
    total = 0
    quantity = 0
    for item in cart_items:
        total += item.product.price * item.quantity
        quantity += item.quantity
    
    tax = round(0.05 * total,2)
    grand_total = total + tax
    
    context = {
        'cart_items': cart_items,
        'quantity': quantity,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)