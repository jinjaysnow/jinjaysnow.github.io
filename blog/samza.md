author: Jin Jay
title: LinkedIn Samza
Date: 2016-05
description: LinkedIn Samza所使用的故障恢复方法。
keywords: LinkedIn
          Samza

调研当前的流数据处理系统所使用的故障恢复方法，比较优缺点。

# Samza简介
Samza是一个流处理框架:

- 简单的API:不像大多数低层级的消息系统的API，Samza提供了一个非常简单的，基于回调的 “消息处理”  API，和MapReduce类似。
- 受控的状态：Samza管理“流处理器”的快照和恢复。当一个流处理器重启，Samza会恢复它的状态到一个一致的快照。Samza被构建来处理大规模的状态(每个分区数GB).
- 容错：当集群中的任何一个机器发生故障，Samza和YARN一起透明地迁移你的task到另一台机器。
- Durability持久性: Samza使用Kafka来保证消息按照他们写入一个partition的顺序被处理，并且不会有消息丢失。
- Scalability可扩展:Samza在各个层面上都是分区的以及分布式的。Kafka提供了有序的、分区的、可回放的、容错的消息流。YARN提供给Samza容器一个分布式的环境来运行。
- Pluggable可插拔的:虽然Samza自带对Kafka和YARN的支持，但是Samza同时提供了可插拔的API来让你在别的消息系统和运行环境中运行Samza。
- Processor isolation处理器隔离:Samza与Apache YARN一起工作。YARN提供了Hadoop的安全模型，以及利用Linux CGruops的资源隔离。

# Samza中的故障恢复方法
Samza提供了一个checkpoint检查点的机制，即使一个job崩溃，或机器宕机，网络故障或者其他情况下，Samza能保证消息不会丢失。

如果一个Samza的组件出现故障，需要将组件重启(一般在另一台机器上)并恢复处理。为了实现这个过程，一个组件定时为每一个任务实例的当前的状态创建检查点。

<center>![offset](https://samza.apache.org/img/0.7.0/learn/documentation/container/checkpointing.svg)</center>

当一个Samza组件启动时，会寻找最近的检查点，并从该检查点处开始消费消息流。如果前一个组件出现故障，最近的检查点可能与当前的位置有一个微小的滞后(也即，这个job在上一次检查点写入后可能已经消费了一些消息)，但是我们不能确定。在这种情况下，这个job可能再次处理这一小部分消息。

这个保证被称为“至少一次处理”：Samza保证job不会丢失任何消息，即使组件重启。然而，对于job来说，在一个组件重启时，它可能会看到某一个相同消息超过一次。

# 参考文献
[Apache Samza官方文档](https://samza.apache.org/learn/documentation/0.7.0)

[TOC]























