title: 改善Python程序
author: Jin Jay
date: 2014-11
description: 《编写高质量代码————改善Python程序的91个建议》：主要记录编写高质量Python程序需要注意的地方。
keywords: improve python
            改善Python程序


《编写高质量代码--改善Python程序的91个建议》：主要记录编写高质量Python程序需要注意的地方(个人觉得有用的建议)。

### Python与C语言的不同之处
#### 三元操作符
`C?X:Y`在Python中的表示为`X if C else Y`

### 编写函数的四个原则
#### 原则一
函数设计要尽量短小，嵌套层次不宜过深。
#### 原则二
函数申明应该做到合理、简单、易于使用。
#### 原则三
函数参数设计应该考虑向下兼容。

    def readline(filename):                     ### 第一版
        print "file read completed"
    def readline(filename, logger=logger.info)  ### 第二版，使用了默认参数，兼容了上一版 
#### 原则四
一个函数只做一件事，尽量保证函数语句粒度的一致性。

### 将常量集中到一个文件

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

### 利用assert语句来发现问题

    assert expression1 ["," expression2]
断言实际是被设计用来捕获用户所定义的约束的，而不是用来捕获程序本身错误的，所以需要谨慎使用。
### 数据交换值的时候不推荐使用中间变量

    x,y = y,x

### 不推荐使用type来进行类型检查
**基于内建类型扩展的用户自定义类型，type函数并不能准确返回结果。**  
正确做法是：如果类型有对应的工厂函数，可以使用工厂函数对类型进行相应的转换，如`list(listing)`，`str(name)`等，否则可以使用`isinstance()`函数来检测。

    isinstance(object, classinfo)

### 警惕eval()的安全漏洞
> eval is evil.
**如果使用对象不是新人员，应该尽量避免使用eval，在需要使用eval的地方可用安全性更好的`ast.literal_eval`替代。**

### 分清==与is的适用场景
`x is y`当且仅当x和y是同一个对象的时候才返回True。  
**判断两个对象相等应该使用==而不是is。**

### 考虑兼容性，尽可能使用Unicode
**decode()** 解码  
**encode()** 编码  

    ### coding=utf-8
### 构建合理的包层次来管理module
包结构：

    Package/ __init__.py
        Module1.py
        Module2.py
        Subpackage/ __init__.py
            Module1.py
            Module2.py

`__init__.py`通过在该文件中定义`__all__`变量，控制需要导入的子包或模块。

    __all__ = ['Module1', 'Module2', 'Subpackage']

### 使用with自动关闭资源

    with expression [as target]:
        codes

### 遵循异常处理的基本原则
![exceptionhandle.png](http://jinjaysnow.github.io/images/exceptionhandle.png)

1. 注意异常的粒度，不推荐在try中放入过多的代码。
2. 谨慎使用单独的except语句处理所有异常，最好能定位具体的异常。
3. 注意异常捕获的顺序，在合适的层次处理异常。
4. 使用更为友好的异常信息，遵守异常参数的规范。

### 连接字符串优先使用join而不是+

### 格式化字符串是尽量使用.format方式而不是%
#### %转换标记

    %[转换标记] [宽度[.精确度]]

| 转换标记 | 解释 |
| ------ | ---- |
| - | 表示左对齐 |
| + | 在整数之前加上+ |
| 空格 | 在整数之前保留空格 |
| ### | 在八进制数前面显示('0')，在十六禁止前面显示'0x'或者’0X' |
| 0 | 表示转换值若位数不够则用0填充而非默认的空格 |
| c | 转换为单个字符，对于数据将转换为改值所对应的Ascii码 |
| s | 转换为字符串，对于非字符串对象，将默认调用str()函数进行转换 |
| r | 用repr()函数进行字符串转换 |
|i d | 转换为带符号的十进制数 |
| u | 转换为不带符号的十进制数 |
| o | 转换为不带符号的八进制数 |
| x X | 转换为不带符号的十六进制数 |
| e E | 转换为科学计数法表示的浮点数 |
| f F | 转成浮点数(小数部分自然截断) |
| g G | 如果指数大于-4或者小于精度值则和e相同，其他情况与f相同；如果指数大于-4或者小鱼精度值则和E相同，其他情况与F相同 |

例：

    iitemdict = {'itemname':'circumference', 'radius':3, 'value': match.pi*radius*2}
    print "the %(itemname)s of a circle with radius %(radius)f is %(value)0.3f" % itemdict
#### format方式

    [[填充符][对齐方式]][符号][#][0][宽度][,][.精确度][转换类型]

**.format方式格式化字符串的对齐方式**

对齐方式 | 解释 
------- | ------
< | 表示左对齐， 是大多数对象为默认的对齐方式
\> | 表示右对齐，数值默认的对齐方式
= | 仅对数值类型有效，如果有符号的话，在符号后数值前进行填充
^ | 居中对齐，用空格进行填充

**.format方式格式化字符串符号列表**

符号 | 解释
--- | ----
+ | 正数前加+，附属前加-
- | 正数前不加符号，负数前加-，为数值的默认形式
空格 | 正数前加空格，负数前加-

例：

    "The number {0:,} inn hex is:{0:#x}, the number {1} in oct is {1:#o}".format(4746, 45)
    输出为：'the number4,746 in hex is: 0x128a, the number 45 in oct is 0o55'

    "the max number is {max}, the min number is {min}, the averagenumber is {average:0.3f}".format(max=189, min=12.6, average=23.5)
    输出为：'the max number is 189, the min number is 12.6, the averagenumber is 23.500'

    point = (1,3)
    'X:{0[0]};Y:{0[1]}'.format(point)
    输出为：'X:1;Y:3'

### 区别对待可变对象和不可变对象



[TOC]