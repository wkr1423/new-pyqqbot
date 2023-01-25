class StatusCode:
    """
    0	正常
    1	错误的verify key
    2	指定的Bot不存在
    3	Session失效或不存在
    4	Session未认证(未激活)
    5	发送消息目标不存在(指定对象不存在)
    6	指定文件不存在，出现于发送本地图片
    10	无操作权限，指Bot没有对应操作的限权
    20	Bot被禁言，指Bot当前无法向指定群发送消息
    30	消息过长
    400	错误的访问，如参数错误等
    """
    OK = 0
    WRONG_VERIFY_KEY = 1
    BOT_DOES_NOT_EXIST = 2
    WRONG_SESSION = 3
    SESSION_DOES_NOT_EXIST = 4
    OBJECT_DOES_NOT_EXIST = 5
    FILE_DOES_NOT_EXIST = 6
    NO_PERMISSION = 10
    BOT_IS_MUTED = 20
    MESSAGE_IS_TOO_LONG = 30
    WRONG_REQUEST = 400


class VerifyException(Exception):
    """
    关于验证的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class BotException(Exception):
    """
    关于Bot的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SessionException(Exception):
    """
    关于会话的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ObjectException(Exception):
    """
    关于传值的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileException(Exception):
    """
    关于文件的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PermissionException(Exception):
    """
    关于权限的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class MuteException(Exception):
    """
    关于Bot禁言的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class LengthException(Exception):
    """
    关于消息长度的异常
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
