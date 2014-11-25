Title: Django & Tornado
Date: 2014-09
Author: Jin Jay
description: Django与Tornado的简单比较。
Keywords: Django, Tornado

### Django & Tornado
Django 和 Tornado是Python众多web框架中常用的两种，这里简单比较一下两个框架。
#### Django
Django是走大而全的方向，它最出名的是其全自动化的管理后台：只需要使用起ORM(Object Relational Mapping 对象关系映射)，做简单的对象定义，它就能自动生成数据库结构、以及全功能的管理后台。Django适用的是中小型的网站，或者是作为大型网站快速实现产品雏形的工具。Django模版机制比较大的争议是在它不允许在模本中使用编程。Django有着清晰的MVC设计结构，有View层，Control层，还有Model层。在使用Django的时候，它便引导你按照这个思路做下去。
此外，作为一个成熟的框架，Django拥有很多其他的特性：用户验证、本地化、处理unicode等等。

#### Tornado
Tornado是Facebook开源的框架，较之Django，它更轻量级。它可以在一秒钟内处理数以千计的连接。不过Tornado并没有内建数据库连接。
Tornado使用异步的事件处理方式，即它可以处理其它的连接当正在等待内核处理事件的时候。有的说法也叫非阻塞式服务器，即服务器不会因某一个连接等待内核处理而阻塞。

#### 怎样选择？
在Django和Tornado之间选择，首先要清楚你要构建的网站的类型、团队水平还有你准备花多大精力在上面。Django适合初学者和需要快速构建的网站，因为它隐藏了很多细节。Tornado则更适合有经验的开发者开发更大规模的应用，它需要开发者花更大的精力去构建。如果团队是分散的，Django提供更好的工具去管理结构并集成数据，而Tornado没有提供任何内建的类似的工具。如果你的应用对实时性要求较高(更多的连接，更快的处理速度)，Tornado的非阻塞特性能够带给你很多便利，不过用好这个特性的前提是你的团队的技术水平较高。




[TOC]