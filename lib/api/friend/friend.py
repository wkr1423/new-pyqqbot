import json
import pickle

import requests

from lib.api.status_code import StatusCode, ObjectException, SessionException
from lib.types.public import QQUserData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def getFriendInfo(QQId: int) -> QQUserData:
    """
    获取朋友信息
    :param QQId: 好友的QQ号
    :return: 一个QQUserData
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/friendProfile",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": QQId
        }
    ).json()
    if "code" in result:
        code = result["code"]
        msg = result["msg"]
        if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
            LOGGER.info("请求getFriendInfo失败，是不是session不存在?")
            raise SessionException(msg)
        elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
            LOGGER.info(f"请求getFriendInfo失败，是不是{QQId}并不是你的好友?")
            raise ObjectException(msg)
        elif code == StatusCode.WRONG_REQUEST:
            LOGGER.error("请求getFriendInfo失败，请联系开发者以修复问题？")
            exit(255)
    LOGGER.info(f"朋友({QQId})的信息:\n{json.dumps(result, indent=4)}")
    return QQUserData(result)


def deleteFriend(QQId: int) -> None:
    """
    删除好友
    :param QQId:好友的QQ号
    :return: 无返回
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/deleteFriend",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": QQId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求deleteFriend失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求deleteFriend失败，是不是无中生友({QQId})了?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求deleteFriend失败，请联系开发者以修复问题？")
        exit(255)


def agreeFriendRequest(eventId: int, fromId: int, groupId: int) -> None:
    """
    同意好友申请
    :param eventId: 事件的唯一标识，从事件NewFriendRequestEvent获得
    :param fromId: 操作者QQ号，从NewFriendRequestEvent获得
    :param groupId: 请求来自于哪个群，值可能为0，从NewFriendRequestEvent获得
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/newFriendRequestEvent",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "eventId": eventId,
            "fromId": fromId,
            "groupId": groupId,
            "operate": 0,
            "message": ""
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求agreeFriendRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求agreeFriendRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求agreeFriendRequest失败，请联系开发者以修复问题？")
        exit(255)


def disagreeFriendRequest(eventId:int, fromId:int, groupId:int, reason:str, blackList:bool=False) -> None:
    """
    拒绝好友申请
    :param eventId: 事件的唯一标识，从事件NewFriendRequestEvent获得
    :param fromId: 操作者QQ号，从NewFriendRequestEvent获得
    :param groupId: 请求来自于哪个群，值可能为0，从NewFriendRequestEvent获得
    :param reason: 拒绝的理由
    :param blackList: 是否加入黑名单，不建议使用
    :return: 无
    """
    operate = 1
    if blackList:
        operate = 2
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/newFriendRequestEvent",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "eventId": eventId,
            "fromId": fromId,
            "groupId": groupId,
            "operate": operate,
            "message": reason
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求disagreeFriendRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求disagreeFriendRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求disagreeFriendRequest失败，请联系开发者以修复问题？")
        exit(255)
