'''
write a place_order view to place order using OrderForm, save order details in Order Model and if order is placed then redirect to payment page
'''
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from carts.models import Cart, CartItem
from accounts.models import UserProfile
from store.models import Product, Variation

import datetime
import json

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.http import JsonResponse

def place_order(request):
    if request.user.is_authenticated:

        '''
        check if there is any item in the CartItem model, if there is no item then redirect to store page
        '''
        cart_items = CartItem.objects.filter(user=request.user)
        if cart_items.count() <= 0:
            messages.warning(request, 'No item in the cart')
            return redirect('store')
        else:
            total = 0
            quantity
            for item in cart_items:
                total += item.product.price * item.quantity
                quantity += item
            
            tax = 0.05 * total
            grand_total = total + tax

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                '''
                store data in Order Model
                '''
                order = Order()
                order.user = request.user
                order.first_name = form.cleaned_data['first_name']
                order.last_name = form.cleaned_data['last_name']
                order.phone = form.cleaned_data['phone']
                order.email = form.cleaned_data['email']
                order.address_line_1 = form.cleaned_data['address_line_1']
                order.address_line_2 = form.cleaned_data['address_line_2']
                order.city = form.cleaned_data['city']
                order.pincode = form.cleaned_data['pincode']
                order.order_note = form.cleaned_data.get('order_note')
                order.order_total = grand_total
                order.tax = tax
                order.ip = request.META.get('REMOTE_ADDR')
                order.save()

                # generate order number and store in Order Model
                current_date = str(datetime.date.today()).replace('-','')
                order_number = current_date + str(order.id)
                order.order_number = order_number
                order.save()

                '''
                get user profile details from UserProfile Model and update and save user details
                '''
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.address_line_1 = form.cleaned_data['address_line_1']
                user_profile.address_line_2 = form.cleaned_data['address_line_2']
                user_profile.city = form.cleaned_data['city']
                user_profile.pincode = form.cleaned_data['pincode']
                user_profile.state = form.cleaned_data['state']
                user_profile.country = form.cleaned_data['country']
                user_profile.save()

                '''
                get the order details and pass it to payments.html as context
                '''
                order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total
                }
                return render(request, 'orders/payments.html', context)
            else:
                return ('checkout')
        else:
            try:
                order_queryset = Order.objects.filter(user=request.user, is_ordered=False)
                order = list(order_queryset)[-1]
                context = {
                        'order': order,
                        'cart_items': cart_items,
                        'total': total,
                        'tax': tax,
                        'grand_total': grand_total
                    }
                return render(request, 'orders/payments.html', context)
            except:
                return render(request, 'orders/payments.html')
    else:
        return redirect('login')

'''
write a payments view to get paymentl details from javascript fetch API and store payment details in Payment Model
'''
def payments(request):
    body = json.loads(request.body)
    print(body)

    # store payment details in payment model
    payment = Payment(
        user = request.user,
        payment_id = body['payment_id'],
        payment_method = body['payment_method'],
        amount_paid = body['amount_paid'],
        status = body['status'],
    )
    payment.save()

    '''
    get the order details and update the order payment details, staus and is_ordered fields
    '''
    order_number = body['order_number']
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    order.payment = payment
    order.status = 'Completed'
    order.is_ordered = True
    order.save()

    '''
    move cart items to OrderProduct Model
    '''
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product = item.product
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.is_ordered = True
        order_product.save()
        '''
        store product variation details in OrderProduct Model
        '''
        cart_item = CartItem.objects.get(id=item.id)
        # get variation of each item
        product_variation = cart_item.variation.all()
        # order_product id will get generated as you have saved the object earlier
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variation.set(product_variation)
        order_product.save()

        '''
        reduce the product stock by the already ordered item quntity
        '''
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
    '''
    clear the cart once order is placed
    '''
    Cart.objects.filter(user=request.user).delete()

    '''
    send order complete email to the user
    '''
    mail_subject = 'Thank you for your order ' + order.order_number
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()

    '''
    send order number, payment id and status back to java script in payments.html
    '''
    data = {
        'order_number': order.order_number,
        'payment_id': payment.payment_id,
        'status': payment.status,
    }
    return JsonResponse(data)

'''
write a order_complete view to grab order details from Order, Payment and OrderProduct Model and render order_complete.html page
'''
def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    try:

        order = Order.objects.get(order_number=order_number, is_ordered=True)
        payment = Payment.objects.get(payment_id=payment_id)
        order_products = OrderProduct.objects.filter(order=order, payment=payment)
        
        '''
        calculate toal, tax and grand total
        '''
        total = 0
        quantity = 0
        for item in order_products:
            total += item.product_price * item.quantity
            quantity += item.quantity
        
        tax = 0.05 * total
        grand_total = total + tax

        context = {
            'order': order,
            'payment': payment,
            'order_products': order_products,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        }
    except (Order.DoesNotExist, Payment.DoesNotExist, OrderProduct.DoesNotExist):
        return redirect('store')

    return render(request, 'orders/order_complete.html', context)