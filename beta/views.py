import json
from datetime import timedelta
import stripe

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .decorators import check_auth
from .forms import NewUserForm
from .utils import get_auth, create_password_token
from .models import User, PasswordToken
from django.core.mail import send_mail

# Create your views here.
TOKEN_EXPIRE = 86400
HEADERS      = {
    "Access-Control-Allow-Origin": settings.FRONTEND_URL,
    "Access-Control-Allow-Methods": "POST, PUT, PATCH, GET, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization"
    }
SUCCESS      = status.HTTP_200_OK
ERROR        = status.HTTP_400_BAD_REQUEST

stripe.api_key = settings.STRIPE_PRIVATE_KEY



#* USER VIEWS START *#

@api_view(["POST"])
def login_user(request):
    username = request.data['username']
    password = request.data['password']

    try:
        account = User.objects.get(username=username)
    except Exception as e:
        return Response("incorrect username", status=status.HTTP_401_UNAUTHORIZED, headers=HEADERS)

    user = authenticate(username=username, password=password)

    if user == None:
        return Response("incorrect password", status=status.HTTP_401_UNAUTHORIZED, headers=HEADERS)

    try:
        token, _   = Token.objects.get_or_create(user=user)
        user_token = token.key
    except BaseException as e:
        return Response(f"could not create token {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        login(request, account)
        return Response({"token": user_token}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin": settings.FRONTEND_URL})
    except Exception as e:
        return Response("account doesnt exist", status=status.HTTP_401_UNAUTHORIZED, headers=HEADERS)


@api_view(["POST"])
def logout_user(request):
    try:
        username   = request.data['user']
        token      = request.data['token']
        
        auth , msg = get_auth(request, username, token)
        
        if auth['auth'] != 'Visitor':
            key   = request.POST.get('token')
            token = Token.objects.get(key=key)
            token.delete()
            logout(request)
            return Response("User Logged out", status=SUCCESS, headers=HEADERS)
        
    except:
        return Response(status=ERROR, headers=HEADERS)


@api_view(["POST"])
def create_user(request):
    try:
        user = User(username=request.data['username'], email=request.data['email'])
        user.set_password(request.data['password1'])
        user.save()
        token      = Token.objects.create(user=user)
        data       = {
            'token': token.key
        }
        login(request, user)
        return Response(data, status=SUCCESS, headers=HEADERS)
    except Exception as e:
        print(e)
        return Response(status=ERROR, headers=HEADERS)


@api_view(["POST"])
def delete_user(request):
    username   = request.data['user']
    token      = request.data['token']

    auth , msg = get_auth(request, username, token)
    
    if auth['auth'] != 'Visitor':
        user = User.objects.get(username=username)
        Token.objects.get(key=token).delete()
        logout(request)
        #todo: if subscription not null
        try:
            stripe.Subscription.cancel(user.sub_id)
        except:
            pass
        user.delete()
        return Response(status=SUCCESS, headers=HEADERS)
    else:
        return Response(status=ERROR, headers=HEADERS)


@api_view(['POST'])
def get_user(request):
    try:
        username   = request.data['user']
        token      = request.data['token']
        
        auth, msg = get_auth(request, username, token)
        
        if auth['auth'] != 'Visitor':
            stats = 'Inscrito' if auth['auth'] == 'Client' else 'Nao Inscrito'
            user  = User.objects.get(username=username)
            data  = {
                "user": user.username,
                "email": user.email,
                "status": stats
            }
            return Response(data, status=SUCCESS, headers=HEADERS)
        else:
            return Response(status=ERROR, headers=HEADERS)
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(['POST'])
def check_auth(request):
    try:
        username   = request.data['user']
        token      = request.data['token']

        auth , msg = get_auth(request, username, token)
        return Response(auth, status=SUCCESS, headers=HEADERS)
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)



@api_view(['POST'])
def update_email(request):
    try:
        username   = request.data['user']
        token      = request.data['token']
        email      = request.data['email']
        
        auth, msg = get_auth(request, username, token)
        
        if auth['auth'] != 'Visitor':
            user  = User.objects.get(username=username)
            user.email = email
            user.save()
            return Response(status=SUCCESS, headers=HEADERS)
        else:
            return Response(status=ERROR, headers=HEADERS)
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)

@api_view(['POST'])
def update_password(request):
    try:
        username   = request.data['user']
        token      = request.data['token']
        password   = request.data['pass']
        
        auth, msg = get_auth(request, username, token)
        
        if auth['auth'] != 'Visitor':
            user  = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return Response(status=SUCCESS, headers=HEADERS)
        else:
            password_token = PasswordToken.objects.get(id=token)
            username       = password_token.user
            user           = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return Response(status=SUCCESS, headers=HEADERS)
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)

@api_view(["POST"])
def forgot_password(request):
    try:
        email = request.data['email']
        user  = User.objects.get(email=email)
        token = create_password_token(user.username)
        
        send_mail(
            'Recuperação de senha - Cloud Pharma',
            f'Entre no link abaixo {settings.FRONTEND_URL}recoverpassword/{token}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        return Response(status=SUCCESS, headers=HEADERS)

    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(['POST'])
def create_subscription(request):
    data = request.data
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                'price' : data['price_id'],
                'quantity' : 1
                }
            ],
            mode = 'subscription', 
            success_url = settings.FRONTEND_URL + 'success/{CHECKOUT_SESSION_ID}',
            cancel_url  = settings.FRONTEND_URL +'failure'       
        )
        return redirect(checkout_session.url , code=303)
    except Exception as message:
        return Response(message, status=ERROR, headers=HEADERS)

@api_view(['POST'])
def delete_subscription(request):
    username   = request.data['user']
    token      = request.data['token']

    auth , msg = get_auth(request, username, token)
    
    if auth['auth'] == 'Client':
        user = User.objects.get(username=username)
        stripe.Subscription.cancel(user.sub_id)
        user.sub_id = ''
        user.status = True
        user.save()
        return Response(status=SUCCESS, headers=HEADERS)
    else:
        return Response(status=ERROR, headers=HEADERS)

@api_view(['POST'])
def validate_stripe_payment(request):
    try:
        session_id = request.data['id']
        session    = stripe.checkout.Session.retrieve(session_id)
        sub_id     = session['subscription']
        username   = request.data['user']
        token      = request.data['token']
        
        auth, msg = get_auth(request, username, token)
        
        if auth['auth'] != 'User':
            return Response(status=ERROR, headers=HEADERS)
        
        newuser        = User.objects.get(username=username)
        newuser.sub_id = sub_id
        newuser.status = True
        newuser.save()

        return Response(data={'message': 'Success'}, status=status.HTTP_200_OK, headers=HEADERS)

    except:
        return Response(data={'message': 'Error'}, status=ERROR, headers=HEADERS)


@api_view(['POST'])
def validadte_password_token(request):
    token = request.data['token']
    
    try:
        PasswordToken.objects.get(id=token)
        return Response(status=SUCCESS, headers=HEADERS)

    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(['POST'])
def contact(request):
    try:
        name    = request.data['name']
        email   = request.data['email']
        subject = request.data['subject']
        message = request.data['message']
        
        send_mail(
                subject,
                f'Mensagem de {name}({email}): \n{message}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        
        return Response(status=SUCCESS, headers=HEADERS)

    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)