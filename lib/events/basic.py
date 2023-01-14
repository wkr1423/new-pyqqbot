from lib.event import BaseEvent


class FriendInputStatusChangedEvent(BaseEvent):
    """
    好友输入状态改变
    """
    eventName = ["FriendInputStatusChangedEvent"]
    dataPack = "lib.types.basic.FriendInputStatusChangedData"

    @staticmethod
    def condition(data):
        return True


class FriendNickChangedEvent(BaseEvent):
    """
    好友昵称改变
    """
    eventName = ["FriendNickChangedEvent"]
    dataPack = "lib.types.basic.FriendNickChangedData"

    @staticmethod
    def condition(data):
        return True


class BotGroupPermissionChangeEvent(BaseEvent):
    """
    Bot在群里的权限被改变. 操作人一定是群主
    """
    eventName = ["BotGroupPermissionChangeEvent"]
    dataPack = "lib.types.basic.BotGroupPermissionChangeData"

    @staticmethod
    def condition(data):
        return True


class BotMuteEvent(BaseEvent):
    """
    Bot被禁言
    """
    eventName = ["BotMuteEvent"]
    dataPack = "lib.types.basic.BotMuteData"

    @staticmethod
    def condition(data):
        return True


class BotUnmuteEvent(BaseEvent):
    """
    Bot被取消禁言
    """
    eventName = ["BotUnmuteEvent"]
    dataPack = "lib.types.basic.BotUnmuteData"

    @staticmethod
    def condition(data):
        return True


class BotJoinGroupEvent(BaseEvent):
    """
    Bot加入了一个新群
    """
    eventName = ["BotJoinGroupEvent"]
    dataPack = "lib.types.basic.BotJoinGroupData"

    @staticmethod
    def condition(data):
        return True


class BotLeaveEventActive(BaseEvent):
    """
    Bot主动退出一个群
    """
    eventName = ["BotLeaveEventActive"]
    dataPack = "lib.types.basic.BotLeaveActiveData"

    @staticmethod
    def condition(data):
        return True


class BotLeaveEventKick(BaseEvent):
    """
    Bot被踢出一个群
    """
    eventName = ["BotLeaveEventKick"]
    dataPack = "lib.types.basic.BotLeaveKickData"

    @staticmethod
    def condition(data):
        return True


class BotLeaveEventDisband(BaseEvent):
    """
    Bot因群主解散群而退出群, 操作人一定是群主
    """
    eventName = ["BotLeaveEventDisband"]
    dataPack = "lib.types.basic.BotLeaveDisbandData"

    @staticmethod
    def condition(data):
        return True


class GroupRecallEvent(BaseEvent):
    """
    群消息撤回
    """
    eventName = ["GroupRecallEvent"]
    dataPack = "lib.types.basic.GroupRecallData"

    @staticmethod
    def condition(data):
        return True


class FriendRecallEvent(BaseEvent):
    """
    好友消息撤回
    """
    eventName = ["FriendRecallEvent"]
    dataPack = "lib.types.basic.FriendRecallData"

    @staticmethod
    def condition(data):
        return True


class NudgeEvent(BaseEvent):
    """
    戳一戳事件
    """
    eventName = ["NudgeEvent"]
    dataPack = "lib.types.basic.NudgeData"

    @staticmethod
    def condition(data):
        return True


class GroupNameChangeEvent(BaseEvent):
    """
    某个群名改变
    """
    eventName = ["GroupNameChangeEvent"]
    dataPack = "lib.types.basic.GroupNameChangeData"

    @staticmethod
    def condition(data):
        return True


class GroupEntranceAnnouncementChangeEvent(BaseEvent):
    """
    某群入群公告改变
    """
    eventName = ["GroupEntranceAnnouncementChangeEvent"]
    dataPack = "lib.types.basic.GroupEntranceAnnouncementChangeData"

    @staticmethod
    def condition(data):
        return True


class GroupMuteAllEvent(BaseEvent):
    """
    全员禁言改变
    """
    eventName = ["GroupMuteAllEvent"]
    dataPack = "lib.types.basic.GroupMuteAllData"

    @staticmethod
    def condition(data):
        return True


class GroupAllowAnonymousChatEvent(BaseEvent):
    """
    是否允许匿名聊天
    """
    eventName = ["GroupAllowAnonymousChatEvent"]
    dataPack = "lib.types.basic.GroupAllowAnonymousChatData"

    @staticmethod
    def condition(data):
        return True


class GroupAllowConfessTalkEvent(BaseEvent):
    """
    坦白说是否开启
    """
    eventName = ["GroupAllowConfessTalkEvent"]
    dataPack = "lib.types.basic.GroupAllowConfessTalkData"

    @staticmethod
    def condition(data):
        return True


class GroupAllowMemberInviteEvent(BaseEvent):
    """
    是否允许群员邀请好友加群
    """
    eventName = ["GroupAllowMemberInviteEvent"]
    dataPack = "lib.types.basic.GroupAllowMemberInviteData"

    @staticmethod
    def condition(data):
        return True


class MemberJoinEvent(BaseEvent):
    """
    新人入群的事件
    """
    eventName = ["MemberJoinEvent"]
    dataPack = "lib.types.basic.MemberJoinData"

    @staticmethod
    def condition(data):
        return True


class MemberLeaveEventKick(BaseEvent):
    """
    成员被踢出群（该成员不是Bot）
    """
    eventName = ["MemberLeaveEventKick"]
    dataPack = "lib.types.basic.MemberLeaveKickData"

    @staticmethod
    def condition(data):
        return True


class MemberLeaveEventQuit(BaseEvent):
    """
    成员主动离群（该成员不是Bot）
    """
    eventName = ["MemberLeaveEventQuit"]
    dataPack = "lib.types.basic.MemberLeaveQuitData"

    @staticmethod
    def condition(data):
        return True


class MemberCardChangeEvent(BaseEvent):
    """
    群名片改动
    """
    eventName = ["MemberCardChangeEvent"]
    dataPack = "lib.types.basic.MemberCardChangeData"

    @staticmethod
    def condition(data):
        return True


class MemberSpecialTitleChangeEvent(BaseEvent):
    """
    群头衔改动（只有群主有操作限权）
    """
    eventName = ["MemberSpecialTitleChangeEvent"]
    dataPack = "lib.types.basic.MemberSpecialTitleChangeData"

    @staticmethod
    def condition(data):
        return True


class MemberPermissionChangeEvent(BaseEvent):
    """
    成员权限改变的事件（该成员不是Bot）
    """
    eventName = ["MemberPermissionChangeEvent"]
    dataPack = "lib.types.basic.MemberPermissionChangeData"

    @staticmethod
    def condition(data):
        return True


class MemberMuteEvent(BaseEvent):
    """
    群成员被禁言事件（该成员不是Bot）
    """
    eventName = ["MemberMuteEvent"]
    dataPack = "lib.types.basic.MemberMuteData"

    @staticmethod
    def condition(data):
        return True


class MemberUnmuteEvent(BaseEvent):
    """
    群成员被取消禁言事件（该成员不是Bot）
    """
    eventName = ["MemberUnmuteEvent"]
    dataPack = "lib.types.basic.MemberUnmuteData"

    @staticmethod
    def condition(data):
        return True


class MemberHonorChangeEvent(BaseEvent):
    """
    群员称号改变
    """
    eventName = ["MemberHonorChangeEvent"]
    dataPack = "lib.types.basic.MemberHonorChangeData"

    @staticmethod
    def condition(data):
        return True


class NewFriendRequestEvent(BaseEvent):
    """
    添加好友申请
    """
    eventName = ["NewFriendRequestEvent"]
    dataPack = "lib.types.basic.NewFriendRequestData"

    @staticmethod
    def condition(data):
        return True


class MemberJoinRequestEvent(BaseEvent):
    """
    用户入群申请（Bot需要有管理员权限）
    """
    eventName = ["MemberJoinRequestEvent"]
    dataPack = "lib.types.basic.MemberJoinRequestData"

    @staticmethod
    def condition(data):
        return True


class BotInvitedJoinGroupRequestEvent(BaseEvent):
    """
    Bot被邀请入群申请
    """
    eventName = ["BotInvitedJoinGroupRequestEvent"]
    dataPack = "lib.types.basic.BotInvitedJoinGroupRequestData"

    @staticmethod
    def condition(data):
        return True


'''
class MessageEvent(BaseEvent):
    """
    bot收到朋友的消息
    """
    eventName = ["FriendMessage", "GroupMessage", "TempMessage", "StrangerMessage"]
    dataPack = "lib.types.basic.BotInvitedJoinGroupRequestData"
'''
