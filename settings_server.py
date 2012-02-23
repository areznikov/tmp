import logging

# LOGGING PART
logging.getLogger(name="amf_server")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)


# SERVER CONFIGURATION
VERSION="0.0a"
HOST="http://dev.unixsupport.ru/"
AVATAR_PREFIX=HOST+"/avatar/"
#Player default settings
Player_avatar_default = AVATAR_PREFIX+"default.jpg"
Player_experience_start=100
Player_coins_golden_start=0
Player_coins_silver_start=50
#Player Statuses
Player_Statuses = (
    (0,"In menu"),
    (1,"Wait for rival"),
    (2,"In game")
    )

