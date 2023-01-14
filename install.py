import os
import platform
import logging
import sys

# get information
arch = platform.architecture()[0]  # 64bit or 32bit
system = platform.system()  # Windows or Linux or Darwin
machine = platform.machine()  # (x86_64 or AMD64) or aarch64
branch = platform.freedesktop_os_release() if system == "Linux" else None
branch = branch["ID_LIKE"] if branch is not None and "ID_LIKE" in branch else None  # debian or rhel fedora
logging.info(f"computer info")
logging.info(f"bit: {arch}")
logging.info(f"system type: {system}")
logging.info(f"arch: {machine}")
logging.info(f"branch: {branch}")

# get executable path
executable = sys.executable
path = os.path.abspath(os.path.dirname(__file__))

# dependencies
dependencies = ["requests", "websockets"]


# create venv
def create_venv():
    global executable
    logging.info("正在安装虚拟环境")
    if os.system(f"{executable} -m venv venv") != 0:
        logging.critical("请安装venv这个包，以启用虚拟环境")
        exit(256)
    if system == "Linux" or system == "Darwin":
        executable = os.path.join(path, "venv/bin/python")
    else:
        executable = os.path.join(path, "venv/Scripts/python.exe")
    logging.info("完成")


# install dependencies
def install_packages():
    logging.info("正在安装依赖")
    if os.system(f"{executable} -m pip") != 0:
        logging.critical("请安装pip这个包，以启用虚拟环境")
        exit(256)
    for dependency in dependencies:
        logging.info(f"正在安装{dependency}")
        result = os.system(f"{executable} -m pip install {dependency}")
        while result != 0:
            logging.info(f"安装失败，正在重试")
            result = os.system(f"{executable} -m pip install {dependency}")
        logging.info(f"安装完毕")
    logging.info("完成")


# install bot
def install_bot():
    import requests
    requests.get("https://api.github.com/repos/iTXTech/mcl-installer/releases/latest", verify=False).json()
