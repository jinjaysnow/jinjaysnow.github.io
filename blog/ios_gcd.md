author: Jin Jay
title: iOS多线程GCD
Date: 2015-01
description: iOS应用开发多线程GCD方式的描述。
keywords: iOS GCD
          iOS多线程

参考资源：http://blog.csdn.net/totogo2010/article/details/8016129
## 简介
Grand Central Dispatch 简称（GCD）是苹果公司开发多线程处理技术。GCD的工作原理是让一个程序，根据可用的处理资源，安排他们在任何可用的处理器核心上平行排队执行特定的任务。这个任务可以是一个函数或者一个程序段(block)。

## 常见用法
GCD中的队列为`dispatch queue`，主要有以下三种：
1. **Serial。** Serial queue通常用于同步访问特定的资源或数据。当你创建多个Serial queue时，虽然它们各自是同步执行的，但Serial queue与Serial queue之间是并发执行的。
2. **Concurrent。** 可以并发的执行多个任务，任务顺序是随机的。
3. **Main Dispatch Queue。** 全局可用的serial queue，在应用程序主线程上进行执行。

### dispatch_async
为了避免界面在处理耗时的操作时卡死，比如读取网络数据，IO,数据库读写等，我们可以在另外一个线程中处理这些操作，然后通知主线程更新界面。GCD处理代码框架如下：

    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        // 耗时的操作
        dispatch_async(dispatch_get_main_queue(), ^{
            // 更新界面
        });
    });

### dispatch\_group\_async
dispatch\_group\_async可以实现监听一组任务是否完成，完成后得到通知执行其他的操作。这个方法很有用，比如你执行三个下载任务，当三个任务都下载完成后你才通知界面说完成的了。示例代码：

    dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    dispatch_group_t group = dispatch_group_create();
    dispatch_group_async(group, queue, ^{
        [NSThread sleepForTimeInterval:1];
        NSLog(@"group1");
    });
    dispatch_group_async(group, queue, ^{
        [NSThread sleepForTimeInterval:2];
        NSLog(@"group2");
    });
    dispatch_group_async(group, queue, ^{
        [NSThread sleepForTimeInterval:3];
        NSLog(@"group3");
    });
    dispatch_group_notify(group, dispatch_get_main_queue(), ^{
        NSLog(@"updateUi");
    });
    dispatch_release(group);

### dispatch\_barrier\_async
dispatch\_barrier\_async是在前面的任务执行结束后它才执行，而且它后面的任务等它执行完成之后才会执行。示例代码：

    dispatch_queue_t queue = dispatch_queue_create("gcdtest.rongfzh.yc", DISPATCH_QUEUE_CONCURRENT);
    dispatch_async(queue, ^{
        [NSThread sleepForTimeInterval:2];
        NSLog(@"dispatch_async1");
    });
    dispatch_async(queue, ^{
        [NSThread sleepForTimeInterval:4];
        NSLog(@"dispatch_async2");
    });
    dispatch_barrier_async(queue, ^{
        NSLog(@"dispatch_barrier_async");
        [NSThread sleepForTimeInterval:4];
    });
    dispatch_async(queue, ^{
        [NSThread sleepForTimeInterval:1];
        NSLog(@"dispatch_async3");
    });

### dispatch\_apply 
执行某段代码n次。

    dispatch_apply(5, globalQ, ^(size_t index) {
        // 执行5次
    });


[TOC]