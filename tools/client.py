from

from pyamf.remoting.client import RemotingService


gw = RemotingService(url, logger=logging)
service = gw.getService('myservice')

print service.echo('Hello World!')
