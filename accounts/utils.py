'''
write a function send otp to generate otp with 1 minute expiration time using pyotp module and store otp secret key and expiration until in the session
'''
import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    
    # Generate OTP
    otp = totp.now()

    # Generate OTP secret key
    otp_secret_key = totp.secret
    
    # Send OTP to email
    # ...
    
    # Store OTP secret key and expiration time in session
    request.session['otp_secret_key'] = otp_secret_key

    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_until'] = str(valid_date)
    
    print(f"Your OTP is: {otp}")