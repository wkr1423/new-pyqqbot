import json
import pickle

import requests

from lib.api.status_code import StatusCode, SessionException, ObjectException, PermissionException
from lib.types.group import BasicGroupMemberData, GroupSettings
from lib.types.public import QQUserData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def mute(groupId: int, memberId: int, time: int) -> None:
    """
    禁言
    :param groupId:  群号
    :param memberId:  群成员的QQ号
    :param time:  禁言时长，单位为秒
    :return:  无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/mute",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
            "time": time
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求mute失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求mute失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求mute失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求mute失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})内的成员({memberId})禁言{time}秒。")


def unmute(groupId: int, memberId: int) -> None:
    """
    解除禁言
    :param groupId:  群号
    :param memberId:  群成员的QQ号
    :return:  无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/unmute",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求unmute失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求unmute失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求unmute失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求unmute失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})内的成员({memberId})解除禁言。")


def kick(groupId: int, memberId: int, message: str) -> None:
    """
    踢人
    :param groupId:  群号
    :param memberId:  群成员ID
    :param message: 踢人的原因
    :return:  无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/kick",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
            "msg": message
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求kick失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求kick失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求kick失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求kick失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})内的成员({memberId})移出群聊。")


def quitGroup(groupId: int) -> None:
    """
    退出群
    :param groupId:  群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/quit",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求quitGroup失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求quitGroup失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求quitGroup失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功退出群({groupId})。")


def muteAll(groupId: int) -> None:
    """
    全部成员禁言
    :param groupId: 群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/muteAll",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求muteAll失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求muteAll失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求muteAll失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求muteAll失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})全体禁言。")


def unmuteAll(groupId: int) -> None:
    """
    解除全部成员禁言
    :param groupId: 群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/unmuteAll",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求unmuteAll失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求unmuteAll失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求unmuteAll失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求unmuteAll失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功解除群({groupId})的全体禁言。")


def getGroupConfig(groupId: int) -> GroupSettings:
    """
    获取群的配置
    :param groupId: 群号
    :return: 一个GroupSettings
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
        }
    ).json()
    if "code" in result:
        code = result["code"]
        msg = result["msg"]
        if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
            LOGGER.info("请求getGroupConfig失败，是不是session不存在?")
            raise SessionException(msg)
        elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
            LOGGER.info(f"请求getGroupConfig失败，是不是你没加入群{groupId})?")
            raise ObjectException(msg)
        elif code == StatusCode.WRONG_REQUEST:
            LOGGER.error("请求getGroupConfig失败，请联系开发者以修复问题？")
            exit(255)
    LOGGER.info(f"成功获取群({groupId})的设置:\n{json.dumps(result, indent=4)}")
    return GroupSettings(result)


def setGroupName(groupId: int, name: str) -> None:
    """
    设置群名称
    :param groupId: 群号
    :param name: 新的群名称
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": name,
                "confessTalk": None,
                "allowMemberInvite": None,
                "autoApprove": None,
                "anonymousChat": None
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求setGroupName失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求setGroupName失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求setGroupName失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求setGroupName失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})的名字改为{name}。")


def allowConfessTalk(groupId: int) -> None:
    """
    允许坦白说
    :param groupId: 群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": None,
                "confessTalk": True,
                "allowMemberInvite": None,
                "autoApprove": None,
                "anonymousChat": None
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求allowConfessTalk失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求allowConfessTalk失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求allowConfessTalk失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求allowConfessTalk失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功允许群({groupId})成员使用坦白说。")


def disallowConfessTalk(groupId: int) -> None:
    """
    关闭坦白说
    :param groupId: 群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": None,
                "confessTalk": False,
                "allowMemberInvite": None,
                "autoApprove": None,
                "anonymousChat": None
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求disallowConfessTalk失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求disallowConfessTalk失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求disallowConfessTalk失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求disallowConfessTalk失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功禁止群({groupId})成员使用坦白说。")


def disallowMemberInvite(groupId: int) -> None:
    """
    关闭群成员邀请新成员权限
    :param groupId:  群号
    :return:  无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": None,
                "confessTalk": None,
                "allowMemberInvite": False,
                "autoApprove": None,
                "anonymousChat": None
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求disallowMemberInvite失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求disallowMemberInvite失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求disallowMemberInvite失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求disallowMemberInvite失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功禁止群({groupId})成员邀请别人入群。")


def allowMemberInvite(groupId: int) -> None:
    """
    允许群成员邀请新成员
    :param groupId: 群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": None,
                "confessTalk": None,
                "allowMemberInvite": True,
                "autoApprove": None,
                "anonymousChat": None
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求allowMemberInvite失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求allowMemberInvite失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求allowMemberInvite失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求allowMemberInvite失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功允许群({groupId})成员邀请别人入群。")


def allowAnonymousChat(groupId: int) -> None:
    """
    允许匿名聊天
    :param groupId: 群号
    :return:  无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": None,
                "confessTalk": None,
                "allowMemberInvite": None,
                "autoApprove": None,
                "anonymousChat": True
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求allowAnonymousChat失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求allowAnonymousChat失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求allowAnonymousChat失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求allowAnonymousChat失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功允许群({groupId})成员使用匿名聊天。")


def disallowAnonymousChat(groupId: int) -> None:
    """
    关闭匿名聊天
    :param groupId: 群号
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/groupConfig",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "config": {
                "name": None,
                "confessTalk": None,
                "allowMemberInvite": None,
                "autoApprove": None,
                "anonymousChat": False
            }
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求disallowAnonymousChat失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求disallowAnonymousChat失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求disallowAnonymousChat失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求disallowAnonymousChat失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功禁止群({groupId})成员使用匿名聊天。")


def setGroupAdmin(groupId: int, memberId: int) -> None:
    """
    设置群管理员
    :param groupId: 群号
    :param memberId: 要成为群管理员的群成员ID
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberAdmin",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
            "assign": True
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求setGroupAdmin失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求setGroupAdmin失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求setGroupAdmin失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求setGroupAdmin失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功将群({groupId})成员({memberId})设为管理员。")


def unsetGroupAdmin(groupId: int, memberId: int) -> None:
    """
    取消群管理员
    :param groupId: 群号
    :param memberId: 要取消的群管理员ID
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/memberAdmin",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "memberId": memberId,
            "assign": False
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求unsetGroupAdmin失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求unsetGroupAdmin失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求unsetGroupAdmin失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求unsetGroupAdmin失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功取消群({groupId})成员({memberId})的管理员权限。")


def agreeMemberAddRequest(eventId: int, fromId: int, groupId: int) -> None:
    """
    同意加群申请
    :param eventId: 事件ID，从MemberJoinRequestEvent获得
    :param fromId: 请求人的ID，从MemberJoinRequestEvent获得
    :param groupId: 群号，从MemberJoinRequestEvent获得
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/memberJoinRequestEvent",
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
        LOGGER.info("请求agreeMemberAddRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求agreeMemberAddRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求agreeMemberAddRequest失败，请联系开发者以修复问题？")
        exit(255)


def disagreeMemberAddRequest(eventId: int, fromId: int, groupId: int, reason: str, blackList: bool=False) -> None:
    """
    拒绝群加入申请
    :param eventId: 事件ID，从MemberJoinRequestEvent获得
    :param fromId: 请求人的ID，从MemberJoinRequestEvent获得
    :param groupId: 群号，从MemberJoinRequestEvent获得
    :param reason: 拒绝的理由
    :param blackList: 是否加入黑名单
    :return: 无
    """
    operate = 1
    if blackList:
        operate = 3
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/memberJoinRequestEvent",
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
        LOGGER.info("请求disagreeMemberAddRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求disagreeMemberAddRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求disagreeMemberAddRequest失败，请联系开发者以修复问题？")
        exit(255)


def ignoreMemberAddRequest(eventId: int, fromId: int, groupId: int, reason: str, blackList: bool=False) -> None:
    """
    忽略加群申请
    :param eventId: 事件ID，从MemberJoinRequestEvent获得
    :param fromId: 请求人的ID，从MemberJoinRequestEvent获得
    :param groupId: 群号，从MemberJoinRequestEvent获得
    :param reason: 忽略的理由
    :param blackList: 是否加入黑名单
    :return: 无
    """
    operate = 2
    if blackList:
        operate = 4
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/resp/memberJoinRequestEvent",
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
        LOGGER.info("请求ignoreMemberAddRequest失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求ignoreMemberAddRequest失败，是不是根本没人提交申请doge?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求ignoreMemberAddRequest失败，请联系开发者以修复问题？")
        exit(255)
