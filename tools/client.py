from pyamf.remoting.client import RemotingService

#local includes
import _settings as settings

gw = RemotingService(settings.AMF_SERVER_URL,logger=settings.logger)
#gw.setCredentials("test","test")
service = gw.getService('server')


print service.echo('Hello World!')
print service.version()

