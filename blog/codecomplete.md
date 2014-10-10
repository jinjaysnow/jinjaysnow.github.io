Title:   代码大全
Brief:   Code Complete《代码大全》，经典著作书摘，主要关于软件工程，如何构建软件，如何编写代码，应该有什么样的编程风格。
Authors: Jin Jay
image:  images/levelsOfDesign.png
Date:    2014-10
keywords: code complete
          代码大全


# 代码大全
## 需求
应付客户提出的新功能：“咦，这听起来是一个很不错的主意。不过由于它不是需求文档里的内容，我会整理一份修订过的进度表和成本估计表，这样你可以决定是现在实施，还是过一阵子再说。”

## 架构
### 架构设计的重要意义
> 如果你要盖一个简单的建筑物--比如一个狗屋--你只需要去木材店买一些木头和钉子，一个下午就做好了，如果你忘了弄一个门，或是犯了什么错误，那也没什么大不了的，修改一下或者干脆从头再来就是了。你的损失也就是一个下午的时间。如果你写1000行代码时采用了错误的设计，你还可以重构甚至从头再来，不会损失太多。  
>   
> 如果你是在建一栋房子，那么这个建造过程就会复杂得多，而糟糕的设计所引发的后果也更严重。狗屋与房子建造的重要区别就在于设计蓝图，也就是软件的架构设计上。

精心计划，并非意味着事无巨细的计划或者过度的计划。你可以把房屋结构性的支撑规划清楚，而在日后再决定是用木地板还是地毯。

### 架构的典型组成部分
1. 程序组织（Program Organnization），也即模块结构
2. 主要的类（Major Classes）
3. 数据设计（Data Design）
4. 用户界面设计（User Interface Design）
5. 资源管理（Resource Management）:预期的实现环境等
6. 安全性（Security）
7. 性能（Performance）
8. 可伸缩性（Scalability）:系统增长以满足未来需求的能力。如用户数量、服务器数量、网络节点数量、数据库记录数、数据库记录的长度等得增长
9. 互用性（Interoperability）:系统与其他软件或硬件共享数据或资源
10. 国际化/本地化（Internationality/Localization）
11. 输入输出（Input/Output）
12. 错误处理（Error Handling）
13. 容错性（Fault Tolerance）
14. 可行性（Feasibility）
15. 过度工程（Overengineering）
16. 买还是造决策（Buy-vs.-Build Decisions）:购买组件还是自己定制
17. 复用（Reuse）
18. 变更策略（Change Strategy）
19. 总体质量（General Architectural Quality）

架构设计需要
> 如果你不能向一个六岁的小孩解释某件事，那么你自己就没有真正理解它。
> ——Albert Einstein （爱因斯坦）

## 设计
### 关键的设计概念
***软件的首要技术使命是管理复杂度。***
> 有两种设计软件的方式：一种方法是让设计非常简单，看上去明显没有缺陷；另一种方法是让设计非常复杂，看上去没有明显缺陷。
> ——C.A.R Hoare

> 你已陷入复杂度的沼泽的一个现象就是，你发现自己顽固地用一种明显毫无作用的方法——至少在外人眼里。这就像是一个遇到车子抛锚的蠢货一样——他把水放到电池里然后把烟灰缸倒掉。
> ——P.J. Plauger

### 理想的设计特征
1. 最小的复杂度（Minimal complexity）
2. 易于维护（Ease of maintenance）
3. 松散耦合（loose coupling）
4. 可扩展性（extensibility）
5. 可重用性（reusability）
6. 高扇入（high fan-in）:让大量的类使用某个给定的类，即利用在较低层次上的工具类
7. 低扇出（low fan-out）:让一个类里少量或适中的使用其他的类
8. 可移植性（portability）
9. 精简性（leanness）:系统中没有多余的部分
10. 层次性（stratification）:系统应该能在任一层次上观察而不需要进入其他层次
11. 标准技术（Standard techniques）:尽量使用标准化的、常用的方法

### 设计的层次
<img src="../../images/levelsOfDesign.png">
系统首先被组织为子系统。子系统被进一步分解为类，然后类又被分解为子程序和数据。每个子程序的内部也需要进行设计。





## 未完待续...


[TOC]
