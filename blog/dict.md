title: C语言实现字典结构
description: C语言实现字典结构(dict)，字典结构是键值结构，可以通过关键字获取相应的值，很多语言自带此种结构，比如Python。这里我们使用C语言实现一个字典数据类型。
date: 2014-11
keywords: C语言 字典
          C dict
          C redis dict


# 简介
C语言实现字典结构(dict)，字典结构是键值结构，可以通过关键字获取相应的值，很多语言自带此种结构，比如Python。这里我们使用C语言实现一个字典数据类型，主要参考的是redis中对字典的实现。

# 设计
## 外部接口设计
字典是一种数据类型，故定义：

    typedef struct dict Dict;

一些基本的字典操作函数：

| 操作 | 函数 | 算法复杂度 |
|-----|------|---------|
| 创建一个新字典 | dictCreate | O(1) |
| 添加新键值对到字典 | dictAdd | O(1) |
| 添加或更新给定键的值  | dictReplace | O(1) |
| 在字典中查找给定键所在的节点  | dictFind    | O(1) |
| 在字典中查找给定键的值 | dictFetchValue  | O(1) |
| 从字典中随机返回一个节点    | dictGetRandomKey    | O(1) |
| 根据给定键，删除字典中的键值对 | dictDelete  | O(1) |
| 清空并释放字典 | dictRelease | O(N) |
| 清空并重置（但不释放）字典   | dictEmpty   | O(N) |
| 缩小字典    | dictResize  | O(N) |
| 扩大字典    | dictExpand  | O(N) |
| 对字典进行给定步数的rehash   | dictRehash  | O(N) |
| 在给定毫秒内，对字典进行rehash  | dictRehashMilliseconds  | O(N) |







[TOC]
