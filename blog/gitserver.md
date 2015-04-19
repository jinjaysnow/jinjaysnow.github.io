Title:  Git服务器搭建
Authors: Jin Jay
Date:    2014-11
Description: 搭建git服务器，拥有自己的远程代码仓库。
keywords: git server debian
          git服务器搭建


# Git服务器搭建
参考文档：[搭建Git服务器](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/00137583770360579bc4b458f044ce7afed3df579123eca000)

## 安装git

    sudo apt-get install git
## 创建一个git用户,用来运行git服务

    sudo adduser git
## 创建证书登陆
收集所有需要登录的用户的公钥，就是他们自己的`id_rsa.pub`文件，把所有公钥导入到`/home/git/.ssh/authorized_keys`文件里，一行一个。
# 初始化Git仓库
先选定一个目录作为Git仓库，假定是/sources/test.git，在/sources目录下输入命令：

    sudo git init --bare test.git
Git就会创建一个裸仓库，裸仓库没有工作区，因为服务器上的Git仓库纯粹是为了共享，所以不让用户直接登录到服务器上去改工作区，并且服务器上的Git仓库通常都以.git结尾。然后，把owner改为git：

    sudo chown -R git:git test.git
## 禁用shell登录：
出于安全考虑，第二步创建的git用户不允许登录shell，这可以通过编辑/etc/passwd文件完成。找到类似下面的一行：

    git:x:1001:1001:,,,:/home/git:/bin/bash
改为：

    git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
这样，git用户可以正常通过ssh使用git，但无法登录shell，因为我们为git用户指定的git-shell每次一登录就自动退出。

## 克隆远程仓库
现在，可以通过git clone命令克隆远程仓库了，在各自的电脑上运行

    git clone git@server:sources/test.git













[TOC]
