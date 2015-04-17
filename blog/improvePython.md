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
**如果使用对象不是信任源，应该尽量避免使用eval，在需要使用eval的地方可用安全性更好的`ast.literal_eval`替代。**

### 分清==与is的适用场景
`x is y`当且仅当x和y是同一个对象的时候才返回True。  
**判断两个对象相等应该使用==而不是is。**

### 考虑兼容性，尽可能使用Unicode
**decode()** 解码  
**encode()** 编码  

    # coding=utf-8
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
Python中一切皆对象，每一个对象都一个唯一的标示符(id())、类型(type())以及值。对象根据其值能否修改该分为可变对象和不可变对象，其中**数字、字符串、元组**属于不可变对象；字典、列表、字节数组属于可变对象。因此，字符串中某个字符不可修改。

```
# encoding:utf-8
class Student(object):
    """test student"""
    def __init__(self, name, course=[]):
        """init"""
        self.name = name
        self.course = course
    def addcourse(self, coursename):
        self.course.append(coursename)
    def printcourse(self):
        for item in self.course:
            print item

if __name__ == '__main__':
    stuA = Student("Jin Jay")
    stuA.addcourse("Math")
    stuA.addcourse("English")
    print stuA.name + "'s course:"
    stuA.printcourse()
    print "----------------"
    stuB = Student("Snow")
    stuB.addcourse("Chinese")
    stuB.addcourse("Physics")
    print stuB.name + "'s course:"
    stuB.printcourse()
```

输出为：

    Jin Jay's course:
    Math
    English
    ----------------
    Snow's course:
    Math
    English
    Chinese
    Physics

由于init()函数的第二个参数是个默认参数，默认参数在函数被调用的时候仅仅被评估一次，以后都会使用第一次评估的结果，因此实际上对象空间里面的course所指向的是list的地址，每次操作的实际上是list所指向的具体列表。故我们在将可变对象作为函数默认参数的时候要特别警惕，**对可变对象的更改会直接影响原对象**。解决这个问题，最好的方式是传入None作为默认参数，在创建对象的时候动态生成列表。

    def __init__(self, name, course=None):
        self.name = name
        if course is None:course=[]
        self.course = course

对可变对象，需要注意浅拷贝

    >>> list1 = ['a', 'b', 'c']
    >>> list2 = list1
    >>> list1.append('d')
    >>> list1
    ['a', 'b', 'c', 'd']
    >>> list2
    ['a', 'b', 'c', 'd']    # list2也发生变化
    >>> list3 = list1[:]    # 切片是浅拷贝
    >>> list3.remove('a')
    >>> list3
    ['b', 'c', 'd']
    >>> list1
    ['a', 'b', 'c', 'd']
    >>> id(list3)           # list3指向新内存
    4536661200
    >>> id(list1)
    4536477456
    >>> id(list2)
    4536477456

### 函数传参既不是传值也不是传引用
正确的叫法应该是传对象或者传对象的引用。函数参数在传递的过程中将整个对象传入，对可变对象的修改在函数外部以及内部都可见，调用者和被调用者之间共享这个对象；而对于不可变对象，由于并不能真正被修改，因此，修改该往往是通过生成一个新对象然后赋值来实现的。

### 慎用变长参数
Python支持可变长度的参数列表，可以通过在函数定义的时候使用`*args`和`**kwargs`这两个特殊语法来实现。

1. 使用`*args`来实现可变参数列表：`*args`勇于接受一个包装为元组形式的参数列表来传递非关键字参数，参数个数可以任意。
2. 使用`**kwargs`接受字典形式的关键字参数列表，其中字典的键值对分别表示不可变参数的参数名和值。

### 深入理解str()和repr()的区别
1. 两者之间的目标不同：str()主要面向用户，其目的是可读性，返回形式为用户友好性和可读性都较强的字符串类型；而repr()面向的是Python解释器，或者说开发人员，其目的是准确性，其返回值表示Python解释器内部的含义，常作为编程人员的debug用途。
2. 在解释其中直接输入a时默认调用repr()函数，而print a则调用str()。
3. repr()返回值一般可以用eval()函数来还原对象。
4. 这两个方法分别调用内建的`__str__()`和`__repr__()`方法。

### 分清staticmethod和classmethod的适用场景
Python中的静态方法和类方法都依赖于装饰器来实现。其中静态方法的用法如下：

    class C(object):
        @staticmethod
        def f(arg1, arg2, ...):

类方法的用法如下：

    class C(object):
        @classmethod
        def f(cls, arg1, arg2, ...):

### 掌握字符串基本用法
编写多行字符串小技巧：

    s = ('select * '
        'from atable '
        'where afield="value"')

判断一个变量是否是字符串，使用isinstance(s, basestring).

1. 性质判定
    `is*()`、`*with()`
2. 查找替换
    count()、find()、index()、sub()、rfind()、rindex()、rindex()
    推荐按使用in、not in 判断是否包含子串
    replace(old, new[,count]),如果指定count，就最多替换count次，否则全部替换。
3. 分切与连接
    partition(sep)、split([sep[, maxsplit]]):partition()返回三个元素的元组对象[left, sep, right];split()中maxsplit是分切的次数。
4. 变形  
    lower()、upper()、capitalize()、swapcase()
5. 填空与删减
    strip([chars])、lstrip()、rstrip()
    center(width[, fillchar])、ljust(width[, fillchar])、rjust(width[, fillchar])、zfill(width)、expandtabs([tabsize])

### 按需选择sort()或者sorted()

    sorted(iterable[, cmp[, key[, reverse]]])
    s.sort([cmp[, key[, reverse]]])

1. cmp为用户定义的任何比较函数，函数的参数为两个可比较的元素，函数根据地一个参数与第二个参数的关系依次返回-1、0、1
2. key是带一个参数的函数，用来为每个元素提取比较值
3. reverse表示排序结果是否反转（默认从小到大）

当排序对象时列表时，sorted()函数会返回一个排序后的列表，原有列表保持不变；而sort()函数会直接修改原有列表，函数返回为None。

无论是sort()还是sorted()传入参数key比传入参数cmp效率更高。

sorted()函数功能更强大，，使用它可以方便地对不同的数据结构进行排序：  
**对字典排序**

    phonebook = {'Linda': '7750', 'Bob': '9345', 'Carol': '5834'}
    from operator import itemgetter
    sorted_pb = sorted(phonebook.iteritems(), key=itemgetter(1))

**多维list排序**

    from operator import itemgetter
    gameresult = [['Bob', 95.00, 'A'], ['Alan', 86.0, 'C'], ['Mandy', 82.5,'A'], ['Bob', 86, 'E']]
    sorted(gameresult, key=itemgetter(2, 1))

### 使用copy模块深拷贝对象
**浅拷贝**  构造一个新的复合对象并将从原对象中发现的引用插入该对象中。

**深拷贝** 也构造一个新的复合对象，但是遇到引用会继续递归拷贝其所指向的具体内容，使用copy模块的deepcopy()操作实现。深拷贝得到的对象与原对象是相互独立的。

### 深入掌握ConfigParser
#### getboolean()
getboolean()将0、no、false、off转义为False，对应的1、yes、true、on都被转义为True，其他值都会导致抛出ValueError异常。

配置项的查找规则
1. 如果找不到节名，就抛出NoSectionError
2. 如果给定的配置项出现在get()方法的vars参数中，则返回vars参数中的值
3. 如果在指定的接种含有给定的值，则返回其值
4. 在配置文件中有[DEFAULT]节，当读取的配置项不在指定的节里时，ConfigParser会在[DEFAULT]节中查找
5. 如果在构造函数的defaults参数中有指定的配置项，则返回其值
6. 抛出NoOptionError

    [DEFAULT]
    conn_str = %(dbn)s://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s
    dbn = mysql
    user = root
    host = localhost
    port = 3308
     [db1]
    user = aaa
    pw = ppp
    db = example
     [db2]
    host = 192.168.0.110
    pw = www
    db = example


    import ConfigParser
    conf = ConfigParser.ConfigParser()
    conf.read('format.conf')
    print conf.get('db1', 'conn_str')
    print conf.get('db2', 'conn_str')

### 使用argparse处理命令行参数

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outpu')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    parser.add_argument('bar', type=argparser.FileType('w'))
    parser.add_args(['output.txt'])
    parser.add_argument('door', type=int, choices=range(1, 4))

### 使用pandas处理大型CSV文件
CSV(Comma Separated Values)逗号分隔型值的纯文本格式文件。

    import pandas
    pandas.read_csv()
    # 分块处理
    pandas.read_table()

### 一般情况下使用ElementTree解析XML

**ElementTree的主要方法**

主要的方法、属性 | 方法说明和使用
--------------|------------
getroot() | 返回xml文档的根节点
find() findall() findtext() | 从根节点开始搜索
iter(tag=None) | 从根节点开始，根据传入的元素的tag返回所有的元素集合的迭代器
iterfind() | 根据传入的tag名称或者path以迭代器的形式返回所有的子元素

**Element的主要方法**

主要的方法、属性 | 方法说明和使用
--------------|------------
tag | 字符串，用来表示元素所代表的名称
text | 表示元素对应的具体值
attrib | 用字典表示的元素的属性
get(key, default=None) | 根据元素属性字典的key值获取对应的值，如果找不到对应的属性，则返回default
iterms() | 将元素属性以（名称，值）的形式返回
keys() | 返回元素属性的key值结合
find() findall() | 查找
list(elem) | 根据传入的元素返回其所有的子节点

### 使用JSON序列化

    try: import simplejson as json
    except ImportError: import json

### 使用traceback获取栈信息

1. traceback.print\_exception(type, value, traceback[, limit[, file]])
    根据limit的设置打印栈信息，file为None的情况下定位到sysstderr，否则则写入文件；其中type、value、traceback这三个参数对应的值可以从sys.exe\_info()中获取
2. tracebreak.print\_exc([limit[, file]])
    打印三部分信息：错误类型、错误对应的值、具体的trace信息
3. traceback.format\_exc([limit])
    与print\_exec类似，区别在与返回值为字符串
4. traceback.extract\_stack([file[, limit]])
    从当前栈帧中提取trace信息

### 使用logging记录日志信息
日志级别，使用`Logger.setLevel(level)`来设置

Level | 使用情形
------|-------
DEBUG | 详细的信息，在追踪问题的时候使用
INFO | 正常的信息
WARNING | 一些不可预见的问题发生，或者将要发生，如磁盘空间低等，但不影响程序的运行
ERROR | 由于某些严重的问题，程序中的一些功能受到影响
CRITICAL | 严重的错误，或者程序本身不能够继续运行

logging包含四个主要对象
1. **logger**：logger是程序信息输出的接口，分散在不同的代码中，是得程序可以在运行的时候记录相应的信息，并根据设置的日志级别或filter来决定哪些信息需要输出，并将这些信息分发到其关联的handler。常用的方法有logger.setlevel()、logger.addhandler()、logger.removehandler()、logger.addfileter()、logger.debug()、logger.info()、logger.warning()、logger.error()等。
2. **handler**：handler用来处理信息的输出，可以将信息输出到控制台、文件或者网络。常用的有streamhandler和filehandler。
3. **formatter**：决定log信息的格式，格式使用类似于%(dictionary key)s的形式来定义。
4. **filter**：用来决定哪些信息需要输出。可以被handler和logger使用，支持层次关系。

logging.basicConfig([**kwargs])提供对日志系统的基本配置。支持的字典参数为：

格式 | 描述
----|----
filename | 指定FileHandler的文件名，而不是默认的StreamHandler
filemode | 打开文件的模式，同open函数中的同名参数，默认为'a'
format | 输出格式字符串
datefmt | 日期格式
level | 设置根logger的日志级别
stream | 指定StreamHandler，这个参数若与filename冲突，忽略stream

    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.txt',
        filemode='w',
        format='%(asctime)s %(filename)s[line:%(lineno)d %(levelname)s %(message)s',
    )

**logging使用建议**  
1. 尽量为logging取一个名字而不是采用默认，这样当在不同的模块中使用的时候，其他模块只需要使用以下代码就可以方便地使用同一个logger，因为它本质上复合单例模式。

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger=logging.getLogger(__name__)

2. 为了方便地找出问题所在，logging的名字建议以模块或者class来命名。logging名称遵循'.'划分的继承规则，根是root logger, logger a.b的父logger对象为a。
3. logging只是线程安全的，不支持多进程写入同一个日志文件，因此对于多个进程，需要配置不同的日志文件。

### 使用threading模块编写多线程程序

### 使用Queue使多线程变成更安全
> 程序中存在三种类型的bug：你的bug、我的bug和多线程。

Queue模块有三种队列：
1. Queue.Queue(maxsize): 先进先出，maxsize为队列的大小，为非正数时为无限循环队列。
2. Queue.LifoQueue(maxsize): 后进先出，即栈。
3. Queue.PriorityQueue(maxsize): 优先级队列。

多线程下载实例：

    import os, Queue, threading, urllib2
    class DownloadThread(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init(self)
            self.queue = queue
        def run(self):
            while True:
                url = self.queue.get()
                print self.name+" begin download"+url+"..."
                self.download_file(url)
                self.queue.task_donw()
                print self.name+" download completed!!!"
        def download_file(self, url):
            urlhandler = urllib2.urlopen(url)
            fname = os.path.basename(url)+'html'
            with open(fname, "wb") as f:
                while True:
                    chunk = urlhandler.read(1024)
                    if not chunk: break
                    f.write(chunk)
    if __name__ == "__main__":
        urls = ["http://www.python.org/moin/WebProgramming",
                "https://www.createspace.com",
                "http://wiki.python.org/moin/Documentation"
            ]
        queue = Queue.Queue()
        for i in range(5):
            t = DownloadThread(queue)
            t.setDaemon(True)
            t.start()
        for url in urls:
            queue.put(url)
        queue.join()

### 利用模块实现单例模式
使用模块的好处：
1. 所有的变量都会绑定到模块
2. 模块只初始化一次
3. import机制是线程安全的（保证了在并发状态下模块也只有一个实例）

### 用mixin模式让程序更加灵活
模板方法模式是子类在不改变算法结构的情况下，重新定义算法中的某些步骤。

    import mixins
    def staff():
        people = People()
        bases = []
        for i in config.checked():
            base.append(getattr(mixins, i))
        people.__bases__ += tuple(bases)
        return people

### 用发布订阅模式实现松耦合

    pip install message

### 用状态模式美化代码

    pip install state

实例

```python
from state import curr, switch, stateful, State, behavior
@statefull
class User(object):
    class NeedSignin(State):
        default = True
        @behavior
        def signin(self, usr, pwd):
            ...
            switch(self, Player.Signin)
    class Signin(State):
        @behavior
        def move(self, dst):...
        @behavior
        def atk(self, other):...
```

### \_\_init\_\_不是构造方法
`__new__()`方法才是真正的类的构造方法。  
`object.__new__(cls[,args...])`: 其中cls代表类，args为参数列表。  
`object.__init__(self[,args...])`: 其中self代表是咧对象，args为参数列表。

`__new__` VS `__init__`
1. `__new__`是静态方法，而`__init__`是实例方法
2. `__new__`方法一般需要返回类的对象，当返回类的对象时将会自动调用`__init__`方法进行初始化，如果没有对象返回，则`__init__`方法不会被调用。`__init__`不需要显示返回，默认为None，否则会在运行时抛出TypeError
3. 当需要控制实例创建的时候可使用`__new__`方法，而控制实例初始化的时候使用`__init__`
4. 一般情况下不需要覆盖`__new__`，但当子类继承自不可变类型，如str、int、unicode或者tuple的时候，往往需要覆盖该方法
5. 当需要覆盖`__new__`和`__init__`方法的时候这两个方法的参数必须保持一致，如果不一致将导致异常
6. 作为用来初始化的`__init__`方法在多继承的情况下，子类的`__init__`方法如果不显示调用父类的`__init__`方法，则父类的`__init__`方法不会被调用

### 理解名字查找机制
1. **局部作用域**：默认情况下，函数内部任意的复制操作所定义的变量名，如果没用global语句，则申明都为局部变量，即仅在该函数内可见。
2. **全局作用域**：定义在Python模块文件中的变量名拥有全局作用于，需要注意的是这里的全局仅限单个文件，挤在一个文件的顶层的变量名尽在这个文件内可见，并非所有的文件，其他文件中项实用这些变量名必须先导入文件对应的模块。
3. **嵌套作用域**：在多重函数嵌套的情况下才会考虑到。需要注意的是global语句仅针对全局变量，在嵌套作用域的情况下，如果想在嵌套的函数内修改该外层函数中定义的变量，及时使用global进行申明也不能达到目的，其结果最终是在嵌套的函数所在的命名空间中创建了一个新的变量。
4. **内置作用域**：通过一个标准库中名为`__builtin__`的模块来实现。

朝赵顺序遵循变量解析机制LEGB法则。

### 理解MRO与多继承
MRO(Method Resolution Order, 方法解析顺序)

### 区别`__getattr__`与`__getattribute__`
`__getattribute__()`总会被调用，而`__getattr__()`只有在`__getattribute__()`中印发异常的情况下才会被调用。

### 使用更为安全的property
property是用来实现属性可管理性的built-in数据类型，其实只是一种特殊的数据描述符。使用property的优点：
1. 代码更简洁，可读性更强。
2. 更好的管理属性的访问。
3. 代码可维护性更好。
4. 控制属性访问权限，提高数据安全性。
![property](http://jinjaysnow.github.io/images/property.png)

两种使用property的形式：  
**形式一**

    class Some_Calss(object):
        def __init__(self):
            self._somevalue = 0
        def get_value(self):
            return self._somevalue
        def set_value(self, value):
            self._somevalue = value
        def del_attr(self):
            del self._somevalue
        x = property(get_value, set_value, del_attr, "......")

**形式二**

    class Some_Clasee(object):
        _x = None
        def __init__(self):
            self._x = None
        @property
        def x(self):
            return self._x
        @x.setter
        def x(self, value):
            self._x = value
        @x.deleter
        def x(self):
            del self._x

### 使用中缀语法

    pip install pipe

一个小题：
> 计算小于4 000 000的斐波那契数中的偶数之和

    from pipe import *
    def fib():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    fib() | where(lambda x: x%2 == 0) | take_while(lambda x: x < 4000000) | add

### 熟悉Python的迭代器协议
1. 实现\_\_iter\_\_()方法，返回一个迭代器
2. 实现next()方法，返回当前的元素，并指向下一个元素的位置，如果当前位置已无元素，则抛出StopIteration异常

### 熟悉Python的生成器
如果一个函数，使用了yield语句，那么它就是一个生成器函数。

每一个生成器函数调用之后，它的函数体并不执行，而是到第一次调用next()的时候才开始执行。当第一次调用next()方法时，生成器函数开始执行，执行到yield表达式为止。

### 基于生成器的协程及greenlet
协程，又称微线程。协程往往实现在语言的运行时库或虚拟机中，操作系统对其存在一无所知，所以又被称为用户空间线程或绿色线程。用协程做的东西，用线程或进程通常也是一样可以做的，只是会多一些加锁和通信的操作。

生产者与消费者问题：

    def consumer():
        while True:
            line = yield
            print(line.upper())
    def producer():
        with open('...', 'r') as f:
            for i, line in enumerate(f):
                yield line
                print 'processed line %d' % i
    c = consumer()
    c.next()
    for line in producer():
        c.send(line)

Python2.x版本对协程的支持有限，使用greenlet库。

### 理解GIL的局限性
GIL(Global Interpreter Lock)全局解释器锁，是Python虚拟机上用作互斥线程的一种机制，它的作用是保证任何情况下虚拟机中只有一个线程被运行，而其他线程都处于等待GIL锁被释放的状态。故多核计算机不能发挥很好的优势。

### 对象的管理与垃圾回收
Python使用引用计数器的方法来管理内存中的对象，即针对每一个对象维护一个引用计数值来表示该对象当前有多少个引用。当其他对象引用该对象时，其引用对象会增加1，而删除一个对当前对象的引用，其引用计数会减1。只有当引用计数的值为0的时候该对象才会被垃圾回收器回收，因为他表示这个对象不再被其他对象引用，是个不可达对象。引用计数法最明显的缺点是无法解决循环引用的问题，即两个对象相互引用。

使用gc模块触发垃圾回收：一种是通过显示的调用gc.collect()进行垃圾回收；一种是在创建新的对象为其分配内存的时候，检查threshold阈值，当对象的数量超过threshold的时候便自动进行垃圾回收。默认情况下阈值设为(700, 10, 10)。

### 使用paster创建包
Python自带的有一个distutils标准库：
1. 支持包的构建、安装、发布
2. 支持PyPI的登记、上传
3. 定义了扩展指令的协议，包括distutils.cmd.Command基类、distutils.commands和distutils.key_words等入口点，为setuptools和pip等提供了基础设施

使用distutils，按习惯需要编写一个setup.py文件，作为后续操作的入口点

    from distutils.core import setup
    setup(name='***',
          version='1.0',
          py_modules=['***'],
          )

编写好setup.py文件以后，就可以使用`python setup.py install`把它安装到系统中了。

使用pastescript自动穿件项目的setup.py文件及相关的配置、目录等。

    pip install pastescript

安装以后可以使用paster命令




[TOC]


