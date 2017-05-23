author: Jin Jay
title: CMake使用
Date: 2017-04
description: CMake文档中文翻译，使用入门。
keywords: cmake
          中文翻译
          使用入门

# cmake构建系统
基于CMake的构建系统组织为一系列的高层次的逻辑目标。每一个目标对应一个可执行文件或库文件，或是一个包含自定义命令的自定义目标文件。目标之间依赖关系在cmake构建系统中表示,来确定构建的顺序和响应改变的规则。

## 二进制目标
可执行文件和库文件使用`add_executale()`和`add_library()`来命令来定义。生成的文件会有平台相关的特定的前缀、后缀和扩展名。二进制目标间的依赖关系使用`target_link_libraries()`命令来表示。

```CMake
add_library(archive archive.cpp zip.cpp lzma.cpp)
add_executable(zipapp zipapp.cpp)
target_link_libraries(zipapp archive)
```

上述例子中`arvhive`被定义为一个静态库，包含来自`archive.cpp`, `zip.cpp`, `lzma.cpp`的编译后的对象。`zipapp`是一个可执行文件通过编译链接`zipapp.cpp`得到。在链接`zipapp`可执行文件时，`archive`静态库会被链入。

### 二进制可执行文件
`add_executable()`命令定义一个可执行目标：

```CMake
add_executable(mytool mytool.cpp)
```

类似于`add_custom_command(COMMAND)`这种在构建时产生可运行规则的命令，可以使用一个`EXECUTABLE`目标作为`COMMAND`。构建系统规则会保证在运行这个命令前构建出这个可执行文件。

### 二进制库类型
#### 一般库文件
默认情况下，`add_library()`命令定义一个静态库，除非指定一个特定的类型。指定类型可以使用下面的命令格式

```CMake
add_library(archive SHARED archive.cpp zip.cpp lzma.cpp)
add_library(archive STATIC archive.cpp zip.cpp lzma.cpp)
```

`BUILD_SHARED_LIBS`变量会改变`add_library()`的默认构建行为。

总的来说，某一个库是`SHARED`或`STATIC`基本不会对构建系统有影响——命令，依赖配置和其它API的工作过程与库类型无关。但`MODULE`库类型比较特殊，这个库生成后并不参与链接——也即不会用于`target_link_libraries`命令中。`MODULE`库类型是使用运行时技术作为一个插件被加载。如果库并不导出任何非托管的符号(比如，Windows DLL，C++/CLI DLL)，那么这个库需要设定为不是一个`SHARED`类型的库，因为CMake要求`SHARED`类型库导出至少一个符号。

```CMake
add_library(archive MODULE 7z.cpp)
```

##### Apple Frameworks
一个`SHARED`类型库在OS X和iOS Framework Bundle下需要被标记`FRAMEWORK`属性。`MAOSX_FRAMEWORK_IDENTIFIER`设置`CFBundleIdentifier`键并唯一表示这个bundle.

```CMake
add_library(MyFramework SHARED MyFramework.cpp)
set_target_properties(MyFramework PROPERTIES
    FRAMEWORK TRUE
    FRAMEWORK_VERSION A
    MACOSX_FRAMEWORK_IDENTIFIER org.cmake.MyFramework
)
```

#### 对象库
`OBJECT`库类型也是不参与链接的类型。它定义了参与编译的源文件的对象文件的集合。对象文件集合可以用于作为其他目标的源输入。

```CMake
add_library(archive OBJECT archive.app zip.cpp lzma.cpp)
add_library(archive_Extras STATIC $<TARGET_OBJECTS:archive> extras.cpp)
add_library(test_exe $<TARGET_OBJECTS:archive> test.cpp)
```

`OBJECT`类型库只能在构建系统中作为源输入使用——不能安装、导出或在`target_link_libraries()`中使用——也不可以作为`TARGET`在`add_custom_command(TARGET)`中使用。
虽然对象类型库在`target_link_libraries()`中不能直接使用，但是，可以使用一个`INTERFACE_SOURCES`目标属性设置为`$<TARGET_OBJETS:ojblib>`的接口库间接地链接。

## 构建配置和使用要求
`target_include_directories()`, `target_compile_definitions()`和`target_compile_options()`命令用来配置构建系统及二进制目标的使用要求。这些命令分别指定了`INCLUDE_DIRECTORIES`, `COMPILE_DEFINITIONS`和`COMPILE_OPTIONS`目标属性，以及`INTERFACE_INCLUDE_DIRECTORIES`, `INTERFACE_COMPILE_DEFINITIONS`和`INTERFACE_COMPILE_OPTIONS`目标属性。

每一个命令有`PRIVATE`, `PUBLIC`和`INTERFACE`模式。`PRIVATE`模式指定目标属性的非接口变量；`INTERFACE`模式指定接口变量；`PUBLIC`模式指定非接口和接口变量。

```CMake
target_compile_definitions(archive
    PRIVATE BUILDING_WITH_LZMA
    INTERFACE USING_ARCHIVE_LIB
)
```

### 目标属性
`INCLUDE_DIRECTORIES`属性会按照属性的出现顺序添加`-I`或`-isystem`前缀到编译器命令。
`COMPILE_DEFINITIONS`属性会按照一个未指定的顺序添加`-D`或`/D`前缀到编译器命令。`DEFINE_SYMBOL`目标属性也会作为一个编译器定义量`SHARED`或`MODULE`添加。
`COMPILE_OPTIONS`会在shell中转义并添加，一些编译选项有特殊的处理，比如`POSITION_INDEPENDENT_CODE`。

`INTERFACE_`开头的目标属性是使用要求声明——指定必须使用的内容需要正确编译并链接，对任意的二进制目标，每个目标上在`target_link_libraries9)`命令中指定的每一个`INTERFACE_`属性的内容会被采用。

```CMake
set(srcs archive.cpp zip.cpp)
if (LZMA_FOUND)
  list(APPEND srcs lzma.cpp)
endif()
add_library(archive SHARED ${srcs})
if (LZMA_FOUND)
  # archive库源文件使用-DBUILDING_WITH_LZMA选项编译
  target_compile_definitions(archive PRIVATE BUILDING_WITH_LZMA)
endif()
target_compile_definitions(archive INTERFACE USING_ARCHIVE_LIB)

add_executable(consumer)
# 使用-DUSING_ARCHIVE_LIB来链接构建consumer
target_link_libraries(consumer archive)
```

因而一般需要源目录和相应的构建目录添加到`INCLUDE_DIRECTORIES`，`CMAKE_INCLUDE_CURRENT_DIR`变量可以用来添加相应的目录到所有目标的`INCLUDE_DIRECTORIES`中。变量`CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE`可以开启来添加相应的`INTERFACE_INCLUDE_DIRECTORIES`。

### 传递使用要求
目标的使用要求可以传递给依赖者。`target_link_libraries()`命令有`PRIVATE`, `INTERFACE`和`PUBLIC`关键词来控制这个传播。

```CMake
add_library(archive archive.cpp)
target_compile_definitions(archive INTERFACE USING_ARCHIVE_LIB)

add_library(serialization serialization.cpp)
target_compile_definitions(serialization INTERFACE USING_SERIALIZATION_LIB)

add_library(archiveExtras extras.cpp)
target_link_libraries(archiveExtras PUBLIC archive)
target_link_libraries(archiveExtras PRIVATE serialization)
# archiveExtras使用-DUSING_ARCHIVE_LIB和-DUSING_SERIALIZATION_LIB编译

add_executable(consumer consumer.cpp)
# consumer使用—DUSING_ARCHIVE_LIB编译
target_link_libraries(consumer archiveExtras)
```

### 兼容接口属性

### 属性来源调试

### 使用产生器表达式配置构建
构建配置可以使用`generator expressions`来包括一些内容。

```CMake
add_library(lib1Version2 SHARED lib1_v2.cpp)
set_property(TARGET lib1Version2 PROPERTY INTERFACE_CONTAINER_SIZE_REQUIRED 200)
set_property(TARGET lib1Version2 APPEND PROPERTY
  COMPATIBLE_INTERFACE_NUMBER_MAX CONTAINER_SIZE_REQUIRED
)

add_executable(exe1 exe1.cpp)
target_link_libraries(exe1 lib1Version2)
target_compile_definitions(exe1 PRIVATE
    CONTAINER_SIZE=$<TARGET_PROPERTY:CONTAINER_SIZE_REQUIRED>
)
```

示例中，`exe1`源文件会使用`-DCONTAINER_SIZE=200`来编译。

#### include目录和使用要求
在指定位置使用要求时include目录需要额外考虑。`target_include_directories()`命令用于此处。

```CMake
add_library(lib1 lib1.cpp)
target_include_directories(lib1 PRIVATE
  /absolute/path
  relative/path
)
```

#### 链接库与产生器表达式

```CMake
add_library(lib1 lib1.cpp)
add_library(lib2 lib2.cpp)
target_link_libraries(lib1 PUBLIC
  $<$<TARGET_PROPERTY:POSITION_INDEPENDENT_CODE>:lib2>
)
add_library(lib3 lib3.cpp)
set_property(TARGET lib3 PROPERTY INTERFACE_POSITION_INDEPENDENT_CODE ON)

add_executable(exe1 exe1.cpp)
target_link_libraries(exe1 lib1 lib3)
```

### 接口库

接口库主要使用场景是只有头文件的库，比如`Eigen`库。

```CMake
add_library(Eigen INTERFACE)
target_include_directories(Eigen INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
  $<INSTALL_INTERFACE:include/Eigen>
)

add_executable(exe1 exe1.cpp)
target_link_libraries(exe1 Eigen)
```

这里`Eigen`目标的使用要求在编译时就生效了，在链接时并不生效。

# CMake命令

常用命令列表

命令 | 描述
:---|:---
add_compile_options  | 添加编译选项
add_custom_command | 添加自定义的构建规则
add_custom_target | 添加自定义目标
add_definitions | 添加`-D`定义标志到源文件的编译过程
add_dependencies | 在顶级目标间添加依赖
add_executable | 添加一个可执行文件并指定源文件
add_library | 添加库文件对象
add_subdirectory | 添加一个构建的子目录
aux_source_directory | 找出一个目录下的所有源文件
break | while语句break
cmake_host_system_information | 查询目标系统的配置信息
cmake_minimum_required | 配置需要的最小cmake版本
cmake_parse_arguments | 在宏或函数中解析参数
cmake_policy | 设置CMake policy
configure_file | 赋值文件到另一个位置并更改内容
continue | while语句continue
create_test_sourcelist | 创建测试源文件列表构建测试程序
define_property | 定义和管理自定义属性
elseif, else | 用于判断语句
enable_language | 开启特定的语言支持 
enable_testing | 开启测试
end(foreach,function,if,macro,while) | 语句结束
execute_process | 执行一个或多个子进程
export | 从构建树导出目标给外部项目使用
file | 文件读写操作命令
find_file | 找出一个文件的全路径
find_library | 搜索一个库
find_package | 搜索并加载外部项目的设置
find_path | 查找包含一个文件的路径
find_program | 查找一个可执行程序，未找到时返回-NOTFOUND
foreach,if,function | 命令关键字
get_cmake_property | 获取cmake属性
get_directory_property | 获取目录属性
get_filename_component | 获取一个文件的组件
get_(source_file,target,test)_property | 属性获取
include_directories | 添加include目录
include_regular_expression | 设置在依赖检测时使用的正则表达式
include | 加载并运行在一个文件或**模块**中的cmake代码
install | 生成项目的安装规则
link_directories | 指定库搜寻的目录
link_libraries | 链接库到目标
list | 列表操作，后接其他命令，如LENGTH,FIND INSERT,SORT
load_cache | 从另一个项目的cmake缓存中加载值
macro | 定义宏
math | 数学表达式
message | 输出信息
option | 提供用户可以选择开启或关闭的选项
project | 定义项目相关信息
remove_definitions | 移除`-D`选项
return | 从一个文件，目录或函数返回
separate_arguments | 解析以空格分开的参数到为一个逗号分隔的列表
set_directory_properties | 设置目录属性
set_property | 设置属性
set | 设置变量
set_(source_files,target,tests)_properties | 设置顺序性
source_group | 定义源文件组来用于IDE项目生成
string | 字符串操作，FIND,REPLACE,APPEND等
target_compile_definitions | 目标编译声明
target_compile_features | 编译特性
target_compile_options | 目标编译选项
target_include_directories | 给目标添加include目录
target_link_libraries | 目标链接库
target_sources | 给目标添加源文件
try_compile | 尝试编译源代码
try_run | 尝试运行可执行程序
unset | 取消变量设置
variable_watch | 变量值改变检测
while | 循环

# CMake编译特性
项目源文件可能依赖于编译器的一些特性，主要有三种使用场景：编译器特性要求，可选的编译特性和条件编译选项。

## 编译器特性要求
使用`target_compile_features()`来指定特性需求，例如需要编译器支持`cxx_constexpr`特性。

```CMake
add_library(mylib requires_constexpr.cpp)
target_compile_features(mylib PRIVATE cxx_constexpr)
```

CMake处理时会确保使用的C++编译器兼容这个特性，并添加必要的标志，比如`-std=gnu++11`，如果不兼容则返回`FATAL_ERROR`。

## 可选的编译器特性
编译器拥有某一个特性时采用该特性，否则不采用。

## 条件编译选项

```CMake
add_library(foo INTERFACE)
set(with_variadics ${CMAKE_CURRENT_SOURCE_DIR}/with_variadics)
set(no_variadics ${CMAKE_CURRENT_SOURCE_DIR}/no_variadics)
target_include_directories(foo
    INTERFACE
    "$<$<COMPILE_FEATURES:cxx_variadic_templates>:${with_variadics}>"
    "$<$<NOT:$<COMPILE_FEATURES:cxx_variadic_templates>>:${no_variadics}>"
)
```

# CMake产生式
产生式(generator expressions)在构建系统生成过程中产生构建配置特定的信息。产生式可以用于条件链接，条件定义等。

## 逻辑表达式
逻辑表达式用于产生条件输出，基本的表达式是0和1，因为其它的逻辑表达式计算结果为0或1，可以组合为条件输出。

```CMake
$<$<CONFIG:Debug>:DEBUG_MODE>
```

在`Debug`配置使用时，展开`DEBUG_MODE`，否则不展开。

```CMake
add_executable(myapp main.cpp foo.c bar.cpp)
target_compile_definitions(myapp
  PRIVATE $<$<COMPILE_LANGUAGE:CXX>:COMPILING_CXX>
)
target_include_directories(myapp
  PRIVATE $<$<COMPILE_LANGUAGE:CXX>:/opt/foo/cxx_headers>
)
```

## 信息表达式

```CMake
include_directories(/usr/include/$<CXX_COMPILER_ID>/)
```

常用表达式 | 描述
:---|:---
$<CONFIG\> | 配置文件名
$<PLATFORM_ID\> | 平台的CMake ID
$<C(XX)_COMPILER_ID\> | 编译器ID
$<C(XX)_COMPILER_VERSION\> | 编译器版本
$<TARGET_FILE:target\> | 目标文件的全路径
$<TARGET_FILE_NAME:target\> | 目标文件名(.exe, .so.1.2, .a)
$<TARGET_FILE_DIR:target\> | 目标文件的文件夹
$<TARGET_LINKER_FILE:target\> | 目标文件使用的链接文件
$<TARGET_LINKER_FILE_(NAME,DIR):target\> | 目标文件使用的链接文件名称，路径
$<TARGET_SONAME_FILE_(NAME,DIR):target\> | 目标文件相关的so文件信息
$<TARGET_PDB_FILE_(NAME,DIR):target\> | 目标文件相关的pdb文件信息
$<INSTALL_PREFIX\> | 安装前缀
$<COMPILE_LANGUAGE\> | 源文件的编译语言

## 输出表达式

```CMake
-I$<JOIN:$<TARGET_PROPERTY:INCLUDE_DIRECTORIES>, -I>
```

示例生成在`INCLUDE_DIRECTOIRES`目标属性中的字符串，并使用`-I`前缀。

常用输出表达式 | 描述
:----|:-----
$<0:...\> | 空字符串
$<1:...\> | ...中的内容
$<JOIN:list, ...\>| 将...中的内容于list内容组合
$<ANGLE-R\> | 符号`>`
$<COMMA\> | 符号`.`
$<SEMICOLON\> | 符号`;`
$<TARGET_NAME:...\> | 标记...为一个目标的名字
$<LINK_ONLY:...\> | 只有在链接时产生内容，否则为空
$<INSTALL_INTERFACE:...\> | 在使用`install(EXPORT)`时产生内容，否则为空字符串
$<BUILD_INTERFACE:...\> | 在使用`export()`时产生内容，否则为空字符串
$<LOWER_CASE:...\> | 转为小写字符
$<UPPER_CASE:...\> | 转为大写字符
$<MAKE_C_IDENTIFIER:...\> | 转为C标识符
$<TARGET_OBJECTS:objLib\> | 来自objLib构建中的对象列表
$<SHELL_PATH:...\> | 转换为shell路径样式

# CMake模块

先使用`include()`命令添加模块，再调用模块类的宏。

模块 | 描述
:---|:---
AddFileDependencies | 添加给定的文件作为源文件的依赖项
BundleUtilities | 用于处理Mac上.app的工具函数集
Check(C,CXX,Fortran)CompilerFlag | 检查编译器是否支持给定的标志
Check(C,CXX,Fortran)SourceCompiles | 检查给定的代码是否编译链接到一个可执行文件中
Check(C,CXX,Fortran)SourceRuns | 检查是否编译运行给定的代码
CheckCXXSymbolExists | 检查符号是否存在在C++中
CheckFunctionExists | 检查是否函数是否存在
CheckIncludeFileCXX | 检查是否在C++中能够include一个文件
CheckIncludeFile | 检查是否在C中能够include一个文件
CheckIncludeFiles | 检查是否在C中能够include一个或多个文件
CheckLanguage | 检查语言
CheckLibraryExists | 检查库文件是否存在
CheckPrototypeDefinition | 检测原型定义是否正确
CheckStructHasMember | 检查结构体
CheckSymbolExists | 检查符号是否存在
CheckTypeSize | 检查类型是否存在，存在则返回大小
CheckVariableExists | C变量是否存在
CMakeAddFortranSubdirectory | 添加Fortran子文件夹
CMakeBackwardCompatibilityCXX | C++向后兼容
CMakeDependentOption | 依赖选项
CMakeDetermineVSServicePack | 确定Visual Studio服务包
CMakeExpandImportedTargets | 展开导入目标
CMakeFindDependencyMacro | 查找依赖宏
CMakeFindPackageMo de | 命令行`--find-package`
CMakePackageConfigHelpers | 配置文件相关
CMakePrintHelpers | 输出属性和变量
CMakePushCheckState | 管理变量
ExternalData | 外部数据管理
ExternalProject | 外部项目
Find(\*)| 查找\*库文件,如FindZLIB
InstallRequiredSystemLibraries | 安装必要的系统库
ProcessorCount | 处理器个数
TestBigEndian | 测试大小端
TestCXXAcceptsFlag | 测试C++的标识符

# CMake工具链
通常CMake自动确定主机构建的工具链，但在交叉编译场景下，可以指定一个工具链文件来配置编译器及相应工具的路径。

## 语言

使用`project()`命令指定语言，语言会指定相应的内建变量。默认为：

```CMake
project(C_Only C)
```

`enable_language()`用来开启语言支持。

```CMake
project(MyProject NONE) # NONE不指定语言
enable_language(CXX)
```

## 交叉编译
使用`-DCMAKE_TOOLCHAIN_FILE=path/to/file`命令行参数来指定编译器值。典型的交叉编译工具链如下：

```CMake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_SYSROOT /home/devel/rasp-pi-rootfs)
set(CMAKE_STAGING_PREFIX /home/devel/stage)

set(tools /home/devel/gcc-4.7-linaro-rpi-gnueabihf)
set(CMAKE_C_COMPILER ${tools}/bin/arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER ${tools}/bin/arm-linux-gnueabihf-g++)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)       
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
```

# CMake变量
## 信息变量

变量 | 描述
:---|:---
CMAKE_ARGC | 返回命令行模式下的参数个数
CMAKE_ARGV0 | 第一个参数，类似有CMAKE_ARGV1
CMAKE_AR | 打包静态库的工具名称
CMAKE_BINARY_DIR | 构建书的顶级路径
CMAKE_CACHEFILE_DIR | CMakeCache.txt文件的目录
CMAKE_CACHE_MAJOR_VERSION | 版本号，类似还有MINOR,PATCH_VERSION
CMAKE_COMMAND | cmake命令的路径
CMAKE_CROSSCOMPILING | 返回是否是交叉编译 
CMAKE_CROSSCOMPILING_EMULATOR | 返回交叉编译可运行目标机器程序的命令
CMAKE_CTEST_COMMAND | 返回ctest命令的全路径
CMAKE_CURRENT_BINARY_DIR | 返回当前处理二进制文件的文件夹
CMAKE_CURRENT_LIST_(DIR,FILE,LINE) | 返回当前列表的目录，全路径，行号
CMAKE_CURRENT_SOURCE_DIR | 当前源代码文件夹
CMAKE_DL_LIBS | 包含`dlopen`和`dlclose`的库名
CMAKE_EXECUTABLE_SUFFIX | 可执行后缀
CMAKE_HOME_DIRECTORY | 返回主目录
CMAKE_IMPORT_LIBRARY_(PREFIX,SUFFIX) | 导入链接库的前缀,后缀
CMAKE_JOB_POOL_(COMPILE,LINK) | JOB_POOL编译链接的属性
CMAKE_LINK_LIBRARY_SUFFIX | 链接库的后缀
CMAKE_(MAJOR,MINOR,PATCH)_VERSION | 版本号
CMAKE_MAKE_PROGRAM | 本地构建的工具，有make,ninja,Xcode,vs等
CMAKE_MATCH_COUNT | 最近正则表达式匹配的数目
CMAKE_MINIMUM_REQUIRED_VERSION | CMake的版本要求
CMAKE_PROJECT_NAME |cmake项目名
CMAKE_RANLIB | UNIX上随机库的名称
CMAKE_ROOT | 运行cmake的安装目录
CMAKE_SHARED_LIBRARY_(PREFIX,SUFFIX) | 共享库前后缀 
CMAKE_SHARED_MODULE_(PREFIX,SUFFIX) | 共享模块前后缀 
CMAKE_SIZEOF_VOID_P | void指针的大小，确定是否是64位
CMAKE_SKIP_INSTALL_RULES | 是否跳过安装
CMAKE_SKIP_RPATH | 如果为true，则不添加运行时路径信息
CMAKE_SOURCE_DIR | 源代码文件夹
CMAKE_STATIC_LIBRARY_(PREFIX,SUFFIX) | 静态库前后缀
CMAKE_TOOLCHAIN_FILE | 交叉编译工具链文件
CMAKE_VERBOSE_MAKEFILE | 开启makefile的长输出
CMAKE_VERSION | CMake的版本号
CMAKE_VS_DEVENV_COMMAND | cmake vs开发环境命令`devenv.exe`
CMAKE_VS_MSBUILD_COMMAND | `MSBuild.exe`
PROJECT_BINARY_DIR | 项目构建目录
<PROJECT-NAME>_BINARY_DIR | 某个项目的二进制目录
PROJECT_NAME | 项目名
<PROJECT-NAME>_SOURCE_DIR | 指定的项目源码目录
<PROJECT-NAME>_VERSION | 项目版本
PROJECT_SOURCE_DIR | 项目源码目录

## 行为变量

变量 | 描述
:---|:---
BUILD_SHARED_LIBS | 在`add_library()`时构建共享库
CMAKE_BUILD_TYPE | 构建类型,`Debug`,`Release`,`RelWithDebInfo`,`MinSizeRel`
CMAKE_COLOR_MAKEFILE | 开启颜色输出
CMAKE_DEBUG_TARGET_PROPERTIES | 开启目标属性的跟踪输出
CMAKE_DEPENDS_IN_PROJECT_ONLY | 只考虑在工程目录下的依赖
CMAKE_DISABLE_FIND_PACKAGE_<PackageName> | 关闭对应包的`find_package()`
CMAKE_ECLIPSE_MAKE_ARGUMENTS | ECLIPSE项目的make参数
CMAKE_ERROR_DEPRECATED | 是否指出弃用函数的错误
CMAKE_EXPORT_COMPILE_COMMANDS | 开启或关闭编译命令的输出
CMAKE_FIND_LIBRARY_(PREFIXES,SUFFIXS) | 寻找库时的前后缀
CMAKE_FIND_ROOT_PATH | 列出搜索的主目录
CMAKE_FIND_ROOT_PATH_MODE_INCLUDE | INCLUDE目录
CMAKE_FIND_ROOT_PATH_MODE_LIBRARY | 库目录
CMAKE_FIND_ROOT_PATH_MODE_PACKAGE | 包目录
CMAKE_FIND_ROOT_PATH_MODE_PROGRAM | 程序目录
CMAKE_IGNORE_PATH | 忽略目录
CMAKE_INCLUDE_PATH | INCLUDE目录
CMAKE_INCLUDE_DIRECTORIES_BEFORE | 目录先后
CMAKE_INSTALL_MESSAGE | 安装信息，ALWAYS,LAZY,NEVER
CMAKE_INSTALL_PREFIX | 安装前缀
CMAKE_LIBRARY_PATH | 库路径
CMAKE_MODULE_PATH | 模块路径
CMAKE_NOT_USING_CONFIG_FLAGS | 跳过_BUILD_TYPE
CMAKE_PREFIX_PATH | 路径前缀
CMAKE_PROGRAM_PATH | 程序路径,影响`find_program()`
CMAKE_PROJECT_<PROJECT-NAME>_INCLUDE | 项目INCLUDE路径
CMAKE_SYSTEM_IGNORE_PATH | 忽略路径
CMAKE_SYSTEM_INCLUDE_PATH | 系统include路径
CMAKE_SYSTEM_LIBRARY_PATH | 系统库路径
CMAKE_SYSTEM_PREFIX_PATH | 系统前缀路径
CMAKE_SYSTEM_PROGRAM_PATH | 系统程序路径
CMAKE_USER_MAKE_RULES_OVERRIDE | 用户规则覆盖
CMAKE_WARN_DEPRECATED | 警告

## 系统描述变量

变量 | 描述
:---|:---
APPLE | OS X 系统
BORLAND | BORLAND编译器
CMAKE_CL_64 | Microsoft 64位
CMAKE_HOST_APPLE | OS X主机
CMAKE_HOST_SOLARIS | SOLARIS主机
CMAKE_(HOST_)SYSTEM_NAME | 主机名称
CMAKE_(HOST_)SYSTEM_PROCESSOR | 主机处理器
CMAKE_(HOST_)SYSTEM | 主机系统
CMAKE_(HOST_)SYSTEM_VERSION | 主机版本
CMAKE_HOST_UNIX | 是否UNIX主机
CMAKE_HOST_WIN32 | 是否Windows
CMAKE_LIBRARY_ARCHITECTURE_REGEX | 库架构正则表达式
CMAKE_LIBRARY_ARCHITECTURE | 库的架构
CYGWIN | 是否Cygwin
ENV | 访问环境变量$ENV{VAR}
MINGW | 是否mingw
MSVC(11,12,14) | vs版本
UNIX | 是否UNIX
WIN32 | 会搜否Win32
XCODE_VERSION | XCODE版本

## 控制构建的变量

变量 | 描述
:---|:---
CMAKE_ANDROID_ANT_ADDITIONAL_OPTIONS | Android ant额外选项
CMAKE_ANDROID_API | android api
CMAKE_ANDROID_API_MIN | Android最小的API
CMAKE_ANDROID_ARCH | Android默认架构，armv7-a,arm64-v8a,x64等
CMAKE_ANDROID_ASSETS_DIRECTORIES | Android 资源文件
CMAKE_ANDROID_JAR_DEPENDENCIES | Android Jar依赖
CMAKE_ANDROID_JAR_DIRECTORIES | Android Jar目录
CMAKE_ANDROID_JAVA_SOURCE_DIR | Android Java源代码目录
CMAKE_ANDROID_NATIVE_LIB_DEPENDENCIES | Android 本地库依赖
CMAKE_ANDROID_NATIVE_LIB_DIRECTORIES | Android 本地库目录
CMAKE_ANDROID_SKIP_ANT_STEP | 跳过ant
CMAKE_ANDROID_STL_TYPE | STL类型，`gnustl_static`,`gnustl_shared`等
CMAKE_BUILD_WITH_INSTALL_RPATH | 构建时使用安转运行时目录
CMAKE_<CONFIG\>_POSTFIX | 配置的后缀
CMAKE_DEBUG_POSTFIX | 调试后缀
CMAKE_ENABLE_EXPORTS | 开启导出
CMAKE_GNUtoMS | 将GNU库(.dll.a)转为MS格式(.lib)
CMAKE_INCLUDE_CURRENT_DIR | 当前include目录
CMAKE_INSTALL_NAME_DIR | 安装目录
CMAKE_INSTALL_RPATH | 安装运行时目录
CMAKE_IOS_INSTALL_COMBINED | 构建设备和模拟器目标属性
CMAKE_LIBRARY_PATH_FLAG | 库路径标志，默认为`-L`
CMAKE_LINK_DEPENDS_NO_SHARED | 依赖于无共享库的链接
CMAKE_LINK_INTERFACE_LIBRARIES | 链接接口库
CMAKE_LINK_LIBRARY_FLAG | 链接库标志，默认为`-l`
CMAKE_MODULE_LINKER_FLAGS | 模块链接标志
CMAKE_NINJA_OUTPUT_PATH_PREFIX | Ninja输出路径前缀
CMAKE_POSITION_INDEPENDENT_CODE | 位置无关代码属性声明
CMAKE_RUNTIME_OUTPUT_DIRECTORY | 运行时输出路径
CMAKE_SHARED_LINKER_FLAGS | 共享库链接标志
CMAKE_SKIP_BUILD_RPATH | 跳过构建时的运行时路径
CMAKE_SKIP_INSTALL_RPATH | 跳过安装运行时路径
CMAKE_STATIC_LINKER_FLAGS | 静态库链接标志
CMAKE_USE_RELATIVE_PATHS | 使用相对路径
CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS | windows DLL 导出所有符号
CMAKE_WIN32_EXECUTABLE | win32可执行文件
EXECUTABLE_OUTPUT_PATH | 执行输出路径
LIBRARY_OUTPUT_PATH | 库输出路径

## 语言变量

变量 | 描述
:---|:---
CMAKE_COMPILER_IS_GNU<LANG\> | 如果是GNU编译器则返回true
CMAKE_C(XX)_COMPILE_FEATURES | C/C++编译特性
CMAKE_C(XX)_EXTENSIONS | C/C++扩展
CMAKE_C(XX)_STANDARD | C/C++标准
CMAKE_C(XX)_STANDARD_REQUIRED | C/C++需要的标准
CMAKE_<LANG\>_ARCHIVE_APPEND | 打包添加的内容
CMAKE_<LANG\>_COMPILE_OBJECT | 对象编译
CMAKE_<LANG\>_COMPILER_ABI | 编译API
CMAKE_<LANG\>_COMPILER_ID | 编译ID
CMAKE_<LANG\>_COMPILER | 编译器
CMAKE_<LANG\>_COMPILER_EXTERNAL_TOOLCHAIN | 编译器外部工具链
CMAKE_<LANG\>_COMPILER_TARGET | 编译目标
CMAKE_<LANG\>_COMPILER_VERSION | 编译器版本
CMAKE_<LANG\>_CREATE_SHARED_LIBRARY | 是否创建共享库
CMAKE_<LANG\>_CREATE_SHARED_MODULE | 是否创建共享模块
CMAKE_<LANG\>_CREATE_STATIC_LIBRARY | 是否创建静态库
CMAKE_<LANG\>_FLAGS_DEBUG | Debug标志 
CMAKE_<LANG\>_FLAGS_MINSIZEREL | minsizerel 标志
CMAKE_<LANG\>_FLAGS_RELEASE | release 标志
CMAKE_<LANG\>_FLAGS_RELWITHDEBINFO |relwithdebinfo 标志 
CMAKE_<LANG\>_FLAGS | 标志
CMAKE_<LANG\>_IGNORE_EXTENSIONS | 忽略扩展
CMAKE_<LANG\>_IMPLICIT_INCLUDE_DIRECTORIES | 隐式include目录
CMAKE_<LANG\>_IMPLICIT_LINK_DIRECTORIES | 隐式链接目录
CMAKE_<LANG\>_IMPLICIT_LINK_LIBRARIES | 隐式链接库
CMAKE_<LANG\>_LIBRARY_ARCHITECTURE | 库架构
CMAKE_<LANG\>_LINKER_PREFERENCE_PROPAGATES | 库引用传递
CMAKE_<LANG\>_LINKER_PREFERENCE | 库引用
CMAKE_<LANG\>_LINK_EXECUTABLE | 链接可执行文件
CMAKE_<LANG\>_OUTPUT_EXTENSION | 输出扩展
CMAKE_<LANG\>_PLATFORM_ID | 平台ID
CMAKE_<LANG\>_SIMULATE_ID | 模拟器ID
CMAKE_<LANG\>_SIZEOF_DATA_PTR | 数据指针大小
CMAKE_<LANG\>_SOURCE_FILE_EXTENSIONS | 源文件扩展名
CMAKE_<LANG\>_STANDARD_INCLUDE_DIRECTORIES | 标准include目录
CMAKE_<LANG\>_STANDARD_LIBRARIES | 标准库
CMAKE_USER_MAKE_RULES_OVERRIDE_<LANG\> | 是否覆盖用户定义规则

# 如何找到库文件
cmake使用`find_package`命令来查找库文件。下面简单介绍如何在CMake项目中使用外部库文件，并编写自己的查找模块。

## 使用外部库
CMake自带多个模块`moudles`来辅助查找相对知名的库和包。可以在命令行中输入`cmake --help-module-list`来获得当前CMake支持的模块。或者找出模块路径并在其中查找，在Ubuntu Linux系统上，模块路径是`/usr/share/cmake/Modules/`.

现在考虑寻找`bzip2`库。存在一个`FindBZip2.cmake`的模块，使用`find_package(BZip2)`来调用模块时，CMake会自动填入多个变量，可在后续脚本中使用。变量名的列表，可以使用`cmake --help-module FindBZip2`来获取。

举例来说，考虑一个很简单的使用bzip2的程序，即编译器需要知道`bzlib.h`的位置，链接器需要找到`bzip2`库文件。

```CMake
# 指定CMake的版本要求
cmake_minimum_required(VERSION 2.8)
# 项目名
project(helloworld)
# 可执行文件配置
add_executable(helloworld hello.c)
# 查找BZip2库
find_package (BZip2)
if (BZIP2_FOUND)
  include_directories(${BZIP_INCLUDE_DIRS})
  target_link_libraries (helloworld ${BZIP2_LIBRARIES})
endif (BZIP2_FOUND)
```

可以使用`cmake`和`make VERBOSE=1`来验证编译器和链接器是否收到了正确的标志。

## 使用CMake Modules中当前没有的外部库
假定要使用`LibXML++`库，CMake并没有改库的模块，但是可以在网络上寻找到一个`FidLibXML++.cmake`文件，那么可以在`CMakeLists.txt`中编写如下代码：

```CMake
find_package(LibXML++ REQUIRED)
include_directories(${LibXML++_INCLUDE_DIRS})
set(LIBS ${LIBS} ${LibXML++_LIBRARIES})
```

然后需要将`FindLibXML++.cmake`文件放到CMake模块路径下。由于CMake并不自带该文件，所以需要手动添加到工程中。在项目根目录下创建`cmake/Modules`文件夹，并在主目录`CMakeLists.txt`文件中，添加如下代码：

```CMake
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/")
```

最后，将CMake模块文件放入到文件夹中即可。

通常上述步骤可以解决大多数问题，但是一些库需要额外的配置，需要留心查看`FindSometing.cmake`文件来继续配置。

### 带有组件的包
有些库依赖于一个或多个独立的库或组件。一个有代表性的例子就是Qt库，它可以包括QtOpenGL和QtXml等组件。要使用这些组件，需要使用下面的命令：

```CMake
find_package(Qt COMPONENTS QtOpenGL QtXml REQUIRED)
```

## package如何工作的
`find_package()`命令会在module路径下查找`Find<name>.cmake`。首先CMake检查所有在`${CMAKE_MODULE_PATH}`变量中的目录，然后在自己的模块路径下查找`<CMAKE_ROOT>/share/cmake-x.y/Modules`。

如果没有找到这样的文件，那么cmake会继续寻找`<Name>Config.cmake`或`<lower-case-name>-config.cmake`。这些文件中会硬编码安装库文件的相应变量值。

前者称为模块模式，后面称为配置模式。对于模块模式，无论包有没有被找到，以下变量都会定义：

- `<NAME>_FOUND`
- `<NAME>_INCLUDE_DIRS`或`<NAME>_INCLUDES`
- `<NAME>_LIBRARIES`或`<NAME>_LIBRARIES`或`<NAME>_LIBS`
- `<NAME>_DEFINITIONS`

所有这些都在`Find<name>.cmake`文件中定义。

对于配置模式，需要手动编写配置文件。

### 如何编写一个ProjectConfig.cmake文件
假定一个项目有如下结构:

```
FooBar/
|-- CMakeLists.txt
|-- FooBarConfig.cmake.in
|-- FooBarConfigVersion.cmake.in
|-- foo/
|   |-- CMakeLists.txt
|   |-- config.h.in
|   |-- foo.h
|   `-- foo.c
`-- bar/
    |-- CMakeLists.txt
    `-- bar.c
```

`FooBar/CMakeLists.txt`文件的简单示例如下：

```CMake
cmake_minimum_required(VERSION 2.8)
project(FooBar C)
 
set(FOOBAR_MAJOR_VERSION 0)
set(FOOBAR_MINOR_VERSION 1)
set(FOOBAR_PATCH_VERSION 0)
set(FOOBAR_VERSION ${FOOBAR_MAJOR_VERSION}.${FOOBAR_MINOR_VERSION}.${FOOBAR_PATCH_VERSION})
 
# 提供选项供用户重载安装目录
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH
  "Installation directory for header files")
if(WIN32 AND NOT CYGWIN)
  set(DEF_INSTALL_CMAKE_DIR CMake)
else()
  set(DEF_INSTALL_CMAKE_DIR lib/CMake/FooBar)
endif()
set(INSTALL_CMAKE_DIR ${DEF_INSTALL_CMAKE_DIR} CACHE PATH
  "Installation directory for CMake files")
 
# 使相对路径转变为绝对路径
foreach(p LIB BIN INCLUDE CMAKE)
  set(var INSTALL_${p}_DIR)
  if(NOT IS_ABSOLUTE "${${var}}")
    set(${var} "${CMAKE_INSTALL_PREFIX}/${${var}}")
  endif()
endforeach()
 
# 设添加nclude-directoreis
include_directories(
  "${PROJECT_SOURCE_DIR}"   # 找到foo/foo.h
  "${PROJECT_BINARY_DIR}")  # 找到foo/config.h
 
# 添加子目录
add_subdirectory(foo)
add_subdirectory(bar)
 
# ===============================
 
# 添加所有的目标到构建树的导出集合
export(TARGETS foo bar
  FILE "${PROJECT_BINARY_DIR}/FooBarTargets.cmake")
 
# 导出包
export(PACKAGE FooBar)
 
# 创建FooBarConfig.cmake和FooBarConfigVersion文件
file(RELATIVE_PATH REL_INCLUDE_DIR "${INSTALL_CMAKE_DIR}"
   "${INSTALL_INCLUDE_DIR}")

# 构建
set(CONF_INCLUDE_DIRS "${PROJECT_SOURCE_DIR}" "${PROJECT_BINARY_DIR}")
configure_file(FooBarConfig.cmake.in
  "${PROJECT_BINARY_DIR}/FooBarConfig.cmake" @ONLY)

# 安装
set(CONF_INCLUDE_DIRS "\${FOOBAR_CMAKE_DIR}/${REL_INCLUDE_DIR}")
configure_file(FooBarConfig.cmake.in
  "${PROJECT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/FooBarConfig.cmake" @ONLY)
# 构建和安装
configure_file(FooBarConfigVersion.cmake.in
  "${PROJECT_BINARY_DIR}/FooBarConfigVersion.cmake" @ONLY)
 
# 安装FooBarConfig.cmake和FooBarConfigVersion.cmake
install(FILES
  "${PROJECT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/FooBarConfig.cmake"
  "${PROJECT_BINARY_DIR}/FooBarConfigVersion.cmake"
  DESTINATION "${INSTALL_CMAKE_DIR}" COMPONENT dev)
 
# 安装导出集合到安装树
install(EXPORT FooBarTargets DESTINATION
  "${INSTALL_CMAKE_DIR}" COMPONENT dev)
```

## 关于pkg-config
`pkg-config`是一个内建的工具，基于`.pc`文件，记录库文件和头文件的位置。一般在类Unix系统上存在。CMake包括一些定义好的函数来使用`pkg-config`。这些函数在CMake的模块目录下的`FindPkgConfig.cmake`文件中，可以帮助处理`pkg-config`支持的库。

## 编写find modules
首先，要注意名称和前缀。要保证名称完全匹配。模块的基本操作需要遵循以下顺序：

- 使用`find_package`来检测一个库依赖的其他库
  - 参数`QUIETLY`和`REQUIRED`需要前置
- 可选的使用pkg-config来检测路径
- 使用`find_path`和`find_library`来分别查找头文件和库文件
  - 使用`pkg-config`得到的路径只用来提示在哪里去找
  - CMake也有很多其他硬编码的位置
  - 结果应保存到变量`<name>_INCLUDE_DIR`和`<name>_LIBRARY`中(注意是单数，而不是复数，后面没有加S)
- 设置`<name>_INCLUDE_DIRS`为`<name>_INCLUDE_DIR <dependency1>_LIBRARIES ...`
- 设置`<name>_LIBRARIES`为`<name>_LIBRARY <dependency1>_LIBRARIES ...`
  - 依赖使用复数形式，包自身使用`find_path`和`find_library`给出的单数形式
- 调用`find_package_handle_standard_ars()`宏来设置`<name>_FOUND`变量并输出一个成功或失败的消息

```CMake
# - 寻找LibXml2
# 定义的变量
#  LIBXML2_FOUND - System has LibXml2
#  LIBXML2_INCLUDE_DIRS - The LibXml2 include directories
#  LIBXML2_LIBRARIES - The libraries needed to use LibXml2
#  LIBXML2_DEFINITIONS - Compiler switches required for using LibXml2

find_package(PkgConfig)
pkg_check_modules(PC_LIBXML QUIET libxml-2.0)
set(LIBXML2_DEFINITIONS ${PC_LIBXML_CFLAGS_OTHER})

find_path(LIBXML2_INCLUDE_DIR libxml/xpath.h
          HINTS ${PC_LIBXML_INCLUDEDIR} ${PC_LIBXML_INCLUDE_DIRS}
          PATH_SUFFIXES libxml2 )

find_library(LIBXML2_LIBRARY NAMES xml2 libxml2
             HINTS ${PC_LIBXML_LIBDIR} ${PC_LIBXML_LIBRARY_DIRS} )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set LIBXML2_FOUND to TRUE
find_package_handle_standard_args(LibXml2  DEFAULT_MSG
                                  LIBXML2_LIBRARY LIBXML2_INCLUDE_DIR)

mark_as_advanced(LIBXML2_INCLUDE_DIR LIBXML2_LIBRARY )

set(LIBXML2_LIBRARIES ${LIBXML2_LIBRARY} )
set(LIBXML2_INCLUDE_DIRS ${LIBXML2_INCLUDE_DIR} )
```





[TOC]
