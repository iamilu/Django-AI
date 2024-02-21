'''
write a register view using Registartion Form and if the form input is valid then
add user in Account Model also add the user in the User Profile model with a dummy profile picture
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, UserProfile
from orders.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm
from .utils import send_otp
import pyotp
import datetime

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            user = Account.objects.create_user(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                username = form.cleaned_data['email'].split('@')[0],
                password = form.cleaned_data['password'],
            )


            user.phone = form.cleaned_data['phone']
            user.is_active = True
            user.save()

            user_profile = UserProfile()
            user_profile.user = user
            user_profile.profile_pic = 'default/default_profile_pic.png'
            user_profile.save()

            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

'''
write a login view to authenticate the user and if the user is authenticated then redirect to the otp view to send otp
and if the user is not authenticated then display an error message to the user and redirect to the login view
'''

def login(request):

    if 'email' in request.session:
        del request.session['email']

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            send_otp(request)
            request.session['email'] = email
            return redirect('otp')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    return render(request, 'accounts/login.html')

'''
write a otp view to verify if the otp is valid along with otp secret key and expiration time then login to the user and redirect to the dashboard view
and if the otp is invalid then display an error message to the user and redirect to the otp view
'''

def otp(request):

    if request.method == 'POST':
        otp = request.POST['otp']
        email = request.session['email']
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_until']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key)
                
                if totp.verify(otp):
                    user = get_object_or_404(Account, email=email)
                    auth.login(request, user)
                    messages.success(request, 'Login successful')
                    
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_until']
                    
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid OTP.')
                    return redirect('otp')
            
            else:
                messages.error(request, 'OTP has expired')
                return redirect('otp')

        else:
            messages.error(request, 'OOPS, something went wrong!')
            return redirect('otp')

    return render(request, 'accounts/otp.html')

'''
write a logout view to logout the user if the user is logged in, send a message to the user and then redirect to the login view
'''
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')

'''
write a forgotPassword view to check the if the user is registered or not, if the user is exist or not and if the user is exist, then send to the resetPassword view
'''
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        try:
            user = Account.objects.get(email__exact=email)
        except Account.DoesNotExist:
            user = None
        
        if user:
            request.session['email'] = email
            return redirect('resetPassword')
        else:
            messages.error(request, 'User does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

'''
write a resetPassword view to check if the new password and confirm password are same, if the new password and confirm password are same, then update the password and redict to the login page
'''
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.session['email']

        if password == confirm_password:
            
            try:
                user = Account.objects.get(email__exact=email)
            except Account.DoesNotExist:
                user = None

            if user:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('login')
            else:
                messages.error(request, 'User does not exist')
                return redirect('forgotPassword')
        else:
            messages.error(request, 'Password and confirm password are not same')
            return redirect('resetPassword')
    return render(request, 'accounts/resetPassword.html')

'''
write a dashboard view to display the user's profile and order count, if the user is logged in
'''
@login_required(login_url='login')
def dashboard(request):

    if 'email' in request.session:
        del request.session['email']

    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    orders_count = Order.objects.filter(user=user, is_ordered=True).order_by('-created_at').count()
    context = {
        'user_profile': user_profile,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)

'''
write a my_orders view to display the list of orders of the user, if the user is logged in
'''
@login_required(login_url='login')
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

'''
write an edit_profile view to edit the user information as per UserForm and UserProfileForm, if the user is logged in
'''
@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid form data')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'user_profile': user_profile,
        }
        return render(request, 'accounts/edit_profile.html', context)

'''
write a change_password view to change the password of the user, if the user is logged in
'''
@login_required(login_url='login')
def change_password(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('login')
            else:
                messages.error(request, 'New password and confirm password are not same')
                return redirect('change_password')
        else:
            messages.error(request, 'Invalid current password')
            return redirect('change_password')
        
    context = {
        'user_profile': user_profile,
    }

    return render(request, 'accounts/change_password.html', context)

'''
write a order_detail view to display the details of the order, if the user is logged in
'''
@login_required(login_url='login')
def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order_detail = OrderProduct.objects.filter(order=order, is_ordered=True)

    context = {
        'order': order,
        'order_detail': order_detail,
    }

    return render(request, 'accounts/order_detail.html', context)