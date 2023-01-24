import logging
import os

# 验证密码
VERIFY_KEY = "INITKEYosGKcJU8"

# path
PATH = os.path.abspath(os.path.dirname(__file__))
PLUGIN_PACKAGE = "plugins"
PLUGIN_PATH = os.path.join(PATH, PLUGIN_PACKAGE)
EVENT_PACKAGE = "lib.events"
EVENT_PATH = os.path.join(PATH, EVENT_PACKAGE.replace(".", '/'))
SESSION_PATH = os.path.join(PATH, "lib/api/session_key")
PATH_BLACKLIST = ["__init__.py", "__pycache__"]

# qq config
QQ_ID = 1726237584
GROUP_ID = [790391238]

# api location
HTTP_HOST = WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 6700
HTTP_PORT = 5700

# log config
LOG_LEVEL = logging.DEBUG
logging.basicConfig(format="[%(asctime)s](%(levelname)s): %(message)s", level=LOG_LEVEL)
LOGGER = logging.getLogger()

# 疯狂atall，解决atall消息用完的暴力方式，不建议打卡，疯狂扰民
CRAZY_ATALL = False
MAX_ATALL_LENGTH = 200
