import logging
import os

# 验证密码
VERIFY_KEY = "wkr20080124"

# path
PATH = os.path.abspath(os.path.dirname(__file__))
PLUGIN_PACKAGE = "plugins"
PLUGIN_PATH = os.path.join(PATH, PLUGIN_PACKAGE)
EVENT_PACKAGE = "lib.events"
EVENT_PATH = os.path.join(PATH, EVENT_PACKAGE.replace(".", '/'))
PATH_BLACKLIST = ["__init__.py", "__pycache__"]

# qq config
QQ_ID = 1726237584
GROUP_ID = [790391238]

# api location
HOST = "localhost"
PORT = 8000

# log config
LOG_LEVEL = logging.DEBUG
logging.basicConfig(format="[%(asctime)s](%(levelname)s): %(message)s", level=LOG_LEVEL)
LOGGER = logging.getLogger()
