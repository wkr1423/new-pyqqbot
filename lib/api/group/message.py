import json
import pickle

import requests

from lib.api.group.member import getMemberList
from lib.api.status_code import StatusCode, SessionException, ObjectException, PermissionException
from lib.message_types import Message, Plain, At, AtAll, Json
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER, CRAZY_ATALL, MAX_ATALL_LENGTH


def sendGroupMessage(groupId, messageChain: list[Message], quote=None) -> None | int | list[int]:
    processedMessage = []
    for messages in messageChain:
        if isinstance(messages, Message) and type(messages) != Message:
            processedMessage.append(messages.generate())
        else:
            return None
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/sendGroupMessage",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "messageChain": processedMessage,
            "quote": quote
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    LOGGER.debug(msg)
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求sendGroupMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求sendGroupMessage失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求sendGroupMessage失败，请联系开发者以修复问题？")
        exit(255)
    elif msg.find("AT_ALL_LIMITED") != -1 or code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求sendGroupMessage失败，不能发送AtAll了{groupId}?")
        LOGGER.info(f"是否开启了疯狂atall模式：{CRAZY_ATALL}")
        crazyAtAll(groupId, messageChain, quote, CRAZY_ATALL)
        raise ObjectException(msg)
    LOGGER.info(f"成功向群({groupId})信息:\n{json.dumps(processedMessage, indent=4)}")
    return result["messageId"]


def crazyAtAll(groupId, messageChain, quote, areYouSure=False):
    if areYouSure:
        messageIds = []
        messages = Plain()
        messages.buildByArgs("===全体成员===")
        messageIds.append(sendGroupMessage(groupId, [messages]))
        members = getMemberList(groupId)
        messages = []
        for i in range(len(members)):
            at = At()
            at.buildByArgs(members[i].qq)
            messages.append(at)
            if i % MAX_ATALL_LENGTH == MAX_ATALL_LENGTH - 1:
                LOGGER.debug(messages)
                messageIds.append(sendGroupMessage(groupId, messages))
                messages = []
        if len(messages) != 0:
            messageIds.append(sendGroupMessage(groupId, messages))
            messages = []
        for message in messageChain:
            if type(message) != AtAll:
                messages.append(message)
        messageIds.append(sendGroupMessage(groupId, messages, quote))
        return messageIds


def sendFakeRedPocketToGroup(groupId):
    msg = Json()
    msg.buildByArgs({
        "app": "com.tencent.gxhServiceIntelligentTip",
        "desc": "xyz",
        "view": "gxhServiceIntelligentTip",
        "ver": "1.0.0.1",
        "prompt": "[QQ红包]你收到一个专属红包，请在新版手机QQ查看。",
        "appID": "",
        "sourceName": "",
        "actionData": "",
        "actionData_A": "",
        "sourceUrl": "",
        "meta": {
            "gxhServiceIntelligentTip": {
                "action": "",
                "appid": "gxhServiceIntelligentTip",
                "bgImg": "http:\/\/r.photo.store.qq.com\/psc?\/V50sYhPJ4MptGg1ssqwo0ZF6HX31705y\/ruAMsa53pVQWN7FLK88i5gUE6oWZ1hyNWXpQh.nyvv8UW*OoOjdlLmRf4Yow7SmiSdK9kqbhf0lKCG9l7.YRlfexLbdo.CXqCcRW9RHVYGU!\/o"
            }
        },
        "config": {
            "ctime": 1674311381,
            "height": 220,
            "round": 1,
            "token": "09fa6b848c4afa23ab8fd5d69c3249f2",
            "type": "normal",
            "width": 150
        },
        "text": "",
        'extraApps': [],
        "sourceAd": "",
        "extra": "{\"app_type\":1,\"appid\":100951776,\"msg_seq\":1674311380207513,\"uin\":1726237584}"
    })
    sendGroupMessage(groupId, [msg])


def setEssence(groupId, messageId):
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/setEssence",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "messageId": messageId
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求setEssence失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求setEssence失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求setEssence失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求setEssence失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})的消息({messageId})设为精华消息。")


def nudgeGroupMember(groupId, QQId) -> None:
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/sendNudge",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": QQId,
            "subject": groupId,
            "kind": "Group"
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求nudgeGroupMember失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求nudgeGroupMember失败，是不是kind值填错了?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求nudgeGroupMember失败，请联系开发者以修复问题？")
        exit(255)


def recallGroupMessage(groupId, messageId) -> None:
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/recall",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "messageId": messageId,
            "target": groupId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求recallGroupMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求recallGroupMessage失败，是不是没有这条消息({messageId} from {groupId})啊?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求recallGroupMessage失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功撤回信息({messageId} from {groupId})。")