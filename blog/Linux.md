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


### 设置自定义的链接库路径 

```
export LD_LIBRARY_PATH=$HOME/lib:$LD_LIBRARY_PATH
```

### iptables设置
```
iptables -A INPUT -i lo -j ACCEPT
```
允许局域网所有连接

```
iptables -A INPUT -p tcp  --dport 8001:8004 -j REJECT
```
外网不允许访问8001到8004端口


[TOC]
