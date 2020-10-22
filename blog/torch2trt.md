Title: Torch2TRT使用
description:  将pytorch网络转为TensorRT网络的torch2trt加速库的简介，使用及更改pytorch代码适配示例，docker中的运行示例。
Author: Jin Jay
Date:    2020-10
keywords: Torch2TRT
          TensorRT
          Pytorch


# Torch2TRT简介

[torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt)可以将Pytorch网络转为TensorRT网络来进行加速。该库的开发人员主要针对NVIDIA嵌入式设备进行开发，支持[Jetson AGX Xavier](https://developer.nvidia.com/embedded/jetson-agx-xavier-developer-kit), Jetson Nano, Jetson TX1, Jetson TX2, Jetson Xavier NX等。目前(2020年)，算力最强为Jetson AGX Xavier，拥有32TOPS的计算力，32G内存和32G板载存储，可以额外添加1T M.2 SSD 升级存储，国内目前单价大概8000元。

## 安装
Jetson设备上根据Github上的官方教程可以直接安装。参考文末`Jetson_zoo`安装pytorch并安装对应版本的`torchvision`(使用`git checkout -b v0.5`切换到对应的`torchvision`分支，然后手动编译安装)，最后编译安装`torch2trt`，建议添加`--user`选项将库安装到用户目录。

```bash
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
python3 setup.py install --plugins --user
```

台式机及服务器端，由于需要配合TensorRT使用，建议在NVIDIA的官方网站下载对应的Docker镜像，[https://ngc.nvidia.com/catalog/containers/nvidia:tensorrt](https://ngc.nvidia.com/catalog/containers/nvidia:tensorrt)。Docker虚拟容器需要主机具有相关的驱动，建议保持最新的驱动即可。

```bash
docker pull nvcr.io/nvidia/tensorrt:20.09-py3 # 下载镜像
docker run --gpus all --name tensorrt -it nvcr.io/nvidia/tensorrt:20.09-py3 /bin/bash # 运行镜像
docker start tensorrt # 在镜像关闭退出后启动镜像
docker exec -it tensorrt /bin/bash # 启动镜像后再次进入镜像，进行交互式界面
apt update && apt install vim # 为了便于在镜像中编辑，可安装vim等库
```

安装TensorRT镜像后，需要安装Pytorch及下载torch2trt库。

```bash
pip3 install torch torchvision # 下载并安装pytorch
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
```

Torch2TRT主要面向Jetson设备，要在台式机和服务器上运行，需要做一些小的改动，改动`setup.py`中下述代码

```python
def trt_inc_dir():
    return "/usr/include/aarch64-linux-gnu"

def trt_lib_dir():
    return "/usr/lib/aarch64-linux-gnu"
```

为 

```python
def trt_inc_dir():
    return "/usr/include/x86_64-linux-gnu"

def trt_lib_dir():
    return "/usr/lib/x86_64-linux-gnu"
```

即替换TensorRT的相关路径为平台相关路径。同样地，更改`build.py`中的下述代码:

```python
def build(cuda_dir="/usr/local/cuda",
          torch_dir=imp.find_module('torch')[1],
          trt_inc_dir="/usr/include/aarch64-linux-gnu",
          trt_lib_dir="/usr/lib/aarch64-linux-gnu"):
```

为

```python
def build(cuda_dir="/usr/local/cuda",
          torch_dir=imp.find_module('torch')[1],
          trt_inc_dir="/usr/include/x86_64-linux-gnu",
          trt_lib_dir="/usr/lib/x86_64-linux-gnu"):
```

然后，执行编译安装操作:

```bash
python3 setup.py install --plugins --user
```

## 改写Pytorch代码适配torch2trt

具体的示例是基于[MWCNN](https://github.com/lpj0/MWCNN)网络，改写其中的`DWT`和`IWT`模块。

### DWT
离散小波变化`DWT`原始代码为:

```python
class DWT(torch.nn.Module):
    def __init__(self):
        super(DWT, self).__init__()
        self.requires_grad = False

    def forward(self, x):
        return dwt_init(x)


def dwt_init(x):
    x01 = x[:, :, 0::2, :] / 2
    x02 = x[:, :, 1::2, :] / 2
    x1 = x01[:, :, :, 0::2]
    x2 = x02[:, :, :, 0::2]
    x3 = x01[:, :, :, 1::2]
    x4 = x02[:, :, :, 1::2]
    x_LL = x1 + x2 + x3 + x4
    x_HL = -x1 - x2 + x3 + x4
    x_LH = -x1 + x2 - x3 + x4
    x_HH = x1 - x2 - x3 + x4

    return torch.cat((x_LL, x_HL, x_LH, x_HH), 1)
```

`torch2trt`库不能将非`torch.nn.Module`子类的`dwt_init`函数翻译为TensorRT网络，故而会出现出错。解决方法较简单，将`dwt_init`函数整理放入`DWT`类中即可。修改后代码如下:

```python
class DWT(torch.nn.Module):
    def __init__(self):
        super(DWT, self).__init__()
        self.requires_grad = False

    def forward(self, x):
        x01 = x[:, :, 0::2, :] / 2
        x02 = x[:, :, 1::2, :] / 2
        x1 = x01[:, :, :, 0::2]
        x2 = x02[:, :, :, 0::2]
        x3 = x01[:, :, :, 1::2]
        x4 = x02[:, :, :, 1::2]
        x_LL = x1 + x2 + x3 + x4
        x_HL = -x1 - x2 + x3 + x4
        x_LH = -x1 + x2 - x3 + x4
        x_HH = x1 - x2 - x3 + x4

        return torch.cat((x_LL, x_HL, x_LH, x_HH), 1)
```

### IWT

小波逆变换`IWT`的原始代码如下:

```python
class IWT(nn.Module):
    def __init__(self):
        super(IWT, self).__init__()
        self.requires_grad = False

    def forward(self, x):
        return iwt_init(x)

def iwt_init(x):
    r = 2
    in_batch, in_channel, in_height, in_width = x.size()
    out_batch, out_channel, out_height, out_width = in_batch, int(
        in_channel / (r ** 2)), r * in_height, r * in_width
    x1 = x[:, 0:out_channel, :, :] / 2
    x2 = x[:, out_channel:out_channel * 2, :, :] / 2
    x3 = x[:, out_channel * 2:out_channel * 3, :, :] / 2
    x4 = x[:, out_channel * 3:out_channel * 4, :, :] / 2


    h = torch.zeros([out_batch, out_channel, out_height, out_width]).float().cuda()

    h[:, :, 0::2, 0::2] = x1 - x2 - x3 + x4
    h[:, :, 1::2, 0::2] = x1 - x2 + x3 - x4
    h[:, :, 0::2, 1::2] = x1 + x2 - x3 - x4
    h[:, :, 1::2, 1::2] = x1 + x2 + x3 + x4

    return h
```

`IWT`与`DWT`有类似的问题存在，但是更为难办的问题是`torch.zeros`这种运行时新建Tensor的操作符不被TensorRT支持，导致无法进行转换，且TensorRT提供的仅有`add_constant()`这种不允许动态改变值的网络层，无法实现`h[:, :, 0::2, 0::2] = x1 - x2 - x3 + x4`这种赋值操作。查看所有torch2trt支持的操作，`ConvTranspose2D`组件可以上采样生成更大尺寸的图像，在相关区域补0，可以解决我们的问题。如下，是修正后的代码:

```python

class Padding1(torch.nn.Module):
    def __init__(self, input_channel):
        super(Padding1, self).__init__()
        self.requires_grad = False
        self.conv = torch.nn.ConvTranspose2d(input_channel, input_channel, 1,stride=2, padding=0, groups=input_channel, bias=False)
        torch.nn.init.constant_(self.conv.weight, 1)

    def forward(self, x):
        x1 = self.conv(x)
        y = torch.nn.functional.pad(x1, (0, 1, 0, 1))
        return y

class Padding2(torch.nn.Module):
    def __init__(self, input_channel):
        super(Padding2, self).__init__()
        self.requires_grad = False
        self.conv = torch.nn.ConvTranspose2d(input_channel, input_channel, 1,stride=2, padding=0, groups=input_channel, bias=False)
        torch.nn.init.constant_(self.conv.weight, 1)

    def forward(self, x):
        x1 = self.conv(x)
        y = torch.nn.functional.pad(x1, (0, 1, 1, 0))
        return y

class Padding3(torch.nn.Module):
    def __init__(self, input_channel):
        super(Padding3, self).__init__()
        self.requires_grad = False
        self.conv = torch.nn.ConvTranspose2d(input_channel, input_channel, 1,stride=2, padding=0, groups=input_channel, bias=False)
        torch.nn.init.constant_(self.conv.weight, 1)

    def forward(self, x):
        x1 = self.conv(x)
        y = torch.nn.functional.pad(x1, (1, 0, 0, 1))
        return y

class Padding4(torch.nn.Module):
    def __init__(self, input_channel):
        super(Padding4, self).__init__()
        self.requires_grad = False
        self.conv = torch.nn.ConvTranspose2d(input_channel, input_channel, 1,stride=2, padding=0, groups=input_channel, bias=False)
        torch.nn.init.constant_(self.conv.weight, 1)

    def forward(self, x):
        x1 = self.conv(x)
        y = torch.nn.functional.pad(x1, (1, 0, 1, 0))
        return y

class IWT(torch.nn.Module):
    def __init__(self, input_channel=1):
        super(IWT, self).__init__()
        self.requires_grad = False
        self.padding1 = Padding1(int(input_channel / 4))
        self.padding2 = Padding2(int(input_channel / 4))
        self.padding3 = Padding3(int(input_channel / 4))
        self.padding4 = Padding4(int(input_channel / 4))

    def forward(self, x):
        r = 2
        in_batch, in_channel, in_height, in_width = x.size()

        out_batch, out_channel, out_height, out_width = in_batch, int(
            in_channel / (r ** 2)), r * in_height, r * in_width
        x1 = x[:, 0:out_channel, :, :] / 2
        x2 = x[:, out_channel:out_channel * 2, :, :] / 2
        x3 = x[:, out_channel * 2:out_channel * 3, :, :] / 2
        x4 = x[:, out_channel * 3:out_channel * 4, :, :] / 2

        y1 = x1 - x2 - x3 + x4
        y2 = x1 - x2 + x3 - x4
        y3 = x1 + x2 - x3 - x4
        y4 = x1 + x2 + x3 + x4

        t_h1 = self.padding1(y1)
        t_h2 = self.padding2(y2)
        t_h3 = self.padding3(y3)
        t_h4 = self.padding4(y4)

        r= t_h1 + t_h2 + t_h3 + t_h4
        return  r
```

通过组合`ConvTranspose2D`和`pad`可以实现`IWT`相关的操作。重新训练网络后，可以实现`TensoRT`加速。


## 在Jetson设备的Docker中运行tensorrt

主机上安装tensorrt的docker支持

```bash
sudo apt install nvidia-container-csv-tensorrt
```

修改`nvidia-docker`配置文件`/etc/nvidia-container-runtime/host-files-for-container.d/tensorrt.csv`:

```txt
lib, /usr/lib/aarch64-linux-gnu/libnvinfer.so.6.0.1
lib, /usr/lib/aarch64-linux-gnu/libnvinfer_plugin.so.6.0.1
lib, /usr/lib/aarch64-linux-gnu/libnvonnxparser.so.6.0.1
lib, /usr/lib/aarch64-linux-gnu/libnvonnxparser_runtime.so.6.0.1
lib, /usr/lib/aarch64-linux-gnu/libnvparsers.so.6.0.1
sym, /usr/lib/aarch64-linux-gnu/libnvcaffe_parser.so.6
sym, /usr/lib/aarch64-linux-gnu/libnvcaffe_parser.so.6.0.1
sym, /usr/lib/aarch64-linux-gnu/libnvinfer.so.6
sym, /usr/lib/aarch64-linux-gnu/libnvinfer.so
sym, /usr/lib/aarch64-linux-gnu/libnvinfer_plugin.so
sym, /usr/lib/aarch64-linux-gnu/libnvinfer_plugin.so.6
sym, /usr/lib/aarch64-linux-gnu/libnvonnxparser.so.6
sym, /usr/lib/aarch64-linux-gnu/libnvonnxparser_runtime.so.6
sym, /usr/lib/aarch64-linux-gnu/libnvparsers.so.6
dir, /usr/src/tensorrt
dir, /usr/lib/python3.6/dist-packages/tensorrt
dir, /usr/include/aarch64-linux-gnu
```

虚拟机中安装相关库:

```bash
apt install python3-opencv python3-matplotlib
apt-get install -y git python3-pip cmake protobuf-compiler libprotoc-dev libopenblas-dev gfortran libjpeg8-dev libxslt1-dev libfreetype6-dev
pip3 install -U numpy
pip3 install torch-xxx.whl --user # 下载pytorch包安装

git clone -b v0.5.0 https://github.com/pytorch/vision torchvision
python3 setup.py install —user

apt-get install libprotobuf* protobuf-compiler ninja-build -y
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
python3 setup.py install --plugins --user

```


## TODO

1. 可通过编写相关插件实现`IWT`功能，需要进一步研究`torch2trt`源码。

## 相关资源链接

1. Jetson_Zoo 汇总了Jetson设备的相关资源链接。[https://elinux.org/Jetson_Zoo](https://elinux.org/Jetson_Zoo)



[TOC]































