import json
import pickle

import requests

from lib.api.status_code import StatusCode, SessionException, ObjectException
from lib.types.group import BasicGroupData
from lib.types.public import QQUserData, BasicQQUserData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def getFriendList() -> list[BasicQQUserData]:
    """
    获取朋友列表
    :return: 一个承载 BasicQQUserData 的列表
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/friendList",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getFriendList失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getFriendList失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"bot的朋友:\n{json.dumps(data, indent=4)}")
    friendList = []
    for friend in data:
        friendList.append(BasicQQUserData(friend))
    return friendList


def getGroupList() -> list[BasicGroupData]:
    """
    获取群列表
    :return: 一个承载 BasicGroupData 的列表
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupList",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getGroupList失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getGroupList失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"bot加入的group:\n{json.dumps(data, indent=4)}")
    groupList = []
    for group in data:
        groupList.append(BasicGroupData(group))
    return groupList


def getBotInfo() -> QQUserData:
    """
    获取机器人信息
    :return: 一个QQUserData
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/botProfile",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
        }
    ).json()
    if "code" in result:
        code = result["code"]
        msg = result["msg"]
        if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
            LOGGER.info("请求getFriendInfo失败，是不是session不存在?")
            raise SessionException(msg)
    LOGGER.info(f"bot的信息:\n{json.dumps(result, indent=4)}")
    return QQUserData(result)


def agreeInviteRequest(eventId: int, fromId: int, groupId: int) -> None:
    """
    同意别人的入群邀请
    :param eventId: 事件ID， 从BotInvitedJoinGroupRequestEvent获得
    :param fromId: 邀请人的ID，从BotInvitedJoinGroupRequestEvent获得
    :param groupId: 群号，从BotInvitedJoinGroupRequestEvent获得
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/botInvitedJoinGroupRequestEvent",
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
        LOGGER.info("请求agreeInviteRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求agreeInviteRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求agreeInviteRequest失败，请联系开发者以修复问题？")
        exit(255)


def disagreeInviteRequest(eventId: int, fromId: int, groupId: int, reason: str) -> None:
    """
    拒绝别人的入群邀请
    :param eventId: 事件ID， 从BotInvitedJoinGroupRequestEvent获得
    :param fromId: 邀请人的ID，从BotInvitedJoinGroupRequestEvent获得
    :param groupId: 群号，从BotInvitedJoinGroupRequestEvent获得
    :param reason: 拒绝的理由
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/botInvitedJoinGroupRequestEvent",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "eventId": eventId,
            "fromId": fromId,
            "groupId": groupId,
            "operate": 1,
            "message": reason
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求disagreeInviteRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求disagreeInviteRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求disagreeInviteRequest失败，请联系开发者以修复问题？")
        exit(255)
