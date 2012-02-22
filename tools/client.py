from pyamf.remoting.client import RemotingService

#local includes
import _settings as settings

gw = RemotingService(settings.AMF_SERVER_URL,logger=settings.logger)
gw.setCredentials("test","test")
service = gw.getService('server')


print service.echo('Hello World!')
print service.version()

player = gw.getService('user')


player.prove_access("I have access to it")



gw.setCredentials("","")
player.prove_access("I have access to it")