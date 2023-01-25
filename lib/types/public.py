# 参数可能为None的我懒得写了
from lib import message_types
from lib.types.group import BasicGroupMemberData


class BasicQQUserData:
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


class QQUserData:
    """
    朋友基本信息
    qq: QQ号 int
    nickname: 昵称 str
    remark: 备注 str
    """

    def __init__(self, data):
        self.nickname = data["nickname"]
        self.email = data["email"]
        self.age = data["age"]
        self.level = data["level"]
        self.sign = data["sign"]
        self.sex = data["sex"]


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


class MessageData:
    def __init__(self, data):
        messageType = data["type"]
        if messageType == "FriendMessage":
            self.type = "friend"
            self.sender = BasicQQUserData(data["sender"])
        elif messageType == "GroupMessage":
            self.type = "group"
            self.sender = BasicGroupMemberData(data["sender"])
        elif messageType == "TempMessage":
            self.type = "temp"
            self.sender = BasicGroupMemberData(data["sender"])
        elif messageType == "OtherClientMessage":
            self.type = "other_client_available"
            self.sender = BasicQQUserData(data["sender"])
        self.id = data["messageChain"][0]["id"]
        self.time = data["messageChain"][0]["time"]
        del data["messageChain"][0]
        self.messageChain = []
        for message in data["messageChain"]:
            processor = getattr(message_types, message["type"])()
            print(processor)
            processor.buildByDict(message)
            self.messageChain.append(processor)
