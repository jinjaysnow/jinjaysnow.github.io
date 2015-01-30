author: Jin Jay
title: iOS隐藏状态栏
Date: 2015-01
description: iOS应用开发，隐藏状态栏。
keywords: iOS开发
          隐藏状态栏

## 方法一
在ViewController中，调用相应的方法。

    - (BOOL)prefersStatusBarHidden {
        return YES;
    }
在viewDidLoad方法中调用上面的函数

    [self prefersStatusBarHidden];

## 方法二
修改plist文件

    Status bar is initially hidden 设为 YES
    View controller-based status bar appearance 设为 NO

[TOC]