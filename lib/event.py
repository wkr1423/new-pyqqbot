import importlib
import os
import threading

from lib.misc import removeDirs, removeMiscPath, getClasses
from settings import LOGGER, EVENT_PATH, EVENT_PACKAGE


class BaseEvent:
    """
    eventName: 事件名称，即type str
    condition: 触发条件，触发为true，否则为false
    dataPack: 数据包，写包名
    """
    eventName = []
    dataPack = object
    isActiveEvent = False
    delay = 1145141919810

    @staticmethod
    def condition(data):
        ...


activeEventsHandlers = {}


def activeEventHandler(condition, delay, name):
    if condition(None):
        for handler in activeEventsHandlers[name]:
            threading.Thread(target=handler).start()
    threading.Timer(delay, activeEventHandler, (condition, delay, name)).start()


def eventsLoader(eventTypes, eventInfo):
    LOGGER.info("===加载事件===")
    LOGGER.info("->加载新的事件(若未修改则不加载)")
    # 获取event文件夹下的所有文件名，并删除多余的文件
    eventFiles = removeDirs(EVENT_PATH, removeMiscPath(os.listdir(EVENT_PATH)))
    for eventFile in eventFiles:
        loadEventsFromFile(eventFile, eventTypes, eventInfo)
    LOGGER.debug("已加载事件及对应主事件：\n")


def loadEventsFromFile(fileName, eventTypes, eventInfo):
    LOGGER.info(f"*加载{fileName}中的事件")
    # 导入事件
    eventModule = importlib.import_module(f"{EVENT_PACKAGE}.{fileName.split('.')[0]}")  # 此处是把模块名取出来
    importlib.reload(eventModule)  # 这个是为了重载
    eventClasses = getClasses(eventModule)  # 获取文件中的class
    for eventClass in eventClasses:
        initedEventClass = eventClass[1]()  # 初始化
        eventClassName = eventClass[0]  # 获取类名
        # isinstance判断是否继承了BaseEvent类，type排除他本尊
        if isinstance(initedEventClass, BaseEvent) and type(initedEventClass) is not BaseEvent:  # 判断这个是不是个event
            loadEventsFromClass(initedEventClass, eventClassName, eventTypes, eventInfo)


def loadEventsFromClass(initedEventClass, eventClassName, eventTypes, eventInfo):
    LOGGER.info(f"\t加载{eventClassName}中")
    isActiveEvent = initedEventClass.isActiveEvent
    LOGGER.info(f"事件类型：{'主动事件' if isActiveEvent else '基于QQ的事件系统的事件'}")
    if isActiveEvent:
        loadActiveEvent(initedEventClass, eventClassName)
    loadBasicEvent(initedEventClass, eventClassName, eventTypes, eventInfo)


def loadActiveEvent(initedEventClass, eventClassName):
    delay = initedEventClass.delay
    # 触发条件，触发为true，否则为false
    if initedEventClass.condition != BaseEvent.condition:
        condition = initedEventClass.condition
    else:
        LOGGER.info(f"\t\t事件不完整，无法获取触发条件")
        return False
    activeEventsHandlers[eventClassName] = []
    threading.Timer(delay, activeEventHandler, (condition, delay, eventClassName)).start()


def loadBasicEvent(initedEventClass, eventClassName, eventTypes, eventInfo):
    # 初始化主事件
    eventNames = initedEventClass.eventName
    if len(eventNames) != 0:
        for eventName in eventNames:
            if eventName not in eventTypes:
                eventTypes[eventName] = [eventClassName]
            else:
                eventTypes[eventName].append(eventClassName)
    else:
        LOGGER.info(f"\t\t事件不完整，无法获取事件名称")
        return False
    # 记录event
    data = {"handler": []}
    # 触发条件，触发为true，否则为false
    if initedEventClass.condition != BaseEvent.condition:
        data["condition"] = initedEventClass.condition
    else:
        LOGGER.info(f"\t\t事件不完整，无法获取触发条件")
        return False
    # 数据包
    if initedEventClass.dataPack != BaseEvent.dataPack:
        data["datapack"] = initedEventClass.dataPack
    else:
        LOGGER.info(f"\t\t事件不完整，无法获取数据包")
        return False
    eventInfo[eventClassName] = data
    LOGGER.info("\t\t加载完成")
    return True
