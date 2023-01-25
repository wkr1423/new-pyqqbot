from lib.types.group import BasicGroupData, BasicGroupMemberData


class BotGroupPermissionChangeData:
    """
    Bot在群里的权限被改变. 操作人一定是群主
    origin: 原权限 OWNER、ADMINISTRATOR或MEMBER str
    current: 新权限 OWNER、ADMINISTRATOR或MEMBER str
    group: 群基本信息 BasicGroupData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])


class BotMuteData:
    """
    Bot被禁言
    durationSeconds: 禁言时长 int
    operator: 操作者信息 BasicGroupMemberData
    """

    def __init__(self, data):
        self.durationSeconds = data["durationSeconds"]
        self.operator = BasicGroupMemberData(data["operator"])


class BotUnmuteData:
    """
    Bot被取消禁言
    operator: 操作者信息 BasicGroupMemberData
    """

    def __init__(self, data):
        self.operator = BasicGroupMemberData(data["operator"])


class BotJoinGroupData:
    """
    Bot加入了一个新群
    group: 群基本信息 BasicGroupData
    invitor: 操作者信息 BasicGroupMemberData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])
        self.invitor = None if data["invitor"] is None else BasicGroupMemberData(data["invitor"])


class BotLeaveActiveData:
    """
    Bot主动退出一个群
    group: 群基本信息 BasicGroupData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])


class BotLeaveKickData:
    """
    Bot被踢出一个群
    group: 群基本信息 BasicGroupData
    operator: 操作者信息 BasicGroupMemberData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else BasicGroupMemberData(data["operator"])


class BotLeaveDisbandData:
    """
    Bot因群主解散群而退出群, 操作人一定是群主
    group: 群基本信息 BasicGroupData
    operator: 操作者信息 BasicGroupMemberData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else BasicGroupMemberData(data["operator"])


class BotInvitedJoinGroupRequestData:
    """
    Bot被邀请入群申请
    eventId: 事件标识，响应该事件时的标识 int
    fromId: 邀请人（好友）的QQ号 int
    groupId: 被邀请进入群的群号 int
    groupName: 被邀请进入群的群名称 str
    nick: 邀请人（好友）的昵称 str
    message: 邀请消息 str
    """

    def __init__(self, data):
        self.eventId = data["eventId"]
        self.fromId = data["fromId"]
        self.groupId = data["groupId"]
        self.groupName = data["groupName"]
        self.nick = data["nick"]
        self.message = data["message"]
