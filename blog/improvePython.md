title: 改善Python程序
author: Jin Jay
date: 2014-11
description: 《编写高质量代码————改善Python程序的91个建议》：主要记录编写高质量Python程序需要注意的地方。
keywords: improve python
            改善Python程序


《编写高质量代码--改善Python程序的91个建议》：主要记录编写高质量Python程序需要注意的地方(个人觉得有用的建议)。

# Python与C语言的不同之处
## 三元操作符
`C?X:Y`在Python中的表示为`X if C else Y`

# 编写函数的四个原则
## 原则一
函数设计要尽量短小，嵌套层次不宜过深。
## 原则二
函数申明应该做到合理、简单、易于使用。
## 原则三
函数参数设计应该考虑向下兼容。

    def readline(filename):                     # 第一版
        print "file read completed"
    def readline(filename, logger=logger.info)  # 第二版，使用了默认参数，兼容了上一版 
## 原则四
一个函数只做一件事，尽量保证函数语句粒度的一致性。

# 将常量集中到一个文件

```python
class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't change const. %s" % name
        if not name.isupper():
            raise self.ConstCaseError, 'const name "%s" is not all uppercase' % name
        self.__dict__[name] = value
import sys
sys.modules[__name__] = _const()
```

上面的代码对应的模块名未const，使用时只需要import const，便可定义常量了，例如：

    import const
    const.COMPANY = "APPLE"

# 利用assert语句来发现问题

    assert expression1 ["," expression2]
断言实际是被设计用来捕获用户所定义的约束的，而不是用来捕获程序本身错误的，所以需要谨慎使用。
# 数据交换值的时候不推荐使用中间变量

    x,y = y,x

# 不推荐使用type来进行类型检查
**基于内建类型扩展的用户自定义类型，type函数并不能准确返回结果。**  
正确做法是：如果类型有对应的工厂函数，可以使用工厂函数对类型进行相应的转换，如`list(listing)`，`str(name)`等，否则可以使用`isinstance()`函数来检测。

    isinstance(object, classinfo)

# 警惕eval()的安全漏洞
> eval is evil.
**如果使用对象不是新人员，应该尽量避免使用eval，在需要使用eval的地方可用安全性更好的`ast.literal_eval`替代。**

# 分清==与is的适用场景
`x is y`当且仅当x和y是同一个对象的时候才返回True。  
**判断两个对象相等应该使用==而不是is。**

# 考虑兼容性，尽可能使用Unicode
**decode()** 解码  
**encode()** 编码  

    # coding=utf-8
# 构建合理的包层次来管理module
包结构：

    Package/ __init__.py
        Module1.py
        Module2.py
        Subpackage/ __init__.py
            Module1.py
            Module2.py

`__init__.py`通过在该文件中定义`__all__`变量，控制需要导入的子包或模块。

    __all__ = ['Module1', 'Module2', 'Subpackage']

# 使用with自动关闭资源

    with expression [as target]:
        codes

# 遵循异常处理的基本原则
![exceptionhandle.png](http://jinjaysnow.github.io/images/exceptionhandle.png)




[TOC]