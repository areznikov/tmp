from pyamf.remoting.gateway.django import DjangoGateway
from django.contrib.auth import authenticate as django_authenticate

#local including
from server.amf import views as views
import server.settings as settings
import server.settings_server as settings_server


def echo(request, data):
    return data


def version(request):
    return settings_server.VERSION
    
def auth(username,password):
    user= django_authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            return True
    return False



services = {
    'server.echo': echo,
    'server.version' : version,
}

pub_services = {
    'server.echo': echo,
    'server.version' : version,
    'user.login': views.login,
    'user.logout': views.logout
}


#AMFGateway = DjangoGateway(services, authenticator=auth)
AMFGateway = DjangoGateway(services)
Pub_AMFGateway = DjangoGateway(pub_services)