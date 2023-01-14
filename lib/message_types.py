import sys


class Message:
    """
    buildByDict: 通过传data字典来生成一个message对象（系统使用）
    generate: 生成一个data字典以发送消息（系统使用）
    """

    def buildByDict(self, *args): ...

    def generate(self): ...


'''{
    "type": "Quote",
    "id": 123456,
    "groupId": 123456789,
    "senderId": 987654321,
    "targetId": 9876543210,
    "origin": [
        { "type": "Plain", text: "text" }
    ] 
}'''


class Quote(Message):
    """
    回复消息
    messageId: 被引用回复的原消息的messageId int
    type: 回复消息所在的地方，“friend”或者“group” str
    fromId: 被引用回复的原消息的发送者的QQ号 int
    toId: 被引用回复的原消息的接收者者的QQ号（或群号） int
    origin: 原消息内容 list
    """

    def __init__(self):
        self.messageId = None
        self.type = None
        self.fromId = None
        self.toId = None
        self.origin = None

    def buildByArgs(self, messageId, groupId, senderId, targetId, origin):
        self.messageId = messageId
        self.type = "group"
        if groupId == 0:
            self.type = "friend"
        self.fromId = senderId
        self.toId = targetId
        self.origin = []
        for message in origin:
            processedMessage = getattr(sys.modules[__name__], message["type"])
            processedMessage.buildByDict(message)
            self.origin.append(processedMessage)

    def buildByDict(self, data):
        self.buildByArgs(data["id"], data["groupId"], data["senderId"], data["targetId"], data["origin"])

    def generate(self):
        data = {
            "type": "Quote",
            "id": self.messageId,
            "groupId": 0 if self.type == "friend" else self.toId,
            "senderId": self.fromId,
            "targetId": self.toId,
            "origin": []
        }
        for message in self.origin:
            data["origin"].append(message.generate())
        return data


class At(Message):
    """
    @某人
    at: 群员QQ号 int
    display: At时显示的文字，发送消息时无效，自动使用群名片，所以创建此消息时不必填写display str
    """

    def __init__(self):
        self.at = None
        self.display = None

    def buildByArgs(self, at, display=""):
        self.at = at
        self.display = display

    def buildByDict(self, data):
        self.buildByArgs(data["target"], data["display"])

    def generate(self):
        data = {
            "type": "At",
            "target": self.at,
            "display": self.display,
        }
        return data


class AtAll(At):
    """
    @全体成员
    """
    def __init__(self):
        super(AtAll, self).__init__()

    def buildByDict(self, data):
        self.at = "all"
        self.display = "@全体成员"

    def buildByArgs(self, *args):
        self.at = "all"
        self.display = "@全体成员"

    def generate(self):
        data = {
            "type": "AtAll"
        }
        return data


class Face(Message):
    def __init__(self):
        self.faceId = None
        self.name = None

    def buildByFaceId(self, faceId):