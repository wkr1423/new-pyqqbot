import json
import pickle
from typing import List

from lib.api.status_code import StatusCode, SessionException, ObjectException, PermissionException
from lib.message_types import Image
from lib.types.group import GroupNoticeData
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def getNoticeList(groupId: int) -> list[GroupNoticeData]:
    """
    获得公告列表
    :param groupId: 群号
    :return: GroupNoticeData的列表
    """
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/anno/list",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": groupId,
            "offset": None,
            "size": None,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getNoticeList失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求getNoticeList失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getNoticeList失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"群({groupId})公告:\n{json.dumps(data, indent=4)}")
    notices = []
    for notice in data:
        notices.append(GroupNoticeData(notice))
    return notices


def publishNotice(groupId: int, content: str, pinned: bool = False, sendToNewMember: bool = False, showEditCard: bool = False, showPopup: bool = False,
                  requireConfirmation: bool = False, image: Image | None = None) -> GroupNoticeData:
    """
    发布公告
    :param groupId: 群号
    :param content: 公告内容
    :param pinned: 是否置顶
    :param sendToNewMember: 是否发送给新成员
    :param showEditCard: 是否引导新成员修改昵称
    :param showPopup: 是否弹窗显示
    :param requireConfirmation: 是否需要确认
    :param image: 可选Image
    :return: GroupNoticeData
    """
    if image is None:
        imageUrl = imagePath = imageBase64 = None
    elif not image.isBuilt and image.imageId is not None:
        LOGGER.info("图片未被初始化，或初始化方式不能在群公告处使用")
        raise ValueError("图片未被初始化，或初始化方式不能在群公告处使用")
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/anno/publish",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "target": groupId,
            "content": content,
            "pinned": pinned,
            "sendToNewMember": sendToNewMember,
            "showEditCard": showEditCard,
            "showPopup": showPopup,
            "requireConfirmation": requireConfirmation,
            "imageUrl": image.url,
            "imagePath": image.path,
            "imageBase64": image.base64
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求publishNotice失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求publishNotice失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求publishNotice失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求publishNotice失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(
        f"发布群({groupId})公告:\n"
        f"内容:{content}\n"
        f"\t图片:\n" if image is not None else ""
        f"\t\t公告图片url:{image.url}\n" if image is not None and image.url is not None else ""
        f"\t\t公告图片本地路径:{image.path}\n" if image is not None and image.path is not None else ""
        f"\t\t公告图片base64编码:{image.base64}\n" if image is not None and image.base64 is not None else ""
        f"设置:\n"
        f"\t是否置顶:{pinned}\n"
        f"\t是否发送给新成员:{sendToNewMember}\n"
        f"\t是否显示群成员修改群名片的引导:{showEditCard}\n"
        f"\t是否自动弹出:{showPopup}\n"
        f"\t是否需要群成员确认:{requireConfirmation}\n"
        f"结果:\n"
        f"{json.dumps(data, indent=4)}"
    )
    return GroupNoticeData(data)


def deleteNotice(groupId: int, noticeId: int) -> None:
    """
    删除公告
    :param groupId: 群号
    :param noticeId:  公告ID
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/anno/delete",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": groupId,
            "fid": noticeId,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求deleteNotice失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求deleteNotice失败，是不是你没加入群{groupId})?")
        raise ObjectException(msg)
    elif code == StatusCode.NO_PERMISSION:
        LOGGER.info(f"请求deleteNotice失败，是不是你不是群{groupId})的管理员?")
        raise PermissionException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求deleteNotice失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"成功删除群({groupId})公告({noticeId})。")
