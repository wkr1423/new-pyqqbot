from lib import event
from lib.types import friend


class FriendInputStatusChangedEvent(event.BaseEvent):
    """
    好友输入状态改变
    """
    eventName = ["FriendInputStatusChangedEvent"]
    dataPack = friend.FriendInputStatusChangedData

    @staticmethod
    def condition(data):
        return True


class FriendNickChangedEvent(event.BaseEvent):
    """
    好友昵称改变
    """
    eventName = ["FriendNickChangedEvent"]
    dataPack = friend.FriendNickChangedData

    @staticmethod
    def condition(data):
        return True


class FriendRecallEvent(event.BaseEvent):
    """
    好友消息撤回
    """
    eventName = ["FriendRecallEvent"]
    dataPack = friend.FriendRecallData

    @staticmethod
    def condition(data):
        return True


class NewFriendRequestEvent(event.BaseEvent):
    """
    添加好友申请
    """
    eventName = ["NewFriendRequestEvent"]
    dataPack = friend.NewFriendRequestData

    @staticmethod
    def condition(data):
        return True
