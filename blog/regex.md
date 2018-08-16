Title:   编写正则表达式引擎
description:  编写一个简单的正则表达式引擎，支持：转义字符、重复匹配、选择、分支和分组。
Author: Jin Jay
Date:    2014-10
keywords: 正则表达式引擎
          regular expression engine
          2014种子杯初赛



编写一个简单的正则表达式引擎，支持：转义字符、重复匹配、选择、分支和分组。

---

### 程序设计及各模块的功能说明
#### 整体设计
程序流程图
![ 程序流程图 ](http://ijinjay.github.io/static/reg/1.png)
** 基本数据结构说明 **
字符节点类型  

    typedef struct WordNode {
        char content[20];                   // 节点储存的内容，供比较实用
        int  contentLen;                    // 节点存储的字符个数
        int  type;                          // 节点的类型
        int  (*pCompareFunc)(char, ...);    // 节点比较时应使用的函数
        int  quoteIndex;                    // 后项引用的编号
    }WordNode;
NFA状态节点

    typedef struct State {
        WordNode word;          // 当前待匹配单词
        enum eMulTimes  type;   // 当前状态重复信息
        struct State *  next;   // 下一个状态节点
    } State, *pStateNode;
NFA链头节点

    typedef struct Head {
        State *head;        // 头结点
        int    len;         // 字符串长度
    } Head, *pHeadNode;
分组结构

    typedef struct Group {
        char str[20];           // 分组字符串
        int len;                // 分组字符串长度
        int id;                 // 分组编号
    }Group;
模式结构

    typedef struct Patterns {
        char pattern[100];
        int  p;
    }Patterns;
分支结构

    typedef struct Branch {
        Head h[10];         // 分支数组
        int  num;           // 分支个数
    } Branch;

#### 文件读取模块
![文件](http://ijinjay.github.io/static/reg/2.jpeg) 

#### NFA生成模块
![NFA](http://ijinjay.github.io/static/reg/3.png)

#### 字符处理流程：
![NFA结构](http://ijinjay.github.io/static/reg/4.jpg)
 
#### 元字符和反义元字符处理
顺序对模式字符串进行读取，在处理到字符的时候，我们会产生新的节点保存到链表中，然后将其类型存储在pStateNode->WordNode.type中。为了方便处理，我们定义了如下枚举，来方便我们对不确定的情况进行处理，而对于已经确定的字符，由于其值一定小于256，因此我们直接将它保存在type中。

    enum eWord {
        dot       = 256,    // 点
        word      = 257,    // 字母或数字
        space     = 258,    // 空格
        digit     = 259,    // 数字
        begin     = 260,    // 一行开头
        stOrEnd   = 261,    // 单词开始或结尾
        dollar    = 262,    // 结尾
        range     = 263,    // 范围选择
        nonWord   = 264,    // 非字母或数字
        nonSpace  = 265,    // 非空白
        nonDigit  = 266,    // 非数字
        nonStOrEnd= 267,    // 非开始或结束的位置
        nonRange  = 268,    // 范围内不选择
    };
当遇到’\’符号时，我们对其后的字符进行判断。如果为数字，则说明这是一个分组节点，否则它是一个字符节点。
当遇到’[’符号时，我们一直读取到遇到’]’符号为止，并且根据两者之间的内容确定字符可以取到的范围，并将这些值存储节点中。
值得注意的是，在处理元字符和反义元字符时，我们将其重复次数默认为0，并且保存在pStateNode->type中，这时为了方便之后对重复匹配的情况进行处理。

#### 重复匹配处理
在顺序处理模式字符串时，如果碰到’{’，+,*,?符号，则应当进行重复匹配处理。为了方便进行处理，我们也定义了如下的枚举，来针对不同的重复情况。在进行重复匹配时，我们并不创建新的节点，而是修改当前节点的重复次数状态，并且将重复的次数放在pStateNode->WordNode.content中保存。

    enum eMulTimes {
        one = 0,        // 不重复，默认
        zero2one,       // 重复0-1次
        one2n,          // 重复1-n次
        zero2n,         // 重复0-n次
        n,              // 重复n次
        n2more,         // 重复n-更多次
        n2m ,           // 重复n-m次
        leftP = -1,
        rightP = -2,
        quote = -3,
    };
当碰到’{‘符号时，我们通过handleBrace函数，对{n,m},{n,},{n}三种情况进行处理。如果括号之间没有任何元素，会提供输入出错的提示。  
当遇到’+’,’*’,’?’时，则处理较为简单，改变currentNode->type即可。

#### 分支处理
处理模式字符串时，存在’|’符号，则表明出现了分支情况。由于规定的分支情况只要求处理多个正则式的情况，因此我们对用’|’符号分隔的每个正则式，都进行由模式到NFA链的处理，并且将每个链的头保存到一个结构体中。定义

    typedef struct Branch {
        Head h[10];         // 分支数组
        int  num;           // 分支个数
    } Branch;
用来存储不同分支NFA的头结点。  
在处理模式字符串时，先对其进行预处理，通过’|’符号对模式串进行预处理，将它分成多个部分，并保存在数组中。在形成了数组之后，我们将其每个模式串转换成DFA，然后依次与字符串进行匹配。
#### 分组处理
当顺序处理模式字符串时，如果遇到了’（’和’）’符号，则表明出现了分组。在通过模式串转换到NFA这一步，我们只需要生成一个节点，并声明其类型。若为’(’,则pStateNode->type = leftP；若为’)’则pStateNode->type = rightP。其中leftP和rightP为在eMulTimes中声明的枚举类型。
若遇到了’\d’符号，则说明这是一个分组引用的情况。此时我们新建一个节点，并把pStateNode->tyoe = quote, 并在pStateNode->word.quoteIndex中记录这个引用的序号。
#### 字符串匹配模块
为节点绑定匹配函数
在我们设计的WordNode中，有一个int (*pCompareFunc)(char, ..);这个指针函数的参数是可变的，因为不同类型的节点，匹配的方式存在着差别，但是却可以用一个函数指针来指向不同的处理函数，最后在匹配的时候只用调用pCompareFunc进行统一的处理，这样就实现了匹配处理的统一化。  
在通过模式串生成DFA时，我们同时为每个节点绑定了匹配的函数。我们写了如下的函数来方便我们的比较处理：

    //普通字符匹配
    int normalCompare(char ch,...) {}
    //’.’符号匹配
    int dotCompare(char ch,...) {}
    //’\w’和’\W’匹配
    int wordCompare(char ch,...) {}
    //’\d‘和’\D’匹配
    int numCompare(char ch, ...) {}
    //’\s’和’\S’匹配
    int spaceCompare(char ch, ...) {}
    // 匹配行开始，当前位置为第一个字符或前一个字符为'\n'
    int lineStartCompare(char ch, ...) {}
    // 匹配一行的结束，当前位置为最后一个字符或为'\n'
    int endCompare(char ch, ...) {}
    // 匹配单词的开始或结尾，当前位置不为空字符，前一个或后一个字符为空字符
    int startEndCompare(char ch, ...) {}
在最后进行匹配时，我们灵活应用类型，来使用这些函数（例如\S和\s的结果是相反的），达到减少代码量，增加灵活性的目的。
#### 匹配方法
拥有完整的NFA链和匹配字符串，我们从NFA链的头结点开始，对字符串进行处理。如果字符串中的下一段内容，能够满足当前节点的要求，则将结果保存下来，并转移到下一个节点。每一个类型的节点都定义了一个相应的函数，如果匹配成功就继续匹配，不成功就返回失败，进行下一个次循环匹配。

匹配过程示例：
![匹配过程](http://ijinjay.github.io/static/reg/5.jpg)
#### 重复匹配
首先要说的是，我们没有实现贪婪匹配，没有实现贪婪回退的代码，这是我们程序的不足之处。然后处理重复匹配是通过节点的状态类型来做的，如果一个节点是可重复类型，便会有一个while循环（*、+匹配）或for循环（{n,m}）。

#### 分支匹配
由于上一步已经对模式字符串进行了预处理，此时所得的NFA链已经存储在了数组当中。我们从数组中的第一个链开始，将NFA链与待匹配字符串进行匹配，直到出现能够匹配的链，或者匹配完最后一个链为止。  
因此存在多个模式串能够满足字符串时，我们输出的结果是第一个能够满足输入字符串的模式串所匹配得到的结果。 

#### 分组匹配
为了实现分组匹配的效果，我们设计了一个栈来存储匹配的字符和分组信息，并且我们在匹配每一个节点时，都对其进行处理。

栈的结构如下：

    typedef struct StackNode {
        int id;             //元素属于的分组编号
        char c;             //字符值
    }StackNode;
同时，我们有三个函数来处理栈中的情况。

    // 将字符压入栈中，参数为栈数组、字符、位置值指针、group数组、group编号指针
    void push(StackNode stack[], char c, int *pos,Group gs[], int *num)
    //弹出栈顶元素
    char pop(StackNode stack[], int *pos)
    //生成新的分组
    Group* genGroup(StackNode stack[], int *pos)
有两种情况下，我们会进行压栈处理，分别是currentNode->type = pleft或pright时我们将’(’和’)’压入栈中，或者说字符串和节点匹配时将当前字符压入栈中。  
压栈时，如果遇到’(’，则要记录这是第几个分组，因为分组的编号是根据’(’的位置确定的；如果遇到普通字符，则将其放入栈中；如果遇到’)’，我们就生成新的分组，不断的进行pop，直到弹出’(’。我们将所有出栈的元素产生一个新的分组，并根据编号，把它放在一个Group数组的对应位置当中。这样我们就记录了已知的分组的字符串情况。  
如果碰到的节点currentNode->type = quote，那么这就是一个对于已知分组的引用。于是这里的匹配则将取出currentNode->word.quoteIndex，并根据这个编号取出之前Group数组中所存的字符串，将它和需要匹配的字符串进行比较。如果完全相同，则说明后项引用是正确的。

#### 输出模块
在得到每个匹配的结果后，我们将匹配的每个结果写入文件中。此时根据处理的序号生成文件名，并将所得结果写入文件当中。

### 附加信息
代码托管地址：[2014种子杯](https://github.com/ijinjay/2014SeedCup)



[TOC]
