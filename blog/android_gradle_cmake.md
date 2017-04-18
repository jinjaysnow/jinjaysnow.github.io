author: Jin Jay
title: Android Gradle Cmake
Date: 2017-04
description: 使用Android Studio进行Android Native应用开发，选用Gradle和CMake构建工具的组合。介绍如何添加预构建的第三方库。
keywords: Android
          cmake
          gradle

本文介绍使用Android Studio进行Android的C/C++项目开发。构建工具使用Gradle和CMake的组合，这个组合是Android Studio的默认组合。主要讲解添加第三方预构建库，及使用方法。

进行Android Native应用开发的前提是安装必要的工具，可使用Android Studio自带的Android SDK Tools管理工具，下载安装CMake, Android SDK Platform-Tools, Android SDK Build-Tools, NDK。

# 新建C/C++工程
直接使用Android Studio新建空的Native项目，自动生成的主要文件有:

```CMake
build.gradle                         # gradle配置文件
CMakeLists.txt                       # CMake配置文件
src/main/java/**/MainActivity.java   # 应用入口
src/main/cpp/native-lib.cpp          # Native开发示例文件
```

# 添加第三方预构建库
作为示例，以添加Google Tango的`libtango_client_api.so`和`libtango_support_api.so`为例，介绍用法。

## 第三方预构建库的结构

```
libtango_client_api
  |----include
        |----tango_client_api.h
  |----lib
        |----arm64-v8a
               |----libtango_client_api.so
        |----armeabi-v7a
               |----libtango_client_api.so
        |----x86
               |----libtango_client_api.so
```

`libtango_support_api`结构与`libtango_client_api`结构类似，都有`include`文件夹和`lib`文件夹，`lib`文件夹下有预编译好的不同的`ABI`平台的库文件。

假定将库文件加放置在`src`文件夹下。项目名为`SenseDataApp`，自动生成的源文件`native-lib.cpp`更名为`SenseDataApp.cpp`。

## 修改CMakeLists.txt添加构建依赖

`CMakeLists.txt`文件主要配置include路径和库文件路径，在构建过程中使得目标库能够正常构建。

```CMake
cmake_minimum_required(VERSION 3.4.1)
# 添加include路径
include_directories(src/lib_tango_client_api/include
                    src/lib_tango_support_api/include
                    src/main/cpp)
# 设置目标库
add_library( sense-data-app
             SHARED
             src/main/cpp/SenseDataApp.cpp )

# log库为Android自带的库，使用find_library(变量名 库名) 命令可自动找出log库的依赖
find_library( log-lib log )

# 添加tango库文件及指定库文件位置
add_library(Tango_LIBRARY SHARED IMPORTED)
set_target_properties( Tango_LIBRARY
                       PROPERTIES IMPORTED_LOCATION
                       # ${CMAKE_CURRENT_SOURCE_DIR}指代CMakeLists.txt文件的位置，为了确保能够找到库文件，使用绝对路径
                       # ${ANDROID_ABI}可以指代不同ABI平台对应的字符串
                       ${CMAKE_CURRENT_SOURCE_DIR}/src/lib_tango_client_api/lib/${ANDROID_ABI}/libtango_client_api.so )

add_library(Tango_support_LIBRARY SHARED IMPORTED)
set_target_properties( Tango_support_LIBRARY
                       PROPERTIES IMPORTED_LOCATION
                       ${CMAKE_CURRENT_SOURCE_DIR}/src/lib_tango_support_api/lib/${ANDROID_ABI}/libtango_support_api.so )

# 配置库的依赖关系
target_link_libraries( sense-data-app
                       ${log-lib}
                       Tango_LIBRARY
                       Tango_support_LIBRARY )
```

## 配置build.gradle文件

`build.gradle`主要配置ABI信息和将预编译的库文件打包到最终的apk文件中。**如果不配置库文件的打包，会出现运行时的`library not found`错误。**

```Groovy
android {
    defaultConfig {
        // 指定平台对应的abi
        ndk {
            abiFilters 'x86', 'armeabi-v7a', 'arm64-v8a'
        }
    }
   externalNativeBuild {
        cmake {
            path "CMakeLists.txt"
        }
    }
    // 设置jni库文件位置，打包到apk中
    sourceSets.main {
        jniLibs.srcDirs = ["src/lib_tango_client_api/lib", "src/lib_tango_support_api/lib"]
    }
}
```

## 添加库文件加载代码
由于已进将依赖关系写入到目标库`sense-data-app`中，故而只需加载`sensedataapp`动态库即可。

在`MainActivity.java`的`MainActivity`类中添加如下代码:

```
static {
    System.loadLibrary("sense-data-app");
}
```

在Android Studio中点击构建即可正常构建运行。

[TOC]