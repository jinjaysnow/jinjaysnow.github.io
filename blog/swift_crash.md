Title:   Swift Project Crash
Brief:   New Swift Project Crash at startup.
Authors: Jin Jay
Description: 解决新建Swift项目真机运行时报错：dyld: Library not loaded: @rpath/libswiftCore.dylib。
Date:    2015-08
keywords:   dyld
            swift
            rpath
            dyld: Library not loaded: @rpath/libswiftCore.dylib


### dyld: Library not loaded: @rpath/libswiftCore.dylib Error
新建Swift项目，真机运行时出现上述标题错误时，可以采用如下链接中给出的方法进行调试：http://stackoverflow.com/questions/26024100/dyld-library-not-loaded-rpath-libswiftcore-dylib 。

我个人的电脑上使用的是将“Keychain Access”（钥匙串访问）中的相应证书中的信任从**始终信任**切换为**使用系统默认**来解决的这个问题。

![](http://ijinjay.github.io/images/keychain_trust.png)

[TOC]
