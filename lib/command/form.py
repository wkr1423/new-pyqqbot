import re


class BaseField:
    """
    name: 判断时选取值的key
    isRequired: 是否为必须填的内容
    onlyOne：是否只取1个值，开启则取第一个输入的值
    default: 默认值，如果没选的时候取用这个值，当然优先级比isRequired高
    description: 与help这个命令挂钩，你只需要写这个参数是拿来干什么的
    """

    def __init__(self, name, isRequired, onlyOne, default, description, valueType):
        self.error = ""
        self.validators = []  # 验证器列表
        self.value = None  # 待验证的值
        self.name = name  # 验证的key
        self.isRequired = isRequired  # 是否是必须的
        self.onlyOne = onlyOne  # 只允许有1个值
        self.default = default  # 默认值
        self.description = f"{name}: {description} 类型:{valueType}" + " 必填" if isRequired else "" + " 只写一次" if onlyOne else ""  # 文档

    def setValue(self, value):
        # 做验证时使用
        self.value = value

    def validate(self):
        # 内建验证函数
        if not self.validNone():
            return None, self.error
        if not self.validType():
            return None, self.error
        for validator in self.validators:
            if not validator():
                return None, self.error
        return self.value

    def validNone(self):
        # 判空，一般无需更改
        if self.value == "":
            self.error = f"您输入的参数{self.name}是空的！这是不允许的。"
            return False
        return True

    def validType(self):
        # 验证类型
        try:
            ...
            return True
        except ValueError:
            return False


class IntField(BaseField):
    """
    参数为int值
    返回一定是个int
    maxValue，minValue规定大小
    """

    def __init__(self, name, description, isRequired=True, onlyOne=False, default=None, maxValue=None, minValue=None):
        super(IntField, self).__init__(name, isRequired, onlyOne, default, description, "整数")
        self.maxValue = maxValue
        self.minValue = minValue
        self.validators.append(self.validMinValue)
        self.validators.append(self.validMaxValue)

    def validMaxValue(self):
        """验证最大值"""
        if self.maxValue is None:
            return True
        if self.value > self.maxValue:
            self.error = f"您输入的参数{self.name}的值超过最大值喽！这是不允许的。"
            return False
        return True

    def validMinValue(self):
        """验证最小值"""
        if self.minValue is None:
            return True
        if self.value < self.minValue:
            self.error = f"您输入的参数{self.name}的值小于最小值喽！这是不允许的。"
            return False
        return True

    def validType(self):
        """验证类型，这里用异常处理是因为我不会用re (^v^)"""
        try:
            self.value = int(self.value)
            return True
        except ValueError:
            self.error = f"您输入的参数{self.name}的值并非整数！这是不允许的。"
            return False


class FloatField(BaseField):
    """
    参数为float值
    返回一定是个float
    maxValue，minValue规定大小
    """

    def __init__(self, name, description, isRequired=True, onlyOne=False, default=None, maxValue=None, minValue=None):
        super(FloatField, self).__init__(name, isRequired, onlyOne, default, description, "小数")
        self.maxValue = maxValue
        self.minValue = minValue
        self.validators.append(self.validMinValue)
        self.validators.append(self.validMaxValue)

    def validMaxValue(self):
        """验证最大值"""
        if self.maxValue is None:
            return True
        if self.value > self.maxValue:
            self.error = f"您输入的参数{self.name}的值超过最大值喽！这是不允许的。"
            return False
        return True

    def validMinValue(self):
        """验证最小值"""
        if self.minValue is None:
            return True
        if self.value < self.minValue:
            self.error = f"您输入的参数{self.name}的值小于最小值喽！这是不允许的。"
            return False
        return True

    def validType(self):
        """验证类型，这里用异常处理是因为我不会用re (^v^)"""
        try:
            self.value = float(self.value)
            return True
        except ValueError:
            self.error = f"您输入的参数{self.name}的值并非小数（其实整数也可以）！这是不允许的。"
            return False


class StrField(BaseField):
    """
    参数为str值
    返回一定是个str
    maxValue，minValue规定大小
    charRange，从string文件中找，防止一些奇怪的话，传入字符串，比如只有英文。可以使用string库，但不建议使用本参数，会大大影响效率
    """

    def __init__(self, name, description, isRequired=True, onlyOne=False, default=None, maxLength=None, minLength=None,
                 charRange=None):
        super(StrField, self).__init__(name, isRequired, onlyOne, default, description, "字符串类型")
        self.maxLength = maxLength
        self.minLength = minLength
        self.charRange = charRange  # 字符范围
        self.validators.append(self.validMinLength)
        self.validators.append(self.validMaxLength)
        self.validators.append(self.validCharRange)

    def validMaxLength(self):
        """验证最大值"""
        if self.maxLength is None:
            return True
        if len(self.value) > self.maxLength:
            self.error = f"您输入的参数{self.name}的值太长啦♂！这是不允许的。"
            return False
        return True

    def validMinLength(self):
        """验证最小值"""
        if self.minLength is None:
            return True
        if len(self.value) < self.minLength:
            self.error = f"您输入的参数{self.name}的值太短啦♂！这是不允许的。"
            return False
        return True

    def validCharRange(self):
        """验证字符范围"""
        if self.charRange is None:
            return True
        for char in self.value:
            if char not in self.charRange:
                self.error = f"您输入的参数{self.name}的值不在规定范围内！这是不允许的。"
                return False
        return True

    def validNone(self):
        return True

    def validType(self):
        """传回来的都是str啦 (^v^)"""
        return True


class ChoiceField(BaseField):
    """
    参数为str值
    返回一定是个str
    本处的onlyOne会更加严格
    ignoreCase是否忽略大小写
    """

    def __init__(self, name, choices, description, isRequired=True, onlyOne=False, default=None, ignoreCase=True):
        if ignoreCase:
            for i in range(len(choices)):
                choices.append(choices[0].lower())
                del choices[0]
        self.choices = choices
        self.ignoreCase = ignoreCase
        super(ChoiceField, self).__init__(name, isRequired, onlyOne, default, description,
                                          f"选择[{', '.join(choices)}]" + "，不区分大小写" if ignoreCase else "")
        self.validators.append(self.validChoice)

    def validChoice(self):
        """验证选择"""
        if self.ignoreCase:
            if self.value.lower() not in self.choices:
                self.error = f"您输入的参数{self.name}的值不在选择列表中！这是不允许的。"
                return False
        if self.value not in self.choices:
            return False
        return True

    def validType(self):
        """传回来的都是str啦 (^v^)"""
        return True


class BoolField(BaseField):
    """
    参数为bool值
    返回一定是个bool
    本处的onlyOne会更加严格
    """

    def __init__(self, name, description, isRequired=True, onlyOne=False, default=None):
        super(BoolField, self).__init__(name, isRequired, onlyOne, default, description,
                                        "是或否，真与假，true or false都可，不区分大小写")

    def validType(self):
        """传回来的都是str啦 (^v^)"""
        self.value = self.value.lower()
        if self.value == "是" or self.value == "真" or self.value == "true":
            self.value = True
        elif self.value == "否" or self.value == "假" or self.value == "true":
            self.value = False
        else:
            self.error = f"您输入的参数{self.name}的值不是是或否，真与假，true or false！这是不允许的。"
            return False
        return True
