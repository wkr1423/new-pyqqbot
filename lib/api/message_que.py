import pickle
from lib.api.status_code import StatusCode, SessionException, ObjectException
from lib.types.public import MessageData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER
import requests


def countMessage() -> int:
    """
    获取服务器消息队列中的消息数
    :return: 消息数量
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/countMessage",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb'))
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求countMessage失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求countMessage失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"bot 收到了多少条消息: {data}")
    return data


def getMessageFromId(messageId: int, target: int) -> MessageData :
    """
    获取消息具体内容，如果消息超越缓存，可能读取不到
    :param messageId: 消息的唯一ID
    :param target: 好友的QQ号，发起群临时会话的人的QQ号，群的QQ号，三者选其一
    :return: 一个MessageData
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/messageFromId",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "messageId": messageId,
            "target": target
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getMessageFromId失败，是不是session不存在?")
        raise SessionException(msg)
    if code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info("请求getMessageFromId失败，指定对象不存在，是不是messageId和target填错了?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getMessageFromId失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"bot 信息:\n{data}")
    return MessageData(data)
