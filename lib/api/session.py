import json
import pickle

import requests

from lib.api.status_code import StatusCode
from lib.types.friend import BasicQQUserData
from settings import HTTP_PORT, HTTP_HOST, VERIFY_KEY, LOGGER, QQ_ID, PATH, SESSION_PATH


def verify():
    """
    验证并且获取会话
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/verify",
        json={
            "verifyKey": VERIFY_KEY
        }
    ).json()
    code = result["code"]
    if code == StatusCode.WRONG_VERIFY_KEY or code == StatusCode.WRONG_REQUEST:
        LOGGER.error("认证失败，请联系开发者以修复问题")
        exit(255)
    session = result["session"]
    bind(session)


def bind(session):
    """
    将会话和Bot的QQ号绑定
    :param session: 会话
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/bind",
        json={
            "sessionKey": session,
            "qq": QQ_ID
        }
    ).json()
    code = result["code"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.error("无法绑定qq号，是否进行了验证?")
        exit(255)
    elif code == StatusCode.BOT_DOES_NOT_EXIST:
        LOGGER.error("无法绑定qq号，bot是否被登陆了？可以使用autologin进行自动登录。")
        exit(255)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("无法绑定qq号，请联系开发者以修复问题？")
        exit(255)
    pickle.dump(session, open(SESSION_PATH, 'wb'))
    LOGGER.info("http api 初始化完成")


def getSessionInfo() -> BasicQQUserData:
    """
    获取会话信息
    :return: BasicQQUserData
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/sessionInfo",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb'))
        }
    ).json()
    code = result["code"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getSessionInfo失败，是不是session不存在?")
        return None
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getSessionInfo失败，请联系开发者以修复问题？")
        exit(255)
    qq = result["data"]["qq"]
    LOGGER.info("bot 基本信息:\n" + json.dumps(qq))
    return BasicQQUserData(qq)
