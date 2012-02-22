from pyamf.remoting.gateway.django import DjangoGateway
from django.contrib.auth import authenticate as django_authenticate
from server.amf import views as views
import server.settings as settings



def echo(request, data):
    return data


def version(request):
    return settings.VERSION
    
def auth(username,password):
    user= django_authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            return True
    return False



services = {
    'server.echo': echo,
    'server.version' : version,
    #'user.login': views.user_login,
    #'user.logout': views.user_logout,
    #'user.prove_access':views.prove_access
}

AMFGateway = DjangoGateway(services, authenticator=auth)
