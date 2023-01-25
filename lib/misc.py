import hashlib
import inspect
import os.path
import threading
import time

from settings import PATH_BLACKLIST, LOGGER


def getClasses(arg):
    # 获取文件下所有的class
    classes = inspect.getmembers(arg, inspect.isclass)
    LOGGER.debug(classes)
    return classes


def removeMiscPath(paths: list) -> list:
    """
    移除给出文件列表中的黑名单内容
    :param paths: 路径列表
    :return: paths
    """
    for blockedPath in PATH_BLACKLIST:
        while paths.count(blockedPath):
            paths.remove(blockedPath)
    # LOGGER.info(paths)
    return paths


def removeDirs(basedir: str, paths: list):
    # 移除路径中的所有文件夹
    for pathId in range(len(paths)):
        if os.path.isdir(os.path.join(basedir, paths[pathId])):
            paths[pathId] = ""
    while paths.count("") != 0:
        paths.remove("")
    # LOGGER.info(paths)
    return paths


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def getFileMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        md5 = md5obj.hexdigest()
        return md5


def startFunc(func, work, args):
    thread = threading.Thread(target=func, args=args)
    work.append(thread)
    LOGGER.debug(f"work {str(thread)} started")
    thread.start()
    while thread.is_alive():
        time.sleep(1)
    work.remove(thread)
