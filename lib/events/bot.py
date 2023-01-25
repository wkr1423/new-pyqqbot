from lib import event
from lib.types import bot


class BotGroupPermissionChangeEvent(event.BaseEvent):
    """
    Bot在群里的权限被改变. 操作人一定是群主
    """
    eventName = ["BotGroupPermissionChangeEvent"]
    dataPack = bot.BotGroupPermissionChangeData

    @staticmethod
    def condition(data):
        return True


class BotMuteEvent(event.BaseEvent):
    """
    Bot被禁言
    """
    eventName = ["BotMuteEvent"]
    dataPack = bot.BotMuteData

    @staticmethod
    def condition(data):
        return True


class BotUnmuteEvent(event.BaseEvent):
    """
    Bot被取消禁言
    """
    eventName = ["BotUnmuteEvent"]
    dataPack = bot.BotUnmuteData

    @staticmethod
    def condition(data):
        return True


class BotJoinGroupEvent(event.BaseEvent):
    """
    Bot加入了一个新群
    """
    eventName = ["BotJoinGroupEvent"]
    dataPack = bot.BotJoinGroupData

    @staticmethod
    def condition(data):
        return True


class BotLeaveEventActive(event.BaseEvent):
    """
    Bot主动退出一个群
    """
    eventName = ["BotLeaveEventActive"]
    dataPack = bot.BotLeaveActiveData

    @staticmethod
    def condition(data):
        return True


class BotLeaveEventKick(event.BaseEvent):
    """
    Bot被踢出一个群
    """
    eventName = ["BotLeaveEventKick"]
    dataPack = bot.BotLeaveKickData

    @staticmethod
    def condition(data):
        return True


class BotLeaveEventDisband(event.BaseEvent):
    """
    Bot因群主解散群而退出群, 操作人一定是群主
    """
    eventName = ["BotLeaveEventDisband"]
    dataPack = bot.BotLeaveDisbandData

    @staticmethod
    def condition(data):
        return True


class BotInvitedJoinGroupRequestEvent(event.BaseEvent):
    """
    Bot被邀请入群申请
    """
    eventName = ["BotInvitedJoinGroupRequestEvent"]
    dataPack = bot.BotInvitedJoinGroupRequestData

    @staticmethod
    def condition(data):
        return True
