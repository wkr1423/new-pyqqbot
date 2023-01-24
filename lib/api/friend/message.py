import json
import pickle

import requests

from lib.api.status_code import StatusCode, ObjectException, SessionException
from lib.message_types import Message
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def sendFriendMessage(QQId:int, messageChain: list[Message]) -> int:
    """
    发送好友信息
    :param QQId: 好友的QQ号
    :param messageChain: 消息，内容全是构造完成的消息类型
    :return: 消息的ID
    """
    processedMessage = []
    for message in messageChain:
        if isinstance(message, Message) and type(message) != Message:
            processedMessage.append(message.generate())
        else:
            LOGGER.error("请求sendFriendMessage失败，messageChain内的消息类型非支持的消息类型？")
            raise ValueError("messageChain内的消息类型非支持的消息类型")
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/sendFriendMessage",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": QQId,
            "messageChain": processedMessage
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求sendFriendMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求sendFriendMessage失败，是不是{QQId}并不是你的好友?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求sendFriendMessage失败，请联系开发者以修复问题？")
        exit(255)
    elif msg != "success":
        LOGGER.error("请求sendFriendMessage失败，未知的不成功因素，请迅速向开发者发送此信息以获取支持：\n发送好友消息失败了, " + msg)
        exit(255)
    LOGGER.info(f"成功向朋友({QQId})信息:\n{json.dumps(processedMessage, indent=4)}")
    return result["messageId"]


def nudgeFriend(QQId:int) -> None:
    """
    戳一戳
    :param QQId:好友QQ号
    :return:无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/sendNudge",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": QQId,
            "subject": QQId,
            "kind": "Friend"
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求nudgeFriend失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求nudgeFriend失败，是不是kind值填错了?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求nudgeFriend失败，请联系开发者以修复问题？")
        exit(255)


def recallFriendMessage(QQId:int, messageId:int) -> None:
    """
    撤回好友消息
    :param QQId:好友QQ号
    :param messageId: 消息唯一ID
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/recall",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "messageId": messageId,
            "target": QQId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求recallFriendMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求recallFriendMessage失败，是不是没有这条消息({messageId} from {QQId})啊?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求recallFriendMessage失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功撤回信息({messageId} from {QQId})。")