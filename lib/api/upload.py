# uploadImage
import json
import mimetypes
import os
import pickle

from lib.api.status_code import ObjectException
from lib.types.upload import UploadImage
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def uploadImageAsGroup(abspath: str) -> UploadImage:
    """
    上传图片，返回group格式的ID
    :param abspath:  绝对路径
    :return: UploadImage
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/uploadImage",
        data={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "type": "group"
        },
        files={
            "img": (os.path.split(abspath)[1], open(abspath, "rb"), mimetypes.guess_type(abspath)[0])
        }
    )
    if result.text == "":
        LOGGER.info("请求uploadImageToGroup失败，是不是路径写错了?")
        raise ObjectException("服务器没有回应")
    result = result.json()
    LOGGER.info(f"将图片{repr(abspath)}以群的格式上传:\n{json.dumps(result, indent=4)}")
    return UploadImage(result)


def uploadImageAsFriend(abspath: str) -> UploadImage:
    """
    上传图片，返回朋友格式的图片ID
    :param abspath: 绝对路径
    :return: UploadImage
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/uploadImage",
        data={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "type": "friend"
        },
        files={
            "img": (os.path.split(abspath)[1], open(abspath, "rb"), mimetypes.guess_type(abspath)[0])
        }
    )
    if result.text == "":
        LOGGER.info("请求uploadImageAsFriend失败，是不是路径写错了?")
        raise ObjectException("服务器没有回应")
    result = result.json()
    LOGGER.info(f"将图片{repr(abspath)}以朋友的格式上传:\n{json.dumps(result, indent=4)}")
    return UploadImage(result)


def uploadImageAsTemp(abspath: str) -> UploadImage:
    """
    上传图片，返回群临时会话类型的图片ID
    :param abspath: 绝对路径
    :return: UploadImage
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/uploadImage",
        data={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "type": "temp"
        },
        files={
            "img": (os.path.split(abspath)[1], open(abspath, "rb"), mimetypes.guess_type(abspath)[0])
        }
    )
    if result.text == "":
        LOGGER.info("请求uploadImageAsTemp失败，是不是路径写错了?")
        raise ObjectException("服务器没有回应")
    result = result.json()
    LOGGER.info(f"将图片{repr(abspath)}以的格式上传:\n{json.dumps(result, indent=4)}")
    return UploadImage(result)


def uploadVoiceAsGroup(abspath: str) -> UploadImage:
    """
    上传录音，返回群格式的录音ID
    :param abspath: 绝对路径
    :return: UploadImage
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/uploadVoice",
        data={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "type": "group"
        },
        files={
            "voice": (os.path.split(abspath)[1], open(abspath, "rb"), mimetypes.guess_type(abspath)[0])
        }
    )
    if result.text == "":
        LOGGER.info("请求uploadVoiceAsGroup失败，是不是路径写错了?")
        raise ObjectException("服务器没有回应")
    result = result.json()
    LOGGER.info(f"将图片{repr(abspath)}以群的格式上传:\n{json.dumps(result, indent=4)}")
    return UploadImage(result)
