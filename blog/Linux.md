Title: Linux基本操作
Author: Jin Jay
Date: 2014-10
description: Linux基本操作：创建新用户、修改密码、修改用户信息、从远程服务器拷贝。
keywords: Linux

## Linux相关操作
### 创建新用户

    usradd -d /usr/Jay -m Jay   # 创建一个用户名为Jay,用户目录为/usr/Jay的账户

### 修改密码

    passwd Jay  # 修改用户Jay的密码

### 修改用户信息

    usermod Jay

### 从远程服务器拷贝

    scp Jay@myserver:path2file1 file2


### export LD_LIBRARY_PATH=$HOME/lib:$LD_LIBRARY_PATH


[TOC]
