import hashlib
import inspect
import os.path
import ctypes
from settings import PATH_BLACKLIST


def getClasses(arg):
    classes = []
    classMembers = inspect.getmembers(arg, inspect.isclass)
    for (name, cls) in classMembers:
        classes.append((cls, name))
    return classes


def removeMiscPath(paths: list):
    for blockedPath in PATH_BLACKLIST:
        while paths.count(blockedPath):
            paths.remove(blockedPath)
    # LOGGER.info(paths)
    return paths


def removeDirs(basedir: str, paths: list):
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


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stopThread(thread):
    _async_raise(thread.ident, SystemExit)


def getFileMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        md5 = md5obj.hexdigest()
        return md5
