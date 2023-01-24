from lib import event
from lib.types import public


class NudgeEvent(event.BaseEvent):
    """
    戳一戳事件
    """
    eventName = ["NudgeEvent"]
    dataPack = public.NudgeData

    @staticmethod
    def condition(data):
        return True


class MessageEvent(event.BaseEvent):
    """
    bot收到朋友的消息
    """
    eventName = ["FriendMessage", "GroupMessage", "TempMessage", "StrangerMessage", "OtherClientMessage"]
    dataPack = public.MessageData

    @staticmethod
    def condition(data):
        return True
