import json
import mimetypes
import os.path
import pickle

import requests

from lib.api.status_code import StatusCode, SessionException, ObjectException
from lib.types.file import FileInfo, FolderInfo
from settings import HTTP_HOST, HTTP_PORT, SESSION_PATH, LOGGER


def getFileList(folderId: str, groupId: int) -> dict[str, list[FileInfo] | list[FolderInfo]]:
    """
    获取群文件夹下的文件列表，如果folderId为空，则返回群根目录下的文件列表
    :param folderId: 文件夹的ID
    :param groupId: 群号
    :return: 一个含有files和folders的字典,files是一个全是FileInfo的列表，folders是一个全是FolderInfo的列表
    """
    if folderId == "/":
        folderId = ""
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/list",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": folderId,
            "path": None,
            "target": groupId,
            "group": groupId,
            "qq": None,
            "withDownloadInfo": True,
            "offset": None,
            "size": None
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getFileList失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求getFileList失败，是不是你没加入群{groupId}或根本没有这个文件夹({folderId})?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getFileList失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"群({groupId})文件夹({folderId})下的文件:\n{json.dumps(data, indent=4)}")
    files = []
    folders = []
    for file in data:
        if file["isFile"]:
            files.append(FileInfo(file))
            continue
        folders.append(FolderInfo(file))
    return {
        "files": files,
        "folders": folders
    }


def getFileInfo(fileId: str, groupId: int) -> FileInfo | FolderInfo:
    """
    获取文件信息
    :param fileId: 文件的唯一ID
    :param groupId: 群号
    :return: 返回FileInfo或者FolderInfo
    """
    if fileId == "/":
        fileId = ""
    result = requests.get(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/info",
        params={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": fileId,
            "path": None,
            "target": groupId,
            "group": groupId,
            "qq": None,
            "withDownloadInfo": True
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求getFileInfo失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求getFileInfo失败，是不是你没加入群{groupId}或根本没有这个文件({fileId})?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求getFileInfo失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"群({groupId})文件夹({fileId})下的文件:\n{json.dumps(data, indent=4)}")
    if data["isFile"]:
        return FileInfo(data)
    return FolderInfo(data)


def makeDir(dirName: str, groupId: int) -> FolderInfo:
    """
    创建群文件夹
    :param dirName: 文件夹名称
    :param groupId:  群号
    :return: FolderInfo
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/mkdir",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": "",
            "path": None,
            "target": groupId,
            "group": groupId,
            "qq": None,
            "directoryName": dirName
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求makeDir失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求makeDir失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求makeDir失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"群({groupId})中新建文件夹{dirName}:\n{json.dumps(data, indent=4)}")
    return FolderInfo(data)


def deleteFile(groupId: int, fileId: str) -> None:
    """
    删除文件，似乎不能删除文件夹
    :param groupId: 群号
    :param fileId: 文件唯一ID
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/delete",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": fileId,
            "path": None,
            "target": groupId,
            "group": groupId,
            "qq": None
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求deleteFile失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求deleteFile失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求deleteFile失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"删除群({groupId})中的文件({fileId})")


def moveFile(groupId: int, fileId: str, folderId: str) -> None:
    """
    移动文件到其它文件夹
    :param groupId: 群号
    :param fileId: 文件唯一ID
    :param folderId: 要移动到的文件夹ID，如果为空，则放在根目录
    :return: 无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/move",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": fileId,
            "path": None,
            "target": groupId,
            "group": groupId,
            "qq": None,
            "moveTo": folderId,
            "moveToPath": None
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求moveFile失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求moveFile失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求moveFile失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"将群({groupId})中的文件({fileId})移动到文件夹({folderId})")


def renameFile(groupId: int, fileId: str, name: str) -> None:
    """
    重命名文件或文件夹
    :param groupId:  群号
    :param fileId:  文件或文件夹ID
    :param name:  文件或文件夹新的名称
    :return:  无
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/rename",
        json={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "id": fileId,
            "path": None,
            "target": groupId,
            "group": groupId,
            "qq": None,
            "renameTo": name,
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求renameFile失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求renameFile失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求renameFile失败，请联系开发者以修复问题？")
        exit(255)
    LOGGER.info(f"将群({groupId})中的文件({fileId})重命名为{name}")


def uploadFile(groupId: int, abspath: str, folderId: str) -> FileInfo | FolderInfo:
    """
    上传文件
    :param groupId: 群号
    :param abspath:  绝对路径
    :param folderId:  文件夹ID
    :return:  FileInfo 或 FolderInfo
    """
    result = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/file/upload",
        data={
            "sessionKey": pickle.load(open(SESSION_PATH, 'rb')),
            "type": "group",
            "target": groupId,
            "path": folderId
        },
        files={
            "file": (os.path.split(abspath)[1], open(abspath, "rb"), mimetypes.guess_type(abspath)[0])
        }
    ).json()
    code = result["code"]
    msg = result["msg"]
    if code == StatusCode.WRONG_SESSION or code == StatusCode.SESSION_DOES_NOT_EXIST:
        LOGGER.info("请求uploadFile失败，是不是session不存在?")
        raise SessionException(msg)
    elif code == StatusCode.OBJECT_DOES_NOT_EXIST:
        LOGGER.info(f"请求uploadFile失败，是不是你没加入群{groupId}?")
        raise ObjectException(msg)
    elif code == StatusCode.WRONG_REQUEST:
        LOGGER.error("请求uploadFile失败，请联系开发者以修复问题？")
        exit(255)
    data = result["data"]
    LOGGER.info(f"将文件{repr(abspath)}上传到群({groupId})文件夹({folderId})中:\n{json.dumps(data, indent=4)}")
    if data["isFile"]:
        return FileInfo(data)
    return FolderInfo(data)
