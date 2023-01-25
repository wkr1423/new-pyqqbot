
一、介绍
---------

PYQQBOT 是一个用 python 实现的、基于[MIRAI](https://github.com/mamoe/mirai)协议的 QQ 机器人，可运行在 Linux, Windows 和 Mac OSX 平台下。

依赖列表如下：
+ [mirai-api-http](https://github.com/project-mirai/mirai-api-http)
+ [MIRAI](https://github.com/mamoe/mirai)

本项目 github 地址： <https://github.com/wkr1423/new-pyqqbot>

你可以通过扩展 qqbot 来实现：

* 监控、收集 QQ 消息
* 自动消息推送
* 聊天机器人
* 通过 QQ 远程控制你的设备

二、安装方法
-------------

在 Python 2.7/3.4+ 下使用，用 pip 安装：

    pip install qqbot

或者下载 [源码](https://github.com/pandolia/qqbot/archive/master.zip) 解压后 cd 到该目录并运行： `pip install`.

三、使用方法
-------------

##### 1. 启动 QQBot

在命令行输入： **qqbot** ，即可启动一个 QQBot 。

启动过程中会自动弹出二维码图片，需要用手机 QQ 客户端扫码并授权登录。启动成功后，会将本次登录信息保存到本地文件中，下次启动时，可以输入： **qqbot -q qq号码** ，先尝试从本地文件中恢复登录信息（不需要手动扫码），只有恢复不成功或登录信息已过期时才会需要手动扫码登录。一般来说，保存的登录信息将在 2 天之后过期。

注意： Linux 下，需要系统中有 gvfs-open 或者 shotwell 命令才能自动弹出二维码图片（一般安装有 GNOME 虚拟文件系统 gvfs 的系统中都会含这两个命令之一）。 Windows10 下，需要系统中已设置了 png 图片文件的默认打开程序才能自动弹出二维码图片。

若系统无法自动弹出二维码图片，可以手动打开图片文件进行扫码，也可以将二维码显示模式设置为 邮箱模式 、 服务器模式 或 文本模式 进行扫码，详见本文档的第七节。

##### 2. 操作 QQBot

QQBot 启动后，在另一个控制台窗口使用 qq 命令操作 QQBot ，目前提供以下命令：

    1） 帮助、停机和重启命令

        qq help|stop|restart|fresh-restart


    2） 联系人查询、搜索命令
