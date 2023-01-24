from lib.types.public import BasicQQUserData


class BasicPlatformData:
    """
    可了解群消息的平台的信息
    qq: 发送者qq号 int
    platform: 可看的平台 str
    """

    def __init__(self, data):
        self.qq = data["id"]
        self.platform = data["platform"]


class FriendInputStatusChangedData:
    """
    好友输入状态改变
    friend: 好友基本信息 BasicQQUserData
    isInputting: 是否正在输入 bool
    """

    def __init__(self, data):
        self.friend = BasicQQUserData(data["friend"])
        self.isInputting = data["inputting"]


class FriendNickChangedData:
    """
    好友昵称改变
    friend: 好友基本信息 BasicQQUserData
    origin: 原昵称 str
    to: 现备注 str
    """

    def __init__(self, data):
        self.friend = BasicQQUserData(data["friend"])
        self.origin = data["from"]
        self.to = data["to"]


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
