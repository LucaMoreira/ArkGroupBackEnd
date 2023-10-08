from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
import json
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import logout
from .models import User, PasswordToken
import string
import random
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY

# Expire after 24h
TOKEN_EXPIRE = 86400

# If token is expired then it will be removed
def token_expire_handler(token) -> bool:
    time_elapsed = timezone.now() - token.created
    left_time    = timedelta(seconds=TOKEN_EXPIRE) - time_elapsed
    is_expired   = left_time < timedelta(seconds=0)
    if is_expired:
        token.delete()
    return is_expired

def is_subscription_active(id:str) -> bool:
    try:
        subscription = stripe.Subscription.retrieve(id)
        status       = subscription['status']
    
    except Exception as e:
        return False
    
    if status == 'active':
        return True
    else:
        return False

def create_password_token(user, size=40, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    while True:
        token = ''.join(random.choice(chars) for _ in range(size))
        
        try:
            PasswordToken.objects.get(id=token)
        except:
            PasswordToken.objects.create(id=token, user=user)
            return token

def get_auth(request, username, token) -> tuple[dict, str]:
    """
    
    Check user authorization.

    Args:
        request  (React Request): api request
        username (str): session's user username
        token    (str): session's user token

    Returns:
        dict: user's auth level
        str: operation message
    """
    
    #* Check if arg types are correct
    if type(username) != str: return False, "Username must be string"
    if type(token)    != str: return False, "Token must be string"
    
    #* Check if token exists
    try:
        user_token = Token.objects.get(key=token)
    except Exception as e:
        return {'auth': 'Visitor'}, "Token does not exist"
    
    #* Check if user exists
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        return {'auth': 'Visitor'}, "User does not exist"
    
    #* Check if user match token
    if username != str(user_token.user):
        return {'auth': 'Visitor'}, 'User and token does not match'
    
    #* Check if token is expired
    is_expired         = token_expire_handler(user_token)
    
    if is_expired:
        logout(request)
        return {'auth': 'Visitor'}, 'Token Expired'
    
    subscription_id = user.sub_id
    
    if user.is_staff:
        return {'auth': 'Client'}, 'User is staff'
    
    if type(subscription_id) == str and subscription_id != '':
        if not is_subscription_active(user.sub_id):
            user.status = False
            user.save()
            return {'auth': 'User'}, 'User subscription inactive'
        else:
            return {'auth': 'Client'}, 'User is logged and has active subscription'
    else:
        return {'auth': 'User'}, 'User subscription inactive'