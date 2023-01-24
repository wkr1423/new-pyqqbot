from lib import event
from lib.types import group


class GroupRecallEvent(event.BaseEvent):
    """
    群消息撤回
    """
    eventName = ["GroupRecallEvent"]
    dataPack = group.GroupRecallData

    @staticmethod
    def condition(data):
        return True


class GroupNameChangeEvent(event.BaseEvent):
    """
    某个群名改变
    """
    eventName = ["GroupNameChangeEvent"]
    dataPack = group.GroupNameChangeData

    @staticmethod
    def condition(data):
        return True


class GroupEntranceAnnouncementChangeEvent(event.BaseEvent):
    """
    某群入群公告改变
    """
    eventName = ["GroupEntranceAnnouncementChangeEvent"]
    dataPack = group.GroupEntranceAnnouncementChangeData

    @staticmethod
    def condition(data):
        return True


class GroupMuteAllEvent(event.BaseEvent):
    """
    全员禁言改变
    """
    eventName = ["GroupMuteAllEvent"]
    dataPack = group.GroupMuteAllData

    @staticmethod
    def condition(data):
        return True


class GroupAllowAnonymousChatEvent(event.BaseEvent):
    """
    是否允许匿名聊天
    """
    eventName = ["GroupAllowAnonymousChatEvent"]
    dataPack = group.GroupAllowAnonymousChatData

    @staticmethod
    def condition(data):
        return True


class GroupAllowConfessTalkEvent(event.BaseEvent):
    """
    坦白说是否开启
    """
    eventName = ["GroupAllowConfessTalkEvent"]
    dataPack = group.GroupAllowConfessTalkData

    @staticmethod
    def condition(data):
        return True


class GroupAllowMemberInviteEvent(event.BaseEvent):
    """
    是否允许群员邀请好友加群
    """
    eventName = ["GroupAllowMemberInviteEvent"]
    dataPack = group.GroupAllowMemberInviteData

    @staticmethod
    def condition(data):
        return True


class MemberJoinEvent(event.BaseEvent):
    """
    新人入群的事件
    """
    eventName = ["MemberJoinEvent"]
    dataPack = group.MemberJoinData

    @staticmethod
    def condition(data):
        return True


class MemberLeaveEventKick(event.BaseEvent):
    """
    成员被踢出群（该成员不是Bot）
    """
    eventName = ["MemberLeaveEventKick"]
    dataPack = group.MemberLeaveKickData

    @staticmethod
    def condition(data):
        return True


class MemberLeaveEventQuit(event.BaseEvent):
    """
    成员主动离群（该成员不是Bot）
    """
    eventName = ["MemberLeaveEventQuit"]
    dataPack = group.MemberLeaveQuitData

    @staticmethod
    def condition(data):
        return True


class MemberCardChangeEvent(event.BaseEvent):
    """
    群名片改动
    """
    eventName = ["MemberCardChangeEvent"]
    dataPack = group.MemberCardChangeData

    @staticmethod
    def condition(data):
        return True


class MemberSpecialTitleChangeEvent(event.BaseEvent):
    """
    群头衔改动（只有群主有操作限权）
    """
    eventName = ["MemberSpecialTitleChangeEvent"]
    dataPack = group.MemberSpecialTitleChangeData

    @staticmethod
    def condition(data):
        return True


class MemberPermissionChangeEvent(event.BaseEvent):
    """
    成员权限改变的事件（该成员不是Bot）
    """
    eventName = ["MemberPermissionChangeEvent"]
    dataPack = group.MemberPermissionChangeData

    @staticmethod
    def condition(data):
        return True


class MemberMuteEvent(event.BaseEvent):
    """
    群成员被禁言事件（该成员不是Bot）
    """
    eventName = ["MemberMuteEvent"]
    dataPack = group.MemberMuteData

    @staticmethod
    def condition(data):
        return True


class MemberUnmuteEvent(event.BaseEvent):
    """
    群成员被取消禁言事件（该成员不是Bot）
    """
    eventName = ["MemberUnmuteEvent"]
    dataPack = group.MemberUnmuteData

    @staticmethod
    def condition(data):
        return True


class MemberHonorChangeEvent(event.BaseEvent):
    """
    群员称号改变
    """
    eventName = ["MemberHonorChangeEvent"]
    dataPack = group.MemberHonorChangeData

    @staticmethod
    def condition(data):
        return True


class MemberJoinRequestEvent(event.BaseEvent):
    """
    用户入群申请（Bot需要有管理员权限）
    """
    eventName = ["MemberJoinRequestEvent"]
    dataPack = group.MemberJoinRequestData

    @staticmethod
    def condition(data):
        return True
