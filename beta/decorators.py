from django.utils.functional import wraps
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.authtoken.models import Token
from .utils import token_expire_handler, get_auth
from .models import User
from rest_framework.response import Response
from rest_framework import status


HEADERS      = {
    "Access-Control-Allow-Origin": "https://cloudpharma.vercel.app",
    "Access-Control-Allow-Methods": "POST, PUT, PATCH, GET, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization"
    }
SUCCESS      = status.HTTP_200_OK
ERROR        = status.HTTP_400_BAD_REQUEST


def check_auth(required_auth:list):
    
    
    def decorator(view_function): 
        
        
        @wraps(view_function)
        def wrapper(request, *args, **kwargs):
            user       = request.data['user']
            token      = request.data['token']
            auth, msg  = get_auth(request, user, token)
            
            if auth['auth'] in required_auth:
                return view_function(request, *args, **kwargs)
            
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, headers=HEADERS)
        
        
        return wrapper
    
    
    return decorator