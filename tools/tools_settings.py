#Setting file to tools

import logging

logger=logging.getLogger(name="amf_tools")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

amf_server_url = 'http://127.0.0.1:8000/api/'




