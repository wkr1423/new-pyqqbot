import json
import pickle

from lib.api.status_code import StatusCode, SessionException, ObjectException
from lib.types.public import QQUserData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER
import requests


def getUserInfo(QQId: int) ->  QQUserData:
    """
    获取QQ用户的信息
    :param QQId: 用户的QQ号
    :return: QQUserData
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/userProfile",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": QQId,
        }
    ).json()
    if "code" in result:
        code = result["code"]
        msg = result["msg"]
        if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
            LOGGER.info("请求getUserInfo失败，是不是session不存在?")
            raise SessionException(msg)
        elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
            LOGGER.info(f"请求getUserInfo失败，是不是{QQId}根本不存在?")
            raise ObjectException(msg)
        elif code == StatusCode.WRONG_REQUEST:
            LOGGER.error("请求getUserInfo失败，请联系开发者以修复问题？")
            exit(255)
    LOGGER.info(f"用户{QQId}的信息:\n{json.dumps(result, indent=4)}")
    return QQUserData(result)
