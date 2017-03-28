author: Jin Jay
title: Project Tango
Date: 2017-03
description: 谷歌Project Tango使用文档的中文翻译。
Image:  images/APIDiagram.png
keywords: Project Tango
          增强现实
          Augmented Reality



# Tango开发概览
Tango是利用计算机视觉技术来使得设备能够理解其在真实环境中的姿态的技术平台。Tango设备一般配备有一个广角相机(鱼眼相机)、一个深度相机，精确的传感器时间标记和一个能够使应用开发者使用运动追踪、区域学习和深度感知的软件技术堆栈。

## 背景知识
### 坐标系
Tango使用两个不同的遵循右手法则的坐标系，分别是**右手局部坐标系**和**右手Android坐标系**。

**右手局部坐标系:**X轴正方向为水平向右，Z轴竖直向上，Y轴为深度方向垂直向前远离用户。
![右手局部坐标系](../../images/right-hand-local-level.png)

**右手Android坐标系:**X轴正方向为水平向右，Y轴竖直向上，Z轴为垂直向后指向用户。
![右手Android坐标系](../../images/right-hand-android.png)

使用运动追踪时的坐标系对应关系如下：

基础帧 | 坐标系
:---|:----
COORDINATE_FRAME_START_OF_SERVICE | 右手局部坐标系
COORDINATE_FRAME_AREA_DESCRIPTION | 右手局部坐标系
COORDINATE_FRAME_DEVICE | 右手Android坐标系

> OpenGL 坐标系

OpenGL世界坐标和相机坐标使用与右手Android类似的坐标系。
![OPENGL坐标系](../../images/opengl-frames.png)

> Unity 坐标系

Unity世界帧和相机帧使用左手坐标系：X轴水平向右，Y轴竖直向上，Z轴垂直向前远离用户。
![Unity坐标系](../../images/unity-frames.png)


### 坐标帧转换
OpenGL和Unity中，世界帧定义了场景的原点，相机帧表示了相机的视点。由Tango API提供的位姿数据必须转换到合适的坐标系下。这里介绍一下转换的数学基础。

使用下面的符号表示来代表可以被用来将一个向量在目标坐标帧和基础组欧标帧间进行转换的矩阵。
$$\_{ Target }^{ Base }{ T }$$

举例俩说，使用设备的位姿`DEVICE`(D)作为目标坐标帧和`START_OF_SERVICE`(SS)作为基础坐标帧，表示为:
$$\_{ SS }^{ D }{ T }$$

> 将Tango位姿数据转换到OpenGL坐标系下

使用两个变换来将Tango位姿数据转换到OpenGL相机坐标帧下。第一个变换将Tango的`START_OF_SERVICE`(SS)坐标帧转换为`OpenGL World`(OW)坐标帧。
$$\_{ OW }^{ SS }{ T } = \begin{bmatrix} 1&0&0&0 \\\\ 0&0&-1&0 \\\\ 0&1&0&0 \\\\ 0&0&0&1 \end{bmatrix}$$

第二个变换将`OpenGL Camera`(OC)坐标帧转换为`Tango Device`(D)下，由于两个帧使用相同的坐标系，所以转换矩阵为单位阵。
$$\_{ OC }^{ D }{ T } = \begin{bmatrix} 1&0&0&0 \\\\ 0&1&0&0 \\\\ 0&0&1&0 \\\\ 0&0&0&1 \end{bmatrix}$$

通过按序相乘变换矩阵，可以获得从API到OpenGL相机帧的变换矩阵：
$$\_{ OC }^{ OW }{ T } = \_{ SS }^{ OW }{ T } * \_{ D }^{ SS }{ T } * \_{ OC }^{ D }{ T }$$

> 将Tango位姿数据转换到Unity坐标系下

与转换为到OpenGL下类似，首先在`START_OF_SERVICE`(SS)和`Unity World`（UW)下转换。
$$\_{ SS }^{ UW }{ T } = \begin{bmatrix} 1&0&0&0 \\\\ 0&0&1&0 \\\\ 0&1&0&0 \\\\ 0&0&0&1 \end{bmatrix}$$

然后是`Unity Camera`(UC)与`Tango Device`(D)转换。
$$\_{ UC }^{ D }{ T } = \begin{bmatrix} 1&0&0&0 \\\\ 0&1&0&0 \\\\ 0&0&-1&0 \\\\ 0&0&0&1 \end{bmatrix}$$

连乘得到转换矩阵。
$$\_{ UC }^{ UW }{ T } = \_{ SS }^{ UW }{ T } * \_{ D }^{ SS }{ T } * \_{ UC }^{ D }{ T }$$

### 引用帧
为了执行运动追踪，设备报告自己的位姿(位置和方向)相对于给定的引用帧，该帧被认为在三维空间中固定不变。举例来说设备报告“相对于我开始运动追踪的地方，我现在在前方三尺、高度一尺的位置，并向右旋转了30度”。这样设备通过使用有意义的方向信息告知了它的位置：从初始位置开始前方三尺，高度一尺；还有当前它的方向，相对于初始位置向右旋转了30度。为了使用运动追踪，需要设定以下两个帧：

1. 基础帧，参考帧，在三维空间中固定不变的帧，例`COORDINATE_FRAME_START_OF_SERVICE`。
2. 目标帧，想要测量的帧，运动追踪中通常为`COORDINATE_FRAME_DEVICE`。

#### 运动追踪的坐标帧
Tango API提供的用于运动追踪的坐标帧如下：

|目标帧|基础帧|
|:----|:----|
|COORDINATE_FRAME_DEVICE | COORDINATE_FRAME_START_OF_SERVICE|
|COORDINATE_FRAME_DEVICE | COORDINATE_FRAME_AREA_DESCRIPTION|
|COORDINATE_FRAME_START_OF_SERVICE| COORDINATE_FRAME_AREA_DESCRIPTION|

#### 组件对齐的坐标帧

|目标帧|基础帧|
|:----|:----|
|COORDINATE_FRAME_DEVICE         | COORDINATE_FRAME_IMU |
|COORDINATE_FRAME_CAMERA_COLOR   | COORDINATE_FRAME_IMU |
|COORDINATE_FRAME_CAMERA_DEPTH   | COORDINATE_FRAME_IMU |
|COORDINATE_FRAME_CAMERA_FISHEYE | COORDINATE_FRAME_IMU |

一些设备需要对齐多个数据源，比如从彩色相机和深度相机获取的数据。可以将`COORDINATE_FRAME_IMU`作为基础帧，与其他组件目标帧组合。

结合数据中的运动追踪坐标帧和时间戳，计算出的偏移量可以在时间和空间上对多个传感器输入有更深层的了解。这在对齐和组合多个数据源时很有必要。

由于设备设计为刚体模型，这些偏移量被认为不可更改，且在API中也不会发生变化。然而，设备的组件在空间总的位置是变化的。当前Tango API并不会更新外部参数。这些值是在工厂模式下一次标定完成或从工厂的描述设计文件中获取。需要获得更加精确的数据，应用开发者需要实现自己的标定程序来让终端用户执行。

`COORDINATE_FRAME_IMU`基础帧给设备的所有其他组件提供了一个共同的引用点。这个基础帧的原点并不必与其他任一个组件相同，而且可以在设备间变化。与其他的Android传感器类似，设备的坐标帧轴与设备的自然方向对齐。这个工厂定义的方向可能与应用想要的方向并不一致。为了最大化兼容性，不要假定Tango设备有一个自然的`landscape`或`portrait`方向。因而，使用Android的`getRotation()`方法来确定屏幕的旋转，并使用Android的`remapCoordinateSystem()`方法来将传感器坐标映射到屏幕坐标系。

### 内参/外参
对设备进行标定时，标定程序执行一系列的测量来了解设备的相机状况。这个测量值称为相机内部参数。这个信息是必要的，举个例子，开发增强现实应用时，需要将虚拟内容渲染在真是的视频帧上，需要保证设备相机的视角(field of view, **FOV**)与虚拟相机的FOV相同。另一个重要的地方是要确保虚拟物体在FOV下指定的位置处。Tango设备通过使用惯性传感器IMU来确定设备的位姿。而相机与IMU的位置并不一致，所以Tango设备的位姿测量值与真实相机的位置会有一个小的偏差。这个偏差，尽管很小，但可能会使得虚拟物体的位置出现错误。故而必须选定一个合适的坐标帧对。组件间的距离被称为外部参数。

> FOV

视角是指设备从左到右(水平FOV)和从上到下(竖直FOV)能看到的范围，使用度数来表示。

> 焦距

焦距是一个内部参数，可以用来确定FOV的大小，在大多数传统相机上，可以通过调整相机来放大和缩小图像。而Tango设备上，焦距是固定的，需要注意的是：

1. 在通过Tango API获取内部参数时，获得的是两个焦距值x和y。
2. 必须在方程中使用这些值来确定渲染时的FOV。

#### 使用Tango API获取内部参数

```C++
TangoCameraIntrinsics ccIntrinsics;
TangoService_getCameraIntrinsics(TANGO_CAMERA_COLOR, &ccIntrinsics);
```

> 计算相机的FOV

从Tango API获取的参数如下：

|参数|描述|
|:----|:---|
|width|图像的像素宽度|
|height|图像的像素高度|
|fx|x轴的焦距，像素为单位|
|fy|y轴的焦距，像素为单位|

在大多数系统中，$fx = fy$。

举例来说，获取的的数据如下：

```C
ccIntrinsics.height=720;
ccIntrinsics.fy=1042.0;
```

因此，水平FOV为：

```C
Vertical FOV = 2*atan(0.5*720.0/1042.0) = 2*19.0549 deg = 38.1098 deg
```

水平和竖直FOV的计算方程为:
$$
Horizontal \quad FOV = 2 * atan(0.5 * width / fx) - 2 * \arctan(\frac{width/2}{fx}) \\\\
Vertical \quad FOV = 2 * atan(0.5 * height / fx) - 2 * \arctan(\frac{height/2}{fx}) 
$$

如果渲染引擎只支持一个FOV值，则需要查看引擎文档来确定使用哪一个FOV。如果需要使用对角FOV，方程如下：
$$Diagonal \quad FOV = 2*atan(sqrt((width/2fx)^2 + (height/2fy)^2)) = 2 * \arctan(\frac{height/2}{fy})$$

> Tango相机畸变模型

相机的镜头存在着缺陷，会有一些畸变的存在。对大多数场景来说，这个畸变可以忽略不计，不过，在一个Tango设备进行标定时，测量并存储了这些畸变信息，可以使用`TangoCameraIntrinsics`结构来获取。

Tango使用两个镜头畸变模型：
1.如果使用运动追踪相机(鱼眼相机)，那么`FOV`畸变模型被使用，从结构体中获得标定类型为`TANGO_CALIBRATION_EQUIDISTANT`。
2. 如果使用彩色相机，那么多项式畸变模型被使用，从结构体重获得的标定类型为`TANGO_CALIBRATION_POLYNOMIAL_3_PARAMETERS`。

#### 使用Tango API获取外部参数
对于增强现实应用，需要计算IMU和相机之间的位置，这个测量值成为外部参数。因为设备上的组件位置基本不变，所以只需要计算一次即可。

```C++
//Color Camera Frame with respect to IMU Frame
TangoPoseData cToIMUPose;
TangoCoordinateFramePair cToIMUPair;
cToIMUPair.base = TANGO_COORDINATE_FRAME_IMU;
cToIMUPair.target = TANGO_COORDINATE_FRAME_CAMERA_COLOR;
TangoService_getPoseAtTime(0.0, cToIMUPair, &cToIMUPose);
cToIMU_position = ToVector(cToIMUPose.translation[0],
                           cToIMUPose.translation[1],
                           cToIMUPose.translation[2]);
cToIMU_rotation = ToQuaternion(cToIMUPose.orientation[3],
                               cToIMUPose.orientation[0],
                               cToIMUPose.orientation[1],
                               cToIMUPose.orientation[2]);
```

通过选择合适的坐标帧对来计算两个设备组件的外部参数。


## 运动追踪
运动追踪指Tango设备能够在三维空间追踪自己的运动和方向。设备上下前后左右移动和旋转都可以知晓。与鼠标的功能类似，但是不限于二维平面，在整个三维空间中都可以使用。

### 使用
设备在三维空间运动时，会以最高100次每秒的速度来计算位置和方向。每次计算的结果称为设备的位姿。Tango API 提供了两种方式来获取位姿数据：回调函数来获取实时最近的位姿更新和获取一个指定时间的位姿测量值的函数。返回的数据主要由两部分组成：平移向量和旋转四元数。位姿配置为特定的**引用帧对**，必须指定一个目标帧及它相对应的基础帧，给出的数据是目标帧相对于基础帧的相对位姿。

















[TOC]