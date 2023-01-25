import json
import pickle

import requests

from lib.api.status_code import StatusCode, SessionException, ObjectException, PermissionException
from lib.types.group import BasicGroupMemberData
from lib.types.public import QQUserData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def getMemberList(groupId: int) -> None | list[BasicGroupMemberData]:
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberList",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getMemberList失败，是不是session不存在?")
        raise SessionException(msg)
    if code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info("请求getMemberList失败，是不是q群不存在?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getMemberList失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"群号为{groupId}的群的成员:\n{json.dumps(data, indent=4)}")
    memberList = []
    for member in data:
        memberList.append(BasicGroupMemberData(member))
    return memberList


def getGroupMemberInfo(groupId, QQId) -> None | QQUserData:
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberProfile",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": QQId
        }
    ).json()
    if "code" in result:
        code = result["code"]
        msg = result["msg"]
        if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
            LOGGER.info("请求getGroupMemberInfo失败，是不是session不存在?")
            raise SessionException(msg)
        elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
            LOGGER.info(f"请求getGroupMemberInfo失败，是不是群({groupId})不存在或用户({QQId})并不在群内?")
            raise ObjectException(msg)
        elif code == StatusCode.WRONG_REQUEST:
            LOGGER.error("请求getGroupMemberInfo失败，请联系开发者以修复问题？")
            exit(255)
    LOGGER.info(f"群{groupId}的成员{QQId}的信息:\n{json.dumps(result, indent=4)}")
    return QQUserData(result)


def getMemberConfig(groupId, memberId):
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberInfo",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId
        }
    ).json()
    if "code" in result:
        code = result["code"]
        msg = result["msg"]
        if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
            LOGGER.info("请求getMemberConfig失败，是不是session不存在?")
            raise SessionException(msg)
        elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
            LOGGER.info(f"请求getMemberConfig失败，是不是你没加入群({groupId})?")
            raise ObjectException(msg)
        elif code == StatusCode.WRONG_REQUEST:
            LOGGER.error("请求getMemberConfig失败，请联系开发者以修复问题？")
            exit(255)
    LOGGER.info(f"成功获取群({groupId})成员({memberId})的设置:\n{json.dumps(result, indent=4)}")
    return BasicGroupMemberData(result)


def setMemberName(groupId, memberId, name):
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberInfo",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
            "info": {
                "name": name,
                "specialTitle": None
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求setMemberName失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求setMemberName失败，是不是你没加入群({groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求setMemberName失败，是不是你不是群({groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求setName失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})成员({memberId})的名字改为{name}。")


def setMemberSpecialTitle(groupId, memberId, specialTitle):
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberInfo",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
            "info": {
                "name": None,
                "specialTitle": specialTitle
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求setMemberSpecialTitle失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求setMemberSpecialTitle失败，是不是你没加入群({groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求setMemberSpecialTitle失败，是不是你不是群({groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求setMemberSpecialTitle失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})成员({memberId})的头衔改为{specialTitle}。")
