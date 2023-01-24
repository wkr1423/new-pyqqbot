import json
import mimetypes
import os.path
import pickle
import requests

from lib.api.status_code import StatusCode, SessionException, ObjectException
from lib.message_types import Message, Plain, At, AtAll, Json
from lib.types.file import FileInfo, FolderInfo
from lib.types.group import BasicGroupData, BasicGroupMemberData
from lib.types.public import QQUserData
from lib.types.upload import UploadImage
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER, CRAZY_ATALL, MAX_ATALL_LENGTH


def sendTempMessage(groupId, QQId, messageChain: list[Message], ) -> int:
    """
    发起群临时会话
    :param groupId: 群号
    :param QQId: 发起会话的目标人的QQ号
    :param messageChain: 消息，内容全是构造完成的消息类型
    :return: 消息的唯一ID
    """
    processedMessage = []
    for message in messageChain:
        if isinstance(message, Message) and type(message) != Message:
            processedMessage.append(message.generate())
        else:
            LOGGER.error("请求sendTempMessage失败，messageChain内的消息类型非支持的消息类型？")
            raise ValueError("messageChain内的消息类型非支持的消息类型")
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/sendTempMessage",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "group": groupId,
            "qq": QQId,
            "messageChain": processedMessage
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求sendTempMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求sendTempMessage失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求sendTempMessage失败，请联系开发者以修复问题？")
        exit(255)
    elif msg != "success":
        LOGGER.error("请求sendTempMessage失败，未知的不成功因素，请迅速向开发者发送此信息以获取支持：\n发送好友消息失败了, " + msg)
        exit(255)
    LOGGER.info(f"成功向群({groupId})的成员({QQId})信息:\n{json.dumps(processedMessage, indent=4)}")
    return result["messageId"]


def recallTempMessage(QQId, messageId) -> None:
    """
    撤回群临时会话的消息
    :param QQId: 发起会话的目标人的QQ号
    :param messageId: 消息唯一的ID
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
        LOGGER.info("请求recallTempMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求recallTempMessage失败，是不是没有这条消息({messageId} from {QQId})啊?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求recallTempMessage失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功撤回信息({messageId} from {QQId})。")
