import json
import sys

from settings import LOGGER


class Message:
    """
    buildByDict: 通过传data字典来生成一个message对象（系统使用）
    generate: 生成一个data字典以发送消息（系统使用）
    """

    def __init__(self):
        self.isBuilt = False

    def buildByDict(self, *args): ...

    def generate(self): ...


class Quote(Message):
    """
    回复消息
    messageId: 被引用回复的原消息的messageId int
    type: 回复消息所在的地方，“friend”或者“group” str
    fromId: 被引用回复的原消息的发送者的QQ号 int
    toId: 被引用回复的原消息的接收者者的QQ号（或群号） int
    origin: 原消息内容 本文件中所涉及到的各种class[]（除了那些你在客户端发不了的消息节点）
    """

    def __init__(self):
        super(Quote, self).__init__()
        self.messageId = None
        self.type = None
        self.fromId = None
        self.toId = None
        self.origin = None

    def buildByArgs(self, messageId, groupId, senderId, targetId, origin):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.messageId = messageId
        self.type = "group"
        if groupId == 0:
            self.type = "friend"
        self.fromId = senderId
        self.toId = targetId
        self.origin = origin
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.messageId = data["messageId"]
        self.type = "group"
        if data["groupId"] == 0:
            self.type = "friend"
        self.fromId = data["senderId"]
        self.toId = data["targetId"]
        self.origin = []
        for message in data["origin"]:
            processedMessage = getattr(sys.modules[__name__], message["type"])()
            processedMessage.buildByDict(message)
            self.origin.append(processedMessage)
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
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
        super(At, self).__init__()
        self.at = None
        self.display = None

    def buildByArgs(self, at, display=""):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.at = at
        self.display = display
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.buildByArgs(data["target"], data["display"])
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
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
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.at = "all"
        self.display = "@全体成员"
        self.isBuilt = True

    def buildByArgs(self, *args):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.at = "all"
        self.display = "@全体成员"
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "AtAll"
        }
        return data


class Face(Message):
    """
    表情
    faceId: QQ表情编号 int
    name: QQ表情拼音 str
    注: 其二选一
    """

    def __init__(self):
        super(Face, self).__init__()
        self.faceId = None
        self.name = None

    def buildByFaceId(self, faceId):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.faceId = faceId
        self.isBuilt = True

    def buildByName(self, name):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.name = name
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.faceId = data["faceId"]
        self.name = data["name"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Face",
            "faceId": self.faceId,
            "name": self.name
        }
        return data


class Plain(Message):
    """
    纯文本
    text:消息内容 str
    """

    def __init__(self):
        super(Plain, self).__init__()
        self.text = None

    def buildByArgs(self, text):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.text = text
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.text = data["text"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Plain",
            "text": self.text
        }
        return data


class Image(Message):
    """
    图片
    imageId:图片的imageId，群图片与好友图片格式不同。不为空时将忽略url属性 str
    url:图片的URL，发送时可作网络图片的链接；接收时为腾讯图片服务器的链接，可用于图片下载 str
    path:图片的路径，发送本地图片，路径相对于 JVM 工作路径（默认是当前路径，可通过 -Duser.dir=...指定），也可传入绝对路径 str
    base64: 图片的 Base64 编码 str
    四选一
    """

    def __init__(self):
        super(Image, self).__init__()
        self.imageId = None
        self.url = None
        self.path = None
        self.base64 = None

    def buildByImageId(self, imageId):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.imageId = imageId
        self.isBuilt = True

    def buildByUrl(self, url):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.url = url
        self.isBuilt = True

    def buildByPath(self, abspath):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.path = abspath
        self.isBuilt = True

    def buildByBase64(self, base64):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.base64 = base64
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.imageId = data["imageId"]
        self.url = data["url"]
        self.path = data["path"]
        self.base64 = data["base64"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Image",
            "imageId": self.imageId,  # 群图片格式
            # "imageId": "/f8f1ab55-bf8e-4236-b55e-955848d7069f" // 好友图片格式
            "url": self.url,
            "path": self.path,
            "base64": self.base64
        }
        return data


class FlashImage(Image):
    """
    闪照
    imageId:图片的imageId，群图片与好友图片格式不同。不为空时将忽略url属性 str
    url:图片的URL，发送时可作网络图片的链接；接收时为腾讯图片服务器的链接，可用于图片下载 str
    path:图片的路径，发送本地图片，路径相对于 JVM 工作路径（默认是当前路径，可通过 -Duser.dir=...指定），也可传入绝对路径 str
    base64: 图片的 Base64 编码 str
    四选一
    """

    def __init__(self):
        super(FlashImage, self).__init__()

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "FlashImage",
            "imageId": self.imageId,  # 群图片格式
            # "imageId": "/f8f1ab55-bf8e-4236-b55e-955848d7069f" // 好友图片格式
            "url": self.url,
            "path": self.path,
            "base64": self.base64
        }
        return data


class Voice(Message):
    """
    声音
    voiceId：语音的voiceId，不为空时将忽略url属性 str
    url:语音的URL，发送时可作网络语音的链接；接收时为腾讯语音服务器的链接，可用于语音下载 str
    path:语音的路径，发送本地语音，路径相对于 JVM 工作路径（默认是当前路径，可通过 -Duser.dir=...指定），也可传入绝对路径 str
    base64:语音的 Base64 编码 str
    length:返回的语音长度, 发送消息时可以不传 int
    三个参数任选其一
    """

    def __init__(self):
        super(Voice, self).__init__()
        self.voiceId = None
        self.url = None
        self.path = None
        self.base64 = None

    def buildByVoiceId(self, voiceId):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.voiceId = voiceId
        self.isBuilt = True

    def buildByUrl(self, url):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.url = url
        self.isBuilt = True

    def buildByPath(self, abspath):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.path = abspath
        self.isBuilt = True

    def buildByBase64(self, base64):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.base64 = base64
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.voiceId = data["voiceId"]
        self.url = data["url"]
        self.path = data["path"]
        self.base64 = data["base64"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Voice",
            "voiceId": self.voiceId,  # 群图片格式
            # "imageId": "/f8f1ab55-bf8e-4236-b55e-955848d7069f" // 好友图片格式
            "url": self.url,
            "path": self.path,
            "base64": self.base64
        }
        return data


class Xml(Message):
    """
    XML消息
    xml： XML文本 str
    """

    def __init__(self):
        super(Xml, self).__init__()
        self.xml = None

    def buildByArgs(self, xml):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.xml = xml
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.xml = data["xml"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Xml",
            "xml": self.xml
        }
        return data


class Json(Message):
    """
    JSON消息
    json： Json文本 str
    """

    def __init__(self):
        super(Json, self).__init__()
        self.json = None

    def buildByArgs(self, json):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.json = json
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.json = json.loads(data["json"])
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Json",
            "json": json.dumps(self.json)
        }
        return data


class App(Message):
    """
    应用类型消息
    content： 内容 str
    """

    def __init__(self):
        super(App, self).__init__()
        self.content = None

    def buildByArgs(self, content):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.content = content
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.content = data["content"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "App",
            "content": self.content
        }
        return data


class Poke(Message):
    """
    戳一戳
    name: 戳一戳的类型 str
    其可能的值如下：
    Poke: 戳一戳
    ShowLove: 比心
    Like:点赞
    Heartbroken：心碎
    SixSixSix：666
    FangDaZhao：放大招
    ...
    """

    def __init__(self):
        super(Poke, self).__init__()
        self.name = None

    def buildByArgs(self, name):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.name = name
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.name = data["name"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Poke",
            "name": self.name
        }
        return data


class Dice(Message):
    """
    骰子
    value： 1 int
    """

    def __init__(self):
        super(Dice, self).__init__()
        self.value = None

    def buildByArgs(self, value):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.value = value
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.value = data["value"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Dice",
            "value": self.value
        }
        return data


class MarketFace(Message):
    """
    商城表情
    id: 商城表情唯一标识 int
    name:表情显示名称 str
    """

    def __init__(self):
        super(MarketFace, self).__init__()
        self.id = None
        self.name = None

    def buildByArgs(self, faceId, name):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.id = faceId
        self.name = name
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.id = data["id"]
        self.name = data["name"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "MarketFace",
            "id": self.id,
            "name": self.name
        }
        return data


class MusicShare(Message):
    """
    音乐分享
    kind： 类型 str
    title：标题 str
    summary：概括 str
    jumpUrl：跳转路径 str
    pictureUrl： 封面路径 str
    musicUrl：音源路径 str
    brief：简介 str
    """

    def __init__(self):
        super(MusicShare, self).__init__()
        self.kind = None
        self.title = None
        self.summary = None
        self.jumpUrl = None
        self.pictureUrl = None
        self.musicUrl = None
        self.brief = None

    def buildByArgs(self, kind, title, summary, jumpUrl, pictureUrl, musicUrl, brief):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.kind = kind
        self.title = title
        self.summary = summary
        self.jumpUrl = jumpUrl
        self.pictureUrl = pictureUrl
        self.musicUrl = musicUrl
        self.brief = brief
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.kind = data["kind"]
        self.title = data["title"]
        self.summary = data["summary"]
        self.jumpUrl = data["jumpUrl"]
        self.pictureUrl = data["pictureUrl"]
        self.musicUrl = data["musicUrl"]
        self.brief = data["brief"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "MusicShare",
            "kind": self.kind,
            "title": self.title,
            "summary": self.summary,
            "jumpUrl": self.jumpUrl,
            "pictureUrl": self.pictureUrl,
            "musicUrl": self.musicUrl,
            "brief": self.brief
        }
        return data


class MessageNode(Message):
    """
    消息节点
    senderId：发送人QQ号 int
    time:发送时间 int
    senderName:显示名称 str
    messageChain:消息数组 本文件中所涉及到的各种class[]（除了那些你在客户端发不了的消息节点）
    messageId: 可以只使用消息messageId，从当前对话上下文缓存中读取一条消息作为节点 int
    target:引用的上下文目标，群号、好友账号 int
    """

    def __init__(self):
        super(MessageNode, self).__init__()
        self.senderId = None
        self.time = None
        self.senderName = None
        self.messageChain = None
        self.messageId = None
        self.target = None

    def buildByMessageId(self, messageId):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.messageId = messageId
        self.isBuilt = True

    def create(self, senderId, time, senderName, messageChain):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.senderId = senderId
        self.time = time
        self.senderName = senderName
        self.messageChain = messageChain
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.senderId = data["senderId"]
        self.time = data["time"]
        self.senderName = data["senderName"]
        self.messageId = data["messageId"]
        self.target = data["target"]
        self.isBuilt = data["messageRef"]["senderId"]
        self.messageChain = data["messageChain"]
        for message in data["messageChain"]:
            processedMessage = getattr(sys.modules[__name__], message["type"])()
            processedMessage.buildByDict(message)
            self.messageChain.append(processedMessage)

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "senderId": self.senderId,
            "time": self.time,
            "senderName": self.senderName,
            "messageChain": [],
            "messageId": self.messageId,
            "messageRef": {
                "messageId": self.messageId,
                "target": self.target,
            }
        }
        for message in self.messageChain:
            data["messageChain"].append(message.generate())
        return data


class Forward(Message):
    """
    转发
    nodeList：消息节点  MessageNode[]
    """

    def __init__(self):
        super(Forward, self).__init__()
        self.nodeList = None

    def buildByArgs(self, nodeList):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.nodeList = nodeList
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.nodeList = []
        for message in data["nodeList"]:
            processedMessage = MessageNode()
            processedMessage.buildByDict(message)
            self.nodeList.append(processedMessage)
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "Forward",
            "nodeList": [message.generate() for message in self.nodeList]
        }
        return data


class File(Message):
    """
    文件
    id：文件识别id str
    name:文件名 str
    size:文件大小 int
    """

    def __init__(self):
        super(File, self).__init__()
        self.id = None
        self.name = None
        self.size = None

    def buildByArgs(self, fileId, name, size):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.id = fileId
        self.name = name
        self.size = size
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.id = data["id"]
        self.name = data["name"]
        self.size = data["size"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "File",
            "id": self.id,
            "name": self.name,
            "size": self.size
        }
        return data


class MiraiCode(Message):
    """
    MiraiCode
    code:MiraiCode str
    """

    def __init__(self):
        super(MiraiCode, self).__init__()
        self.code = None

    def buildByArgs(self, code):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.code = code
        self.isBuilt = True

    def buildByDict(self, data):
        if self.isBuilt:
            LOGGER.warning("禁止重复构建，这会让你的代码可读性变差")
            return -1
        self.code = data["code"]
        self.isBuilt = True

    def generate(self):
        if not self.isBuilt:
            raise ValueError("对象未被构造")
        data = {
            "type": "MiraiCode",
            "code": self.code
        }
        return data
