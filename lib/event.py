class BaseEvent:
    """
    eventName: 事件名称，即type str
    condition: 触发条件，触发为true，否则为false
    dataPack: 数据包，写包名
    """
    eventName = []
    dataPack = ""

    @staticmethod
    def condition(data):
        ...
