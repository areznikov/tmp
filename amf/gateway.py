from pyamf.remoting.gateway.django import DjangoGateway
from server.amf import views as views
import server.settings as settings



def echo(request, data):
    return data


def version(request):
    return settings.VERSION
    



services = {
    'server.echo': echo,
    'server.version' : version,
    'user.login': views.user_login,
    'user.logout': views.user_logout,
    'user.prove_access':views.prove_access
}

AMFGateway = DjangoGateway(services)