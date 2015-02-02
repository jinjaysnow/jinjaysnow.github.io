author: Jin Jay
title: iOS隐藏状态栏
Date: 2015-01
description: 使用UIImagePickerController对iOS照相机和相册的相关操作。
keywords: iOS照相机
        UIImagePickerController

**UIImagePickerController**
有两种source类型：
1. `ImagePickerControllerSourceTypeCamera`提供通过照相机采集的照片或视频的界面
2. `ImagePickerControllerSourceTypePhotoLibrary`提供从相册选取照片或视屏的界面

按照以下步骤使用图像选取控制器：
1. 通过调用类方法`isSourceTypeAvailable:`验证设备能够允许使用摄像机或相册，参数即上述两种类型之一
2. 通过调用类方法`availableMediaTypesForSourceType:`检查哪一种媒体类型可以供你使用，这一步是让你配置照相机是用作摄像还是用作拍照
3. 通过设置`mediaTypes`属性告诉图像选取控制器你需要的媒体属性，图片或视频或者二者
4. 呈现用户界面，在iPhone和iPod touch上可以使用`presentViewController:animated:completion:`方法来模态（全屏）显示你配置好的图像选取视图控制器。在iPad上需要根据资源类型选取正确的方式，如果你的参数是`UIImagePickerControllerSourceTypeCamera`，你可以使用模态或popover方式，如果是其它的类型，你必须使用popover(弹出对话框)方式
5. 在用户点击按钮后，如果是新拍摄的照片，你的delegate(代理)会自动保存到相册中；对于从相册中选取的照片，delegate可以获取相片数据。

**使用UIImagePickerController必须实现UIImagePickerControllerDelegate协议。**


----

如果想要获取对照相机更多的细节控制，可以使用AVFoundation提供的媒体IFA耐高温和摄像机控制方法。  想要获取对相册的更进一步的访问控制，可以使用Assets Libraray框架提供的相关操作。

[TOC]