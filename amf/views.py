# Create your views here.
import pyamf
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import  login_required
import logging


#internal imports
import server.logconfig

logger=logging.getLogger(name="amf_server")



try:
    pyamf.register_class(User,'django.contrib.auth.models.User')
except ValueError:
    logger.warning("django.contrib.auth.models.User class already registered")


def user_logout(http_request):
    logout(http_request)


def user_login(http_request,username,password):
    user=authenticate(username=username,password=password)
    if user is not None:
        login(http_request,user)
        logger.info("user:"+username+" login from ip:"+http_request.META['HTTP_X_FORWARDED_FOR'])
        return user
    else:
        return None


@login_required
def registered_user_protected_function(http_request):
    return "You are a registered user."

