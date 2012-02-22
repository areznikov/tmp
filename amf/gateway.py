from pyamf.remoting.gateway.django import DjangoGateway
from server.amf import views as views
import settings 



def echo(request, data):
    return data

def version(request):
    return settings.VERSION
    



services = {
    'server.echo': echo,
    'server.version' : version,
    'user.login': views.user_login,
    'user.logout': views.user_logout
}

AMFGateway = DjangoGateway(services)