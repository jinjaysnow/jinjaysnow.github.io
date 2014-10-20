Author: Jin Jay
Title: MPI并行程序设计
Date: 2014-10
description: MPI并行程序设计相关学习。学习资料来源：清华大学《高性能计算之并行编程技术——MPI并行程序设计》。
keywords: MPI
          Mac OS

# MPI并行程序设计
学习资料主要来源：清华大学《高性能计算之并行编程技术——MPI并行程序设计》。

## MPI简介
1. MPI是一个库，而不是一门语言。
2. MPI是一种标准或规范的代表，而不特指某一个对它的具体实现。所有并行计算机制造商都提供对MPI的支持，可以在网上免费得到MPI在不同并行计算技上的实现，一个正确的MPI程序，可以不加修改地在所有的并行计算机上运行。
3. MPI是一种消息传递编程模型。MPI的最终目的是服务于进程间通信这一目标的。

## Open-MPI安装
本文主要使用[OpenMPI](http://www.open-mpi.org/)这个实现版本。计算机为Mac mini 2012年版本，运行Mac OS，Intel i5处理器。语言采用C和C++。  
步骤：  
1. 在[http://www.open-mpi.org/](http://www.open-mpi.org/)下载界面下载最新的稳定版本源代码压缩包
2. 解压缩，进入源代码目录
3. `./configure`
4. `make all install`
5. 完毕
6. 可以进入[http://mtt.open-mpi.org/](http://mtt.open-mpi.org/)进行在线测试是否安装成功。

## 第一个程序hello world
```
#include "mpi.h"
#include <stdio.h>
#include <math.h>

int main(int argc, char *argv[]) {
    int myid, numprocs;
    int namelen;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
    MPI_Get_processor_name(processor_name, &namelen);

    fprintf(stderr, "To beautiful you! Process %d of %d on %s\n", myid, numprocs, processor_name);
    MPI_Finalize();

    return 0;
}
```

## 编译运行

```
# 编译,将source.c文件编译成可运行文件source
mpicc source.c -o source   # C
mpiCC source.cc -o source  # C++
mpic++ source.cc -o source # C++,用于大小写敏感的文件系统

# 运行,并行程序需要多个进程,故需要开启多个源程序进行运算
mpiexec -n 2 ./source
```
e.g. 编译运行第一个程序hello world得到的结果为：
```
To beautiful you! Process 0 of 2 on tp2
To beautiful you! Process 1 of 2 on tp1
```
## To be continued...未完待续
**由于缺少多个CPU共同组成的计算机系统，多核与并行程序设计学习不能更有效的进行，所以暂时停止MPI的学习。**


[TOC]