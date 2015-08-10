title: Mac常用操作
description: Mac基本操作：使用updatedb、使用gdb、快速查找mdfind等。
date: 2014-11
author: Jin Jay
        靳杰
keywords: Mac updatedb
          Mac OS X gdb

# Mac系统上的基本操作
## updatedb

	sudo ln -s /usr/libexec/locate.updatedb /usr/local/bin/updatedb
通过上面的命令，可以生成一个链接，每次只需要使用`sudo updatedb`即可更新查找数据库。

## 使用gdb
### 安装gdb

    brew tap homebrew/dupes
    brew install gdb
### 新建一个证书
打开“钥匙串访问”程序，在主菜单选择**“证书助理”>“创建证书”**
![gdb1](http://jinjaysnow.github.io/static/gdb/gdb1.png)

然后输入证书名，比如`gdb-cert`，将证书类型更改为“代码签名”，并**勾选“让我覆盖这些默认值”**(`截图未勾选`)
![gdb2](http://jinjaysnow.github.io/static/gdb/gdb2.png)

继续，输入有效期，最大为999，我输入的是999
![gdb3](http://jinjaysnow.github.io/static/gdb/gdb3.png)

一直继续，直到指定证书的位置为“系统”
![gdb4](http://jinjaysnow.github.io/static/gdb/gdb4.png)

点击创建
![gdb5](http://jinjaysnow.github.io/static/gdb/gdb5.png)

成功创建

### 确保证书始终被信任
右击证书，选择“显示简介”
![gdb6](http://jinjaysnow.github.io/static/gdb/gdb6.png)

展开“信任”，将代码签名处的值更改为**始终信任**
![gdb7](http://jinjaysnow.github.io/static/gdb/gdb7.png)

### 对GDB签名

    codesign -s gdb-cert $(which gdb)
输入用户名和密码后成功

## mdfind
mdfind是find与locate的结合版本，能够非常快速的匹配查找需要的内容，需要配合updatedb使用。


[TOC]
