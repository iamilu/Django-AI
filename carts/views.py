from django.shortcuts import render

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


