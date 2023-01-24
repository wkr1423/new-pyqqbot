import json
import threading
import time

import websocket

from lib.api.session import verify
from lib.event import eventsLoader
from lib.misc import startFunc
from settings import LOGGER, VERIFY_KEY, QQ_ID, WEBSOCKET_HOST, WEBSOCKET_PORT

eventTypes = {}
eventInfo = {}
work = []


def onBasicEvent(data):
    if data["type"] not in eventTypes.values():
        LOGGER.info(f"未知的事件{data['type']}，请联系开发者以获取帮助")
        return
    for event in eventTypes[data["type"]]:
        if eventInfo[event]["condition"](data):
            for handler in eventInfo[event]["handler"]:
                threading.Thread(target=startFunc, args=(handler, work, (eventInfo[event]["datapack"](data),))).start()


def loadEvents():
    """
    events:
    &nbsp;&nbsp;&nbsp;&nbsp;eventName:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;xxxEvent:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;datapack: lib.types.basic.xxxData
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;condition: function
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;handler: []
    """
    global eventTypes, eventInfo
    eventTypes = {}
    eventInfo = {}
    eventsLoader(eventTypes, eventInfo)
    LOGGER.debug("已加载的事件:\n" + json.dumps(eventTypes, indent=4))


class QQBot:
    def __init__(self):
        # 打开bot
        self.ws = None

    def on_message(self, _, message):
        message = json.loads(message)
        data = message["data"]
        if "type" in data:
            LOGGER.info(f"收到一个event: {data['type']}")

            threading.Thread(target=onBasicEvent, args=(data,)).start()
        LOGGER.debug(json.dumps(message, indent=4))

    def on_close(self, *args):
        if len(args) != 0 and type(args[1]) == KeyboardInterrupt:
            exit()
        LOGGER.info(f"遇到关闭，正在重启  {args}")
        time.sleep(1)
        self.start()

    def start(self):
        # 初始化
        verify()
        loadEvents()
        self.ws = websocket.WebSocketApp(
            f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}/all?verifyKey={VERIFY_KEY}&qq={QQ_ID}",
            on_message=self.on_message,
            on_error=self.on_close,
            on_close=self.on_close,
        )
        self.ws.run_forever()
