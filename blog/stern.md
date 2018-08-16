Title: 东软实习报告
Author: Jin Jay
Date: 2014-08
description: Intern Report in NEUSOFT东软，东软实习报告.
Keywords: 东软实习报告

# 实习内容记述

2014年 6月 17号到7月 11号，在大连东软集团实习。

## 实习任务
经过30多个小时的车程后，在18号下午到达了东软集团，路途比较长，下午在安排的员工宿舍休息。在到达东软集团的第二天，见到了实习经理，他给我们介绍了一下此次实习的日程安排：

```
前期学习 Linux环境编程和系统编程。
根据所学制作一款局域网聊天软件或邮件系统软件。
```

## 实习过程
从到东软的第二天开始，先是学习在 Windows电脑上的 Vmware虚拟机软件中安装 Ubuntu系统。然后是熟悉Linux环境编程。接触到了一些常用命令`ls`, `ps`, `top`, `kill`, `grep`, `find`, `man`, `cd`, `rm`, `cp`, `locate`, `which`, `what`, `whatis`, `where`, `whereis`... 还有管道操作`|`，重定向操作`<`和`>`等等。每一个命令都会练习使用好几遍以达到熟悉的程度。  
Linux系统编程从介绍 Vim编辑器开始，然后是 gcc编译器的使用， gdb调试工具的使用， makefile的编写，最后是系统函数调用(系统编程)的学习。  
6月 28号开始了小组分配和项目编写。我们小组总共8个人，其中一个项目经理，一个评审负责人，一个配置管理员。我是小组评审负责人，主要负责项目的设计评审、技术点分析，同时还是服务器端的编程人员。小组选择了聊天软件项目。

# 专题内容分析
## Linux环境编程学习
### Shell脚本与常用命令
> man命令  
格式化显示在线操作手册。在实习中遇到不会用的命令还有系统编程时不会使用的函数时，通过man命令能够很快速的找到有用的信息，十分好用。例如：

```
man ls # 查看ls命令的帮助信息
```
<img src="http://ijinjay.github.io/images/manls.png">
> 其他常用命令

```
cd ..           # 改变位置到父目录
cd ~            # 改变位置到用户工作目录
cp file1 file2  # 将文件file1复制到file2
mv file1 file2  # 将文件file1更名为file2
mkdir dir1      # 建立一个目录dir1
rm f*           # 删除当前所有以f开头的文件
rm -r dir1      # 删除目录dir1及其子目录下所有文件
cat file1       # 打印文件内容到屏幕
pwd             # 列出当前所在的目录信息
chmod mode file # 改变文件的读写执行权限
```
### 管道 `|`
*语法：* 命令1 | 命令2  
将命令1的执行结果送给命令2，作为命令2的输入。  
管道使得两个及多个命令可以相互通信，带来了很多的便利。

```
ls -R1 | more   # 以分页的方式列出当前目录及其子目录下所有文件的名称
```
### 输入输出重定向`<` & `>`
*语法：* 命令 `<` 文件  
将文件作为命令的输入。
*语法：* 命令 `>` 文件  
将命令的结果送至指定的文件。  
输入输出重定向便于将操作的结果送入文件或读取文件作为操作的输入。

```
mail -s "theme" xx@email.com < file1 # 将文件file1当做信件内容发给收件人
ls -l > list    # 将”ls -l“的结果写入文件list
```

## Linux系统编程
### Vim编辑器
Vim是从vi发展出来的一个文本编辑器。代码补全、编译及错误跳转等方便编程的功能特别丰富。Vim拥有多种模式，常用有三种：

> 普通模式  
在普通模式中，用的是编辑器命令，比如移动光标，删除文本等等。这是Vim启动后的默认模式。常用命令有：

```
j   # 光标向上移动一行
k   # 光标向下移动一行
h   # 光标向左移动一个字符
l   # 光标向右移动一个字符
w   # 光标移到下一个单词词首
e   # 光标移到单词末尾或下一个单词末尾
b   # 光标回退到词首或回退到上一个单词词首
dd  # 删除一行
daw # 删除当前光标所在单词
r   # 替换一个字符
x   # 删除当前光标所在的一个字符
G   # 跳转到文章末尾
gg  # 跳转到文章开头
```


> 插入模式  
在普通模式中，有很多方法可以进入插入模式。常用的方式是按"a"（append／追加）键或者"i"（insert／插入）键。在这个模式中，大多数按键都会向文本缓冲中插入文本。在插入模式中，可以按ESC键回到普通模式。

> 可视模式  
这个模式与普通模式比较相似。但是移动命令会扩大高亮的文本区域。高亮区域可以是字符、行或者是一块文本。当执行一个非移动命令时，命令会被执行到这块高亮的区域上。Vim的"文本对象"也能和移动命令一样用在这个模式中。

```
y   # 复制高亮选中的文本
p   # 粘贴复制在缓冲区的文本
```
> Vim文件配置

```
# 定义F5键用于构建并运行c文件
map <F5> :call Compilerungcc() <CR>
func! Compilerungcc()
exec "w"
exec "!gcc % -o %c"
exec "! ./%<"
endfunc
```
### GCC  
GCC（GNU Compiler Collection，GNU编译器套装），是一套由GNU开发的编程语言编译器。

```
gcc -E hello.c -o hello.i   # 预处理
gcc -S hello.i -o hello.s   # 编译
gcc -c hello.s -o hello.o   # 汇编
gcc hello.o -o hello        # 链接
```
**gcc参数**  
`gcc -I目录 -l链接库 -L链接库路径`

**gcc生成链接库**  

```
# 静态链接库
gcc -c source.c -o source.o             # 生成.o文件
ar rcs -o libsource.a source.o          # ar命令将.o文件打包成静态库文件
ar t libsource.a                        # 查看libsource.a包含哪些文件 
# 动态链接库
gcc -c source.c -fpic -o source.o       # 添加-fpic选项生成.o文件
gcc -shared source.o -o libsource.so    # 生成动态链接库
```
### Makefile
> 在软件开发中，make是一个工具程序（Utility software），它是一种转化文件形式的工具，转换的目标称为“target”；与此同时，它也检查文件的依赖关系，如果需要的话，它会调用一些外部软件来完成任务。大多数情况下，make被用来编译源代码，生成结果代码，然后把结果代码连接起来生成可执行文件或者库文件。*makefile*便是make用来确定一个target文件的依赖关系，然后把生成这个target的相关命令传给shell去执行的文件。

```
# makefile预定义变量
$@ 目标名称
$^ 所有被依赖的对象
$< 第一个被依赖的文件
# 模式规则
%.o: %.c  # 将所有的.c文件生成.o文件， %是通配符
# 使用
cc $(CCFLAGS) -c -o $@ $<
```

### GDB调试工具  
GNU调试器(Debugger，缩写：GDB)，是GNU软件系统中的标准调试器。

```
gcc -c source.c -o source -g    # 在编译时使用-g选项
list    # 显示代码
break   # 设置断点
watch   # 观察变量，变量值改变时输出值
print   # 查看变量信息
step    # 在断点时，用于一步一步继续执行，进入函数内部
next    # 在断电时，继续执行但不进入函数内部
```
### 系统编程

> 系统编程：从操作系统获得服务或资源而向内核发起的函数调用。

#### 文件和文件系统  
在Linux系统中一切皆是文件，很多交互工作是通过读取和写入文件件来完成的。  
文件通过inode（信息节点）访问，inode使用唯一的数值（inode编号）进行标识。一个inode存储文件关联的元数据，如它的修改时间戳、所有者、类型、长度以及文件的数据的地址--不包含文件名。目录将易读的文件名与inode编号进行映射。文件名与inode的配对也称为链接（link）。  
用户请求打开一个文件时，内核打开包含指定文件名的目录然后搜索该文件。内核通过文件名获得inode编号，然后根据inode编号找到对应的inode。

```
// open() 打开文件
#include <fcntl.h>
int open (const char *name, int flags, ...);
// flags: O_RDONLY, O_WRONLY, O_RDWR
// 打开文件错误时会返回-1，成功则返回文件描述符
```

```
// read() 读取文件
#include <unistd.h>
ssize_t read (int fd, void *buf, size_t len);
// 从文件fd的当前偏移量至多读取len个字节到buf中，成功时返回写入buf中的字节数，出错返回-1
```

```
// write() 写入文件
#include <unistd.h>
ssize_t write (int fd, const void *buf, size_t count);
// 从文件fd当前位置开始将buf中至多count个字节写入文件中
```

```
// close() 关闭文件
#include <unistd.h>
int close(int fd);
// 解除文件描述符的关联，并分离进程和文件的关联
```

```
// 其他调用
off_t lseek(int fd, off_t pos, int origin);     // 移动读写指针
#include <sys/stat.h>                           // 查看文件属性
int fstat(int fildes, struct stat *buf);
int lstat(const char *restrict path, struct stat *restrict buf);
int stat(const char *restrict path, struct stat *restrict buf);
// 制作文件硬链接
int link(const char *path1, const char *path2);
// 制作符号链接
int symlink(const char *path1, const char *path2);
```
#### 信号与信号处理  
信号是提供处理异步事件机制的软件终端。信号有一个明确的生命周期：首先，产生信号；然后内核存储信号直到可以发送它；最后，一旦有空闲，内核会适当的处理信号。信号处理通常有三种情况：

1. **忽略信号**  不采取任何操作。信号SIGKILL和SIGSTOP不能忽略。
2. **捕获并处理信号**  内核会暂停该进程正在执行的代码，并跳转到先前注册过的函数。接下来进程执行该函数，执行完后再跳回先前捕获信号的地方继续执行。常见的有SIGINT和SIGTERM。
3. **执行默认操作**  取决于被发送的信号。默认操作通常是终止进程。

```
#include <signal.h>
void (*signal(int sig, void (*func)(int)))(int);
typedef void (*sig_t) (int);
sig_t signal(int sig, sig_t func);
// sig: 信号种类 func: 接收到信号后调用的函数，参数是被处理信号的标识符
int sigaction(int sig, const struct sigaction *restrict act, struct sigaction *restrict oact);
// 设置信号处理动作，signal()不带信号信息，sigaction()带有额外的信号信息
```
#### 进程与线程
**进程管理**  
进程是程序实体的一次运行，是系统进行资源分配和调度的一个基本独立单位。每一个进程都有一个唯一的标识符，即进程ID，简称pid。系统保证某时刻每个pid都是唯一的。
```
// 获得进程ID
#include <sys/types.h>
#include <unistd.h>
pid_t getpid(void);     // 返回调用进程的ID
pid_t getppid(void);    // 返回进程的父进程ID
// 创建进程
pid_t fork(void);       // 父子进程不共享数据，随机运行，返回0给子进程pid_t
pid_t vfork();          // 父子进程共享数据，子进程先运行
// exec系列系统调用
int execl(const char *path, const char *arg0, ... /*, (char *)0 */);
// 将path所指路径的映像载入内存，替换当前进程的映像。execl是可变参数的，但参数列表必须以NULL(0)结尾
// 终止进程
void exit(int status);
int kill(pid_t pid, int sig);
```
**线程**  
线程是一个“轻量级的进程”。线程自己不拥有系统资源，引入线程后进程只作为除CPU外系统资源的分配单元，线程则作为处理机的分配单元，即线程是独立调度的基本单位，进程是资源拥有的基本单位。

```
#include <pthread.h>
int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg);
// 线程创建, thread: 线程标识符  attr: 线程属性(堆栈大小) start_routine: 线程调用的函数 arg: 函数参数
void pthread_exit(void *value_ptr); // 线程退出
// 线程信号量同步
int pthread_mutex_init(pthread_mutex_t *restrict mutex, const pthread_mutexattr_t *restrict attr);  
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```
**进程间通信**  
IPC（InterProcess Communication）函数提供了系统中多个进程之间相互通信的方法。Linux系统中包含以下几种方式的IPC：

1. 半双工Unix管道pipe
2. FIFO(命名管道)
3. 消息队列
4. 信号量机制
5. 共享内存
6. socket网络套接字

```
int pipe(int fildes[2]);    // pipe用于父子进程之间，如果父进程从子进程中读取数据，则父进程应关闭fd1，同时子进程关闭fd0；反之，父进程向子进程发送数据，它应该关闭fd0，子进程关闭fd1。
int mkfifo(const char *path, mode_t mode);  // 创建一个命名管道，用于不同程序之间
```

```
// 消息队列
#include <sys/ipc.h>
#include <sys/msg.h>
int msgget(key_t key, int msgflg);  // 创建或获取一个消息队列 msgflg通常为IPC_CREAT | IPC_EXCL
int msgsnd(int msqid, struct msgbuf *msgp, int msgsz, int msgflg); // 向消息队列发送消息
int msgctl(int msqid, int cmd,  struct msqid_ds *buf); // 控制对消息队列的操作
int msgrcv(int  msqid, void *msgp, size_t msgsz, long msgtyp, int msgflg); // 接收消息队列消息
// 信号量机制
#include <sys/sem.h>
int semget(key_t key, int nsems, int semflg); // 创建或获取一个信号量
int semop(int semid, struct sembuf *sops, size_t nsops); // 信号量操作
int semctl(int semid, int semnum, int cmd, ...); // 信号量控制
// 共享内存
#include <sys/shm.h>
int shmget(key_t key, size_t size, int flags); // 创建或获取一段共享内存
void *shmat(int shmid, const void *shmaddr, int shmflg); // 将共享内存段连接到进程中的地址
int shmctl(int shmid, int cmd, struct shmid_ds *buf); // 内存控制
int shmdt(const void *shmaddr); // 把内存段从晋城地址空间脱离
```

```
// socket套接字
#include <sys/socket.h>
int socket(int domain, int type, int protocol); 
// domain设置为AF_INET，type: SOCK_STREAM | SOCKDGRAM, protocol设为0
int bind(int socket, const struct sockaddr *address, socklen_t address_len);
// 将socket绑定到本地计算机的一个端口上,address_len使用sizeof()获取
int connect(int socket, const struct sockaddr *address, socklen_t address_len); // 连接
int listen(int socket, int backlog); // 侦听，backlog:允许进入连接的个数
int accept(int socket, struct sockaddr *address, socklen_t *address_len); // 处理连接
int send(int socket, const void *buffer, size_t length, int flags); // 发送数据
int recv(int socket, void *buffer, size_t length, int flags); // 接收数据
```
## 项目开发
小组选择了聊天软件项目。
### 需求分析阶段
第一天完成了软件需求分析，产生了需求分析矩阵。大体分成服务器端和客户端。小组人员分为服务器编程人员，客户端编程人员还有UI设计人员。个人在项目中参与讨论需求，之后完成了对需求矩阵的评审。

### 概要设计阶段
进入概要设计阶段，产生了概要设计文档。主要对模块，函数接口等进行设计。系统模块图如下：
![概要设计结构图](http://ijinjay.github.io/images/design.png)
作为评审负责人，我主要完成了概要设计文档的评审工作，写作了概要设计评审记录。此外，对设计中的技术点进行调查分析，主要包括QT的网络库使用、QT文件配置和Redis数据库的使用。

### 编码阶段
与另一名小组成员负责服务器端程序编写。个人主要完成 SQLite3和 Redis数据库相关代码编写。将数据库相关代码封装成概要设计相关接口。
```
// 使用hiredis与Redis数据库交互
redisContext *c = redisConnect("127.0.0.1", 6379);  // 连接本地Redis数据库
redisReply *r = (redisReply *)redisCommand(c, command); // 执行并返回结果
freeReplyObject(r); // 使用完结果后需要释放对象占用的空间
redisFree(c);       // 释放连接
// SQLite3
Sqlite3 *db = NULL; // 定义一个数据对象
int rc = sqlite3_open("test.db", &db); // 打开数据库
int sqlite3_exec(sqlite3*, const char *sql, int(*callback)(void*,int,char**,char**), void *, char **errmsg );   // 执行语句
```
编码阶段结束后，个人完成了代码评审，写作了代码评审记录。

### 测试阶段
测试阶段先由其他队员完成了测试用例的设计。个人对测试用例进行了评审，写作了测试用例评审记录。然后小组成员完成了测试，产生了系统测试报告。最后对系统测试报告进行评审。

### 项目展示
由于时间较紧，最后的软件并没有完成所有需求。没有群聊天，没有文件发送，客户端没有聊天记录保存与查询...但是软件的基本聊天功能实现了，还可以发送表情，发送图片，支持中文。
# 在实习中收获最大与体会最深的内容
不到一个月的时间，总感觉时间太短。可能是因为是实习生，在公司并没有加班什么的，朝九晚五的生活过得也还不错，有很多自己可以支配的时间。  

对于团队项目开发的感受是，在整个实习过程中，网络访问受到限制，只能通过设置网络代理打开百度网页，查看搜索资料内容也必须使用百度快照，感觉略麻烦。不过这样带来的好处是很多问题都是自己一步一步思考清楚后解决的，遇到不会的也是尽量去看文档（尽管大部分文档是英文的，看不太懂- -），而不是通过搜索引擎搜索到相应代码后复制粘贴。实习完后，感觉自己的能力有提升，尤其是看英文文档的能力。  

此外，感触很深的是项目开发过程中，一定要把设计文档写好，尤其是软件模块接口，因为文档是不同模块的编写者之间相互交流的蓝本，这次项目进度落后便是因为客户端与服务器交互的很多接口定义不是很好，双方对接口的理解也有一定的差异。最终项目的服务器端完成了大部分功能，而客户端没能跟上进度很好的完成所有需求，这是一件令人遗憾的事。
# 对实习工作的改进意见
1. 实习能够安排达到一个月的时间。
2. 对公司文化并没有太多接触，如果公司能够让学员们与正式员工多接触，多参与到他们的项目讨论中更有益于了解软件公司项目运作过程。
3. 因为软件学院的实习（应该叫做实训）与其他学院不同，实训并没有见识到很多实际的问题，都是一些自己在学校里做项目能够遇到的，如果能够接触到工业界的项目肯定很有意义。比如服务器访问量达到百万级的应用、分布式计算程序设计等等。

[TOC]
