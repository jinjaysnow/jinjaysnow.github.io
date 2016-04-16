author: Jin Jay
title: 非特权用户安装zsh和Oh-My-Zsh
Date: 2016-04
description: 非特权用户安装zsh，并设定为默认shell，并安装Oh My Zsh插件。
keywords: zsh
          oh-my-zsh
          without root
          非特权用户

# 安装zsh
## 下载zsh源代码
下载最新发行版zsh源代码`http://www.zsh.org/pub/zsh.tar.gz`，解压后进入zsh源代码目录。

## 配置zsh编译安装选项
这里，主要设置zsh的安装目录，让zsh安装在用户目录下，供用户访问
```bash
./configure --prefix=$HOME/
```

## 编译安装
```bash
make && make install
```
zsh默认会安装到`$HOME/bin`目录下.

## 将zsh所在目录添加到PATH中，并设置zsh为默认shell
在主目录下的`.bash_profile`或`.bashrc`中添加如下代码：
```bash
export PATH=$PATH:$HOME/bin   # 添加PATH
export SHELL=`which zsh`      # 设置$SHELL为zsh
exec `which zsh` -l           # 设置登录为zsh
```
执行`source .bash_profile`或`source .bashrc`，显示
```sh
→~
```
则表明安装zsh成功.

# 安装Oh My Zsh
直接通过
```sh
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```

安装失败时，需要手动更改安装的shell脚本。首先下载脚本:

```sh
wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh
```

修改脚本，删除如下代码：
```sh
CHECK_ZSH_INSTALLED=$(grep /zsh$ /etc/shells | wc -l)
if [ ! $CHECK_ZSH_INSTALLED -ge 1 ]; then
    printf "${YELLOW}Zsh is not installed!${NORMAL} Please install zsh first!\n"
    exit
fi
unset CHECK_ZSH_INSTALLED
```

保存后退出，运行`sh install.sh`完成安装。


[TOC]
