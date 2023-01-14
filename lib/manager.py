import importlib
import json
import os
import threading
import time

import websocket

from lib.event import BaseEvent
from lib.misc import removeMiscPath, removeDirs, getFileMD5, getClasses
from settings import LOGGER, VERIFY_KEY, QQ_ID, HOST, PORT, PLUGIN_PATH, EVENT_PATH, EVENT_PACKAGE, PATH

events = {}


def onEvent(data):
    for event in events[data["type"]]:
        if events[data["type"]][event]["condition"](data):
            for handler in events[data["type"]][event]["handler"]:
                threading.Thread(target=handler, args=(events[data["type"]][event]["datapack"](data),), daemon=True).start()


def loadEvents():
    """
    events:
    &nbsp;&nbsp;&nbsp;&nbsp;eventName:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;xxxEvent:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;datapack: lib.types.basic.xxxData
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;condition: function
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;handler: []
    """
    global events
    LOGGER.info("===加载事件===")
    LOGGER.info("->加载新的事件(若未修改则不加载)")
    eventFiles = removeDirs(EVENT_PATH, removeMiscPath(os.listdir(EVENT_PATH)))
    for eventFile in eventFiles:
        LOGGER.info(f"*加载{eventFile}中的事件")
        # 导入事件
        eventModule = importlib.import_module(f"{EVENT_PACKAGE}.{eventFile.split('.')[0]}")
        importlib.reload(eventModule)  # 这个是为了重载
        eventClasses = getClasses(eventModule)  # 获取文件中的class
        for eventClass in eventClasses:
            initedEventClass = eventClass[0]()  # 初始化
            eventClassName = eventClass[1]  # 获取类名
            if isinstance(initedEventClass, BaseEvent) and type(initedEventClass) is not BaseEvent:  # 判断这个是不是个event
                LOGGER.info(f"\t加载{eventClassName}中")
                # 事件名称，即type
                eventNames = initedEventClass.eventName
                for eventName in eventNames:
                    if eventName != BaseEvent.eventName:
                        if eventName not in events:
                            events[eventName] = {}
                    else:
                        LOGGER.info(f"\t\t事件不完整，无法获取事件名称")
                        continue
                data = {"handler": []}
                # 触发条件，触发为true，否则为false
                if initedEventClass.condition != BaseEvent.condition:
                    data["condition"] = initedEventClass.condition
                else:
                    LOGGER.info(f"\t\t事件不完整，无法获取触发条件")
                    continue
                # 数据包包名
                if initedEventClass.dataPack != BaseEvent.dataPack:
                    splitDataPack = initedEventClass.dataPack.split(".")
                    LOGGER.debug(".".join(splitDataPack[:-1]))
                    LOGGER.debug(getattr(importlib.import_module(".".join(splitDataPack[:-1])), splitDataPack[-1]))
                    data["datapack"] = getattr(importlib.import_module(".".join(splitDataPack[:-1])),
                                               splitDataPack[-1])
                else:
                    LOGGER.info(f"\t\t事件不完整，无法获取数据包包名")
                    continue
                for eventName in eventNames:
                    if eventName != BaseEvent.eventName:
                        events[eventName][eventClassName] = data
                LOGGER.info("\t\t加载完成")
    LOGGER.debug(events)


class QQBot:
    def __init__(self):
        # 打开bot
        self.ws = None

    def on_message(self, _, message):
        message = json.loads(message)
        data = message["data"]
        if "type" in data:
            LOGGER.info(f"收到一个event: {data['type']}")
            threading.Thread(target=onEvent, args=(data,), daemon=True).start()
        LOGGER.debug(json.dumps(message, indent=4))

    def on_close(self, *args):
        if len(args) != 0 and type(args[1]) == KeyboardInterrupt:
            exit()
        LOGGER.info(f"遇到关闭，正在重启  {args}")
        time.sleep(1)
        self.start()

    def start(self):
        # 初始化
        loadEvents()
        self.ws = websocket.WebSocketApp(
            f"ws://{HOST}:{PORT}/all?verifyKey={VERIFY_KEY}&qq={QQ_ID}",
            on_message=self.on_message,
            on_error=self.on_close,
            on_close=self.on_close,
        )
        self.ws.run_forever(ping_interval=60, ping_timeout=5)
