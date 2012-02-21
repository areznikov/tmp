from pyamf.remoting.gateway.django import DjangoGateway
from amf.views import views as views
import settings 



def echo(request, data):
    return data

def version():
    return settings.VERSION
    



services = {
    'server.echo': echo,
    'server.get_version' : version,
    'user.login': views.user_login,
    'user.logout': views.user_logout
}

AMFGateway = DjangoGateway(services)