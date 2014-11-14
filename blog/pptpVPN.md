Title:  搭建基于PPTP协议的VPN
Author: Jin Jay
Date:    2014-10
description: 搭建基于PPTP搭建VPN。
keywords:   pptp
            VPN


# 搭建基于PPTP协议的VPN
## PPTP配置
### 安装PPTP

    sudo apt-get install pptpd

### 修改配置文件

    sudo vim /etc/pptpd.conf
将文件最后两行注释的内容更改为未注释状态

    localip 192.168.0.1
    remoteip 192.168.2.10-100
这里localip是VPN连接后服务器的IP地址，remoteip是客户端可分配的IP范围。

### 编辑DNS配置

    sudo vim /etc/ppp/pptpd-options
找到ms-dns这项，去掉前面的#号，修改为Google的DNS

    ms-dns 8.8.8.8
    ms-dns 8.8.4.4

### 添加VPN账号

    sudo vim /etc/ppp/chap-secrets
添加账号密码，样例：

    # Secrets for authentication using CHAP
    # client        server  secret                  IP addresses
    "test"          pptpd   "test12345678"          *
账号密码用双引号括起来保证是一个完整的字符串，无二义。

## 配置NAT
### 开启ipv4 forward

    sudo vim /etc/sysctl.conf
添加内容

    net.ipv4.ip_forward=1
保存退出后运行命令

    sudo sysctl -p

### 建立NAT
使用以下命令安装iptables

    sudo apt-get install iptables
安装成功后，运行命令：

    iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -o eth0 -j MASQUERADE
将客户端的信息转交给eth0网卡转发。`192.168.2.0/24`修改为自己定义的客户端IP范围，`eth0`修改为自己的网卡代码(使用`ifconfig`查看)。

### 保存NAT配置

    sudo iptables-save > /etc/pptpd.conf
    sudo vim /etc/network/interfaces
在eth0后面加上一句：
    
    pre-up iptables-restore < /etc/iptables-rules
这样每次重启后，iptables不会丢失。

## 开启服务

    sudo /etc/init.d/pptpd restart




[TOC]