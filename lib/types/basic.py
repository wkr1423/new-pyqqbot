# 参数可能为None的我懒得写了

class BasicFriendData:
    """
    朋友基本信息
    qq: QQ号 int
    nickname: 昵称 str
    remark: 备注 str
    """

    def __init__(self, data):
        self.qq = data["id"]
        self.nickname = data["nickname"]
        self.remark = data["remark"]


class BasicGroupData:
    """
    群基本信息
    qq: 群号 int
    name: 群名 str
    permission: 机器人在群中的权限 OWNER、ADMINISTRATOR或MEMBER str
    """

    def __init__(self, data):
        self.qq = data["id"]
        self.name = data["name"]
        self.permission = data["permission"]


class GroupMemberData:
    """
    群成员的基本信息，仅限群
    qq: 群成员的QQ号 int
    memberName: 群昵称 str
    permission: 群成员在群中的权限 OWNER、ADMINISTRATOR或MEMBER str
    specialTitle: 群头衔 str
    joinTimestamp: 加入群的时间截 int
    lastSpeakTimestamp: 最后一次发言时间截 int
    muteTimeRemaining: 剩余禁言时间 int
    group: 群基本信息 BasicGroupData
    """

    def __init__(self, data):
        self.qq = data["id"]
        self.memberName = data["memberName"]
        self.permission = data["permission"]
        self.specialTitle = data["specialTitle"]
        self.joinTimestamp = data["joinTimestamp"]
        self.lastSpeakTimestamp = data["lastSpeakTimestamp"]
        self.muteTimeRemaining = data["muteTimeRemaining"]
        self.group = BasicGroupData(data["group"])


class BeDoneMemberData:
    """
    被干某事的人的信息，仅限群
    qq: 被干某事的人的QQ号 int
    memberName: 群昵称 str
    permission: 被干某事的人在群中的权限 OWNER、ADMINISTRATOR或MEMBER str
    group: 被干某事的人群基本信息 BasicGroupData
    """

    def __init__(self, data):
        self.qq = data["id"]
        self.memberName = data["memberName"]
        self.permission = data["permission"]
        self.group = BasicGroupData(data["group"])


class FriendInputStatusChangedData:
    """
    好友输入状态改变
    friend: 好友基本信息 BasicFriendData
    isInputting: 是否正在输入 bool
    """

    def __init__(self, data):
        self.friend = BasicFriendData(data["friend"])
        self.isInputting = data["inputting"]


class FriendNickChangedData:
    """
    好友昵称改变
    friend: 好友基本信息 BasicFriendData
    origin: 原昵称 str
    to: 现备注 str
    """

    def __init__(self, data):
        self.friend = BasicFriendData(data["friend"])
        self.origin = data["from"]
        self.to = data["to"]


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
    operator: 操作者信息 GroupMemberData
    """

    def __init__(self, data):
        self.durationSeconds = data["durationSeconds"]
        self.operator = GroupMemberData(data["operator"])


class BotUnmuteData:
    """
    Bot被取消禁言
    operator: 操作者信息 GroupMemberData
    """

    def __init__(self, data):
        self.operator = GroupMemberData(data["operator"])


class BotJoinGroupData:
    """
    Bot加入了一个新群
    group: 群基本信息 BasicGroupData
    invitor: 操作者信息 GroupMemberData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])
        self.invitor = None if data["invitor"] is None else GroupMemberData(data["invitor"])


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
    operator: 操作者信息 GroupMemberData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class BotLeaveDisbandData:
    """
    Bot因群主解散群而退出群, 操作人一定是群主
    group: 群基本信息 BasicGroupData
    operator: 操作者信息 GroupMemberData
    """

    def __init__(self, data):
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class GroupRecallData:
    """
    群消息撤回
    authorId: 原消息发送者的QQ号 int
    messageId: 原消息messageId int
    time: 原消息发送时间 int
    group: 消息撤回所在的群 BasicGroupData
    operator: 撤回消息的操作人，当null时为bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.authorId = data["authorId"]
        self.messageId = data["messageId"]
        self.time = data["time"]
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class FriendRecallData:
    """
    好友消息撤回
    authorId: 原消息发送者的QQ号 int
    messageId: 原消息messageId int
    time: 原消息发送时间 int
    operator: 好友QQ号或BotQQ号 int
    """

    def __init__(self, data):
        self.authorId = data["authorId"]
        self.messageId = data["messageId"]
        self.time = data["time"]
        self.operator = data["operator"]


class NudgeData:
    """
    戳一戳事件
    fromId: 动作发出者的QQ号 int
    kind: 来源的类型，"Friend"或"Group" str
    friendId, groupId: 来源的QQ号（好友）或群号 int
    action: 动作类型 str
    suffix: 自定义动作内容 str
    target: 动作目标的QQ号 int
    """

    def __init__(self, data):
        self.fromId = data["fromId"]
        self.kind = data["subject"]["kind"]
        if self.kind == "Friend":
            self.friendId = data["subject"]["id"]
        else:
            self.groupId = data["subject"]["id"]
        self.action = data["action"]
        self.suffix = data["suffix"]
        self.target = data["target"]


class GroupNameChangeData:
    """
    某个群名改变
    origin: 原群名 str
    current: 新群名 str
    group: 群名改名的群 BasicGroupData
    operator: 操作的管理员或群主信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class GroupEntranceAnnouncementChangeData:
    """
    某群入群公告改变
    origin: 原公告 str
    current: 新公告 str
    group: 公告改变的群 BasicGroupData
    operator: 操作的管理员或群主信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class GroupMuteAllData:
    """
    全员禁言改变
    origin: 原本是否处于全员禁言 bool
    current: 现在是否处于全员禁言 bool
    group: 全员禁言的群 BasicGroupData
    operator: 操作的管理员或群主信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class GroupAllowAnonymousChatData:
    """
    是否允许匿名聊天
    origin: 原本匿名聊天是否开启 bool
    current: 现在匿名聊天是否开启 bool
    group: 匿名聊天状态改变的群 BasicGroupData
    operator: 操作的管理员或群主信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class GroupAllowConfessTalkData:
    """
    坦白说是否开启
    origin: 原本坦白说是否开启 bool
    current: 现在坦白说是否开启 bool
    group: 坦白说状态改变的群信息 BasicGroupData
    isByBot: 是否Bot进行该操作 bool
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])
        self.isByBot = data["isByBot"]


class GroupAllowMemberInviteData:
    """
    是否允许群员邀请好友加群
    origin: 原本是否允许群员邀请好友加群 bool
    current: 现在是否允许群员邀请好友加群 bool
    group: 允许群员邀请好友加群状态改变的群信息 BasicGroupData
    operator: 操作的管理员或群主信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.group = BasicGroupData(data["group"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class MemberJoinData:
    """
    新人入群的事件
    member: 新人信息 GroupMemberData
    invitor: 被什么人邀请，无则为None GroupMemberData
    """

    def __init__(self, data):
        self.member = GroupMemberData(data["member"])
        self.invitor = None if data["invitor"] is None else GroupMemberData(data["invitor"])


class MemberLeaveKickData:
    """
    成员被踢出群（该成员不是Bot）
    member: 被踢者的信息 GroupMemberData
    operator: 操作的管理员或群主信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.member = GroupMemberData(data["member"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class MemberLeaveQuitData:
    """
    成员主动离群（该成员不是Bot）
    member: 被踢者的信息 BeDoneMemberData
    """

    def __init__(self, data):
        self.member = BeDoneMemberData(data["member"])


class MemberCardChangeData:
    """
    群名片改动
    origin: 原本名 str
    current: 现在名 str
    member: 名子改动的群员的信息 GroupMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.member = GroupMemberData(data["member"])


class MemberSpecialTitleChangeData:
    """
    群头衔改动（只有群主有操作限权）
    origin: 原头衔 str
    current: 现头衔 str
    member: 头衔改动的群员的信息 BeDoneMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.member = BeDoneMemberData(data["member"])


class MemberPermissionChangeData:
    """
    成员权限改变的事件（该成员不是Bot）
    origin: 原权限, ADMINISTRATOR或MEMBER str
    current: 现权限, ADMINISTRATOR或MEMBER str
    member: 头衔改动的群员的信息 BeDoneMemberData
    """

    def __init__(self, data):
        self.origin = data["origin"]
        self.current = data["current"]
        self.member = BeDoneMemberData(data["member"])


class MemberMuteData:
    """
    群成员被禁言事件（该成员不是Bot）
    durationSeconds: 禁言时长，单位为秒 int
    member: 被禁言的群员的信息 GroupMemberData
    operator: 操作者信息 GroupMemberData
    """

    def __init__(self, data):
        self.durationSeconds = data["durationSeconds"]
        self.member = GroupMemberData(data["member"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class MemberUnmuteData:
    """
    群成员被取消禁言事件（该成员不是Bot）
    member: 被取消禁言的群员的信息 GroupMemberData
    operator: 操作者的信息，当None时为Bot操作 GroupMemberData
    """

    def __init__(self, data):
        self.member = GroupMemberData(data["member"])
        self.operator = None if data["operator"] is None else GroupMemberData(data["operator"])


class MemberHonorChangeData:
    """
    群员称号改变
    member: 被取消禁言的群员的信息 GroupMemberData
    action: 称号变化行为：achieve获得称号，lose失去称号 str
    honor: 称号名称 str
    """

    def __init__(self, data):
        self.member = GroupMemberData(data["member"])
        self.action = data["action"]
        self.honor = data["honor"]


class NewFriendRequestData:
    """
    添加好友申请
    eventId: 事件标识，响应该事件时的标识 int
    fromId: 申请人QQ号 int
    groupId: 申请人如果通过某个群添加好友，该项为该群群号；否则为0 int
    nick: 申请人的昵称或群名片 str
    message: 申请消息 str
    """

    def __init__(self, data):
        self.eventId = data["eventId"]
        self.fromId = data["fromId"]
        self.groupId = data["groupId"]
        self.nick = data["nick"]
        self.message = data["message"]


class MemberJoinRequestData:
    """
    用户入群申请（Bot需要有管理员权限）
    eventId: 事件标识，响应该事件时的标识 int
    fromId: 申请人QQ号 int
    groupId: 申请人申请入群的群号 int
    groupName: 申请人申请入群的群名称 str
    nick: 申请人的昵称或群名片 str
    message: 申请消息 str
    invitorId: 邀请人，可能为None int
    """

    def __init__(self, data):
        self.eventId = data["eventId"]
        self.fromId = data["fromId"]
        self.groupId = data["groupId"]
        self.nick = data["nick"]
        self.message = data["message"]
        self.invitorId = data["invitorId"]


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
