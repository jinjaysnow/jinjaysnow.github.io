Title: 状态估计
description:  示例介绍状态测量估计。
Author: Jin Jay
Date:    2017-07
keywords: Orientation Estimation
          Extended Kalman Filtering
          Example
          IMU
          MagneticField
          状态测量
          惯性测量
          磁场
          扩展卡尔曼滤波

# 状态估计&mdash;使用智能手机的加速计、陀螺仪和磁力计估计手机的姿态

设计和实现基于惯性传感器和磁力计的移动设备姿态估计系统。

主要参考：
1. [Using Inertial Sensors for Position and Orientation Estimation](http://cn.arxiv.org/pdf/1704.06053.pdf)
2. [Orientation Estimation using Smartphone Sensors](http://www.control.isy.liu.se/en/student/tsrt14/file/orientation.pdf)
3. [Quaternion kinematics for the error-state Kalman filter](http://www.iri.upc.edu/people/jsola/JoanSola/objectes/notes/kinematics.pdf)

## 相关原理

### 使用四元数表示旋转
坐标帧定义：

- 世界坐标帧，$W$，相对于地球固定，x轴指向东边，y轴指向北边，z轴竖直向上。
- 传感器坐标帧，$S$，手机上的传感器坐标帧，屏幕向上时，x轴指向右侧，y轴指向前方，z轴向上。

世界坐标帧与传感器坐标帧间存在一个线性变换：

$$p^W = R^{W/S}p^S + t^{W/S}$$
其中$p^S$表示在传感器帧中的一点，$p^W$表示同一点在世界坐标帧下的表示。两个坐标帧的相对旋转为$R^{W/S}$，平移为$t^{W/S}$。

旋转可以由多种方式进行描述。一种就是旋转矩阵。使用9个值表示3个自由度。另一种是使用欧拉角，绕三个预先定义的轴进行连续的旋转。不过欧拉角不唯一。第三种表示方式为四元数。四元数可以理解为旋转轴的一个角度表示：
$$q = \begin{pmatrix}  q\_0 \\\\ q\_1 \\\\ q\_2 \\\\ q\_3 \end{pmatrix} = \begin{pmatrix}  \cos(\frac{\alpha}{2})  \\\\ \sin(\frac{\alpha}{2})\begin{pmatrix}  \hat{v}\_x \\\\ \hat{v}\_y \\\\ \hat{v}\_z  \end{pmatrix}   \end{pmatrix} = \begin{pmatrix}  \cos(\frac \alpha 2) \\\\ \sin(\frac \alpha 2)\hat v   \end{pmatrix}$$
其中$\alpha$为绕单位旋转向量$\hat v$的轴的一个正的旋转角度。

### 概率模型
状态估计系统抽象：目标是通过测量值$y\_{1:N}$和概率模型来推算出系统的状态$x\_{1:N}$和参数$\theta$。可以使用如下的条件概率分布来表示：
$$p(x\_{1:N}, \theta|y\_{1:N}) \label{a1} \tag{1}$$
状态估计问题中，主要关注于获取点估计，记为$\hat{x}\_{1:N}$和$\hat \theta$.通常使用协方差来表示对估计值的置信度。
使用所有的测量值$y\_{1:N}$来得到状态$x\_{1:N}$和参数$\theta$的后验估计，这个过程称为平滑。平滑的缺点就是需要等待所有的测量值都被采集后才能进行计算。故而，在大多数应用中，采用滤波来进行估计。滤波的方法中，在时刻t使用当前所有的测量值来估算$x\_t$。滤波问题可以表示为如下的条件概率分布：
$$p(x\_t|y\_{1:t})\label{a2} \tag{2}$$
综上，平滑是将所有的状态$x\_{1:N}$同时估算的过程；滤波是在每一个t时刻，状态$x\_t$被估算。假定模型具有Markov属性，即当前时刻t的所有信息包含在状态$x\_t$中。使用贝叶斯规则，可以将两个条件概率分布分解为:
$$
\begin{align\*}
p(x\_{1:N}, \theta|y\_{1:N}) & \propto p(\theta)p(x\_1|\theta)\prod\_{t=2}^N p(x\_t|x\_{t-1}, \theta)\prod \_{t=1}^Np(y\_t|x\_t, \theta) \label{a3} \tag{3} \\\\ 
p(x\_t|y\_{1:t}) & \propto p(y\_t|x\_t)p(x\_{t}|y\_{1:t-1}) \label{a4} \tag{4}
\end{align\*}
$$

在公式$\ref{a3}$中，$p(\theta)$和$p(x\_1|\theta)$分别编码了关于$\theta$的先验信息和给定$\theta$状态$x\_1$的信息。$p(x\_t|x\_{t-1}, \theta)$和$p(x\_{t+1}|x\_t)$由系统的运动模型建模。分布$p(y\_t|x\_t, \theta)$和$p(y\_t|x\_t)$建模了给定关于状态和参数的测量所得到的信息。
一般，系统的运动模型可以使用非线性函数$f\_t(\cdot)$进行建模，如下：
$$x\_{t+1}=f\_t(x\_t,\omega\_t) \label{a5} \tag{5}$$系统运动模型的不确定性通常有$\omega\_t$进行表示，指代过程噪声。模型$\ref {a5}$提供了关于分布$p(x\_{t+1}|x\_t)$的信息。如果$\omega\_t$是高斯分布$N(0,Q)$的噪声,那么：
$$p(x\_{t+1}|x\_t)\sim N(x\_{x\_{t+1}}; f\_t(x\_t), Q) \label{a6} \tag{6}$$表示随机变量$x\_{t+1}$是均值为$f\_t(x\_t)$，方差为$Q$的正态分布。
由测量给定的关于$x\_t$的信息能被建模为：
$$y\_t=h\_t(x\_t,e\_t) \label{a7} \tag{7}$$其中$h\_t(\cdot)$是一个非线性函数，$e\_t$是测量噪声。

### 测量模型
#### 陀螺仪测量模型
陀螺仪测量角速度，受到随时间缓慢变化的零偏$b\_{w,t}$和噪声$e\_{w,t}$的影响，可将陀螺仪测量值建模为：
$$y\_{w,t} ^S = w\_{t} ^S + b\_{w,t} ^S + e\_{w,t} ^S$$其中，上标$S$表示处于传感器坐标系。通常噪声属于高斯噪声。
将角速度表示到世界坐标系下，有:
$$y\_{w,t} ^W = R\_t^{W/S}(w\_{t} ^S + b\_{w,t} ^S + e\_{w,t}^S) \label{a8} \tag{8}$$

#### 加速计测量模型
加速计测量线性加速度，受零偏$b\_{a,t}$和噪声$e\_{a,t}$的影响：
$$y\_{a,t}^S = a\_t^S + b\_{a,t}^S + e\_{a,t}^S$$加速计的测量值中包含重力：
$$a^W = R^{W/S}(a^S-g^S)$$
由于加速度测量值主要来自重力向量，姿态估计中常常假定线性加速度大约为0：
$$
y\_{a,t}^S = g^S + b\_{a,t}^S + e\_{a,t}^S \label{a9} \tag{9}$$

#### 磁力计测量模型
磁力计测量局部磁场，包括地磁和周围环境中的磁性材料的磁场。地磁$m^W$的水平分量指向地球的磁场北极，水平和竖直分量的比值取决于在地球上的位置，使用磁倾角$\delta$表示。磁场强度可以建模为：
$$m^W = ( 0 \quad \cos\delta \quad \sin\delta)$$假定$\left\\| m^W \right\\|\_2 = 1$。假定磁力计只测量局部的地磁场，有：
$$y\_{m, t}^S = R\_t^{S/W}m^W + e\_{m,t}^S$$

### 运动模型
使用四元数表示方向，方向$q$和角速度$w$的关系如下：
$$\frac{dq}{dt} = \frac 12 S(w)q = \frac 1 2 \overline S(q)w$$
其中$S(w)$是角速度的四维斜对称矩阵，$\overline S(q)$表示将四元数转化为$4\times 3$矩阵。
$$S(\omega)=\begin{pmatrix}
0 & -w\_x & -w\_y&-w\_z \\\\
w\_x & 0 & w\_z & -w\_y \\\\
w\_y & -w\_z & 0 & w\_x \\\\
w\_z & w\_y & -w\_x & 0
\end{pmatrix}\quad 
\overline S(q) = \begin{pmatrix}
-q\_1 & -q\_2 & -q\_3 \\\\
q\_0 & -q\_3 & q\_2 \\\\
q\_3 & q\_0 & -q\_1 \\\\
-q\_2 & q\_1 & q\_0
\end{pmatrix}
$$

### 姿态估计状态空间模型

根据四元数的特征，不考虑惯性传感器零偏，假设没有线性加速度，磁力计只测量本地的地磁强度，有如下的模型
$$
\begin{align\*}
q\_{t+1} &= e^{\frac {\Delta t}2S(y\_{w,t}+e\_{w,t})}q_t\\\\
&= \left(\cos\left(\frac{\left\\|y\_{w,t}+e\_{w,t}\right\\|\Delta t)}2\right)I\_{4\times4}+\frac {\Delta t}2\cdot \frac{\sin\left(\frac{\left\\|y\_{w,t}+e\_{w,t}\right\\|\Delta t}{2}\right)}{\frac{\left\\|y\_{w,t}+e\_{w,t}\right\\|\Delta t}{2}}S(y\_{w,t}+e\_{w,t})\right)q\_t \\\\
& \approx \left(I + \frac {\Delta t}2S(y\_{w,t})\right)q\_t+\frac {\Delta t}2\overline{S}(q\_t)\omega\_t
\label{b1} \tag{10a}\\\\
y\_{a,t} &= R\_t^{S/W}g^W+e\_{a,t} \label{b2} \tag{10b} \\\\ 
y\_{m,t} &= R\_t^{S/W}m^W+e\_{m,t} \label{b3} \tag{10c}
\end{align\*}$$

其中，$g^W$表示世界坐标系下的重力加速度，$m^W$表示世界坐标系下的地磁。

### 先验模型
为了求解平滑问题$\ref{a3}$和滤波问题$\ref{a4}$，需要了解分布$p(x\_1|\theta)$和$p(\theta)$.一般假定$x\_1$和$\theta$相互对立，故需要了解先验分布$p(x\_1)$和$p(\theta)$。
大多数情况下，缺乏对参数$\theta$的先验信息。不过可以使用合理的值来建模参数。比如，对于陀螺仪的零偏可以假定很小，但是可以为正数也可以为负数。合理的先验假设为:
$$b\_{w,t}\sim N(0, \delta\_w^2I\_3)$$
一般，在没有额外的信息确定先验时，可以假定服从一个有大致的方差的正态分布。
对于手机姿态的先验，通常使用第一帧加速计和磁力计的采样值来确定。假定加速计只测量重力向量且磁力计只测量本地的地磁强度。所以加速计可以提供设备的竖直倾角，尽管磁力计也可以提供这个信息，但是实际中加速计提供的信息更加精确。磁力计用来提供南北方向信息，将地磁场和磁力计投影到水平面上来得到。基于给定两个坐标帧下的两个(或更多)线性无关的向量可以确定两个坐标帧间的旋转这一事实，可以求解出设备在世界坐标系中的旋转。故而将这重力方向向量和南北方向向量归一化，有：
$$
\begin{eqnarray}
g^W &= & \begin{pmatrix} 0 & 0 & -1\end{pmatrix} ^T, \quad \quad & g^S &= \frac{y\_{a,1}} {\left\\|y\_{a,1}\\right\\|\_2} \label{b4} \tag{11a} \\\\
m^W &= & \begin{pmatrix} 0 & 1 & 0\end{pmatrix}^T, \quad \quad & m^S &= g^S \times ( \frac{y\_{m,1}} {\left\\|y\_{m,1}\\right\\|\_2} \times g^S ) \label{b5} \tag{11b}
\end{eqnarray}
$$从这四个向量中求解出两个坐标帧相对的旋转，可转化为求解以下优化问题：
$$
\max\_{q^{W/S}} \left\\| \overline{g}^W - q^{W/S}\odot \overline g^S\odot q^{S/W} \right\\|\_2^2+ \left\\| \overline m ^W - q^{W/S}\odot \overline m ^ S \odot q^{S/W} \right\\|\_2^2 \\\\
s.t.\quad \left\\|q^{W/S} \right\\|\_2 = 1 \label{c} \tag{12}
$$
其中$\odot$表示四元数与四元数相乘,$\overline{v}$表示将三维向量表示为四元数形式:
$$
\begin{align\*}
p\odot q &= \begin{pmatrix} p\_0q\_0-p\_v\cdot q\_v \\\\ p\_0q\_v + q\_0p\_v+p\_v\times q\_v \end{pmatrix}, \quad \overline{v} = \left( 0\quad (v)^T \right)^T
\end{align\*}
$$
优化问题$\ref{c}$可以确定一个四元数$q^{W/S}$来最小化归一化的磁场方向和重力方向在世界坐标系和传感器坐标系的表示下的距离。定义矩阵A:
$$A = -(\overline g^W)^L(\overline g^S)^R - (\overline m^W)^L(\overline m^S)^R$$其中，L和R表示四元数乘子：
$$
p^L = \begin{pmatrix}p\_0 & -p\_v^T \\\\ p\_v & p\_0I\_3 + [p_v\times]\end{pmatrix}, \quad q^R = \begin{pmatrix}q\_0 & -q\_v^T \\\\ q\_v & q\_0I\_3-[q\_v\times]\end{pmatrix}
$$其中，$[\cdot \times]$表示三维向量的斜对称矩阵。
优化问题$\ref{c}$转化为求解如下问题：
$$q^{W/S} = \min\_{q^{W/S}}\left(q^{W/S}\right)^T A q^{W/S} \\\\ s.t. \quad \left\\| q^{W/S}\right\\|_2 = 1 \label{c1} \tag{13}$$问题$\ref{c1}$的解是矩阵$A$的最大特征值对应的特征向量。一般认为这个先验给定的先验姿态在68%的情况下误差不超过20°，故而，三个方向上的协方差为：
$$
\Omega\_{3\times3} =e^2I\_{3\times3}, \quad e = \frac {20}{180}\pi = 0.35
$$

<!-- 四元数协方差表示为：
$$
\Omega\_{4\times4} =\frac 14 (q^{W/S})^L \frac{\partial Q(e)}{\partial e}\Omega\_{3\times3}(\frac{\partial Q(e)}{\partial e})^T(q^{S/W})^L
$$其中，$Q(\cdot)$为三维向量表示为单位四元数，对单位四元数的微分如下：
$$\frac{\partial Q(e)}{\partial e} \approx \begin{pmatrix} 0\_{1\times 3} \\\\ I\_{3\times3} \end{pmatrix}$$
 -->
## 算法建模

### 基于优化的姿态平滑估计

$$
\hat{x}\_{1:N}=\min\_{x\_{1:N}}\underbrace{\left\\|e\_1\right\\|^2\_{\Omega\_{x\_1}}}\_{Prior} + \underbrace {\sum\_{t=2}^N\left\\|e\_{w,t}\right\\|^2\_{\Omega\_w}}\_{Dynamics} + \underbrace{\sum\_{t=2}^N(\left\\|e\_{a,t}\right\\|^2\_{\Omega\_a} + \left\\|e\_{m,t}\right\\|^2\_{\Omega\_m})}\_{Measurements}
$$
其中，
$$
\begin{align\*}
e\_{1} &= 2Q^{-1}(\hat{q}\_1^{W/S}\odot q\_1^{S/W}), &e\_1 &\sim N(0, \Omega\_{x\_1}) \\\\
e\_{w,t} &= \frac 2T Q^{-1}(q\_t^{W/S} \odot q\_{t+1}^{S/W}) - y\_{w,t}, &e\_{w,t}&\sim N(0, \Omega\_w) \\\\
e\_{a,t} &= y\_{a,t} - R\_t^{S/W}g^W, & e\_{a,t}&\sim N(0,\Omega\_a) \\\\ 
e\_{m,t} &= y\_{m,t} - R\_t^{S/W}m^W, & e\_{m,t}&\sim N(0,\Omega\_m)
\end{align\*}
$$
式中$Q^{-1}(\cdot)$表示将四元数转换为三元素的向量表示。
$$Q^{-1}(q) = \frac{\arccos q\_0}{\sin (\arccos q\_0)}q\_v=\frac{\arccos q\_0}{\left\\|q\_v\right\\|\_2}q\_v$$

---
输入：初始姿态$q^{W/S}\_0$,惯性测量数据$\left\\{y\_{a,t}, y\_{w,t}\right\\}\_{t=1}^N$,磁力计测量数据$\left\\{y\_{m,t}\right\\}\_{t=1}^N$,初始协方差$\Omega\_w, \Omega\_a, \Omega\_m, \Omega\_{x\_1}$
输出：姿态估计$q^{W}\_{1:N}$和协方差$\Omega\_{q^W\_{1:N}}$
---

### 基于优化的滤波估计
使用平滑的好处是使用所有的测量值$y\_{1:N}$来得到状态$x\_{1:N}$的最有估计。不过，计算消耗和内存需求随着数据集的增长而增加。而且，这是一个后处理解决方案，只有在所有的数据都可用时才能够进行处理。而滤波问题可以建模为如下问题:
$$
\hat x\_{t+1} = \min\_{x\_{t+1}} - \log p(x\_{t+1}|y\_{1:t+1}) = min\_{x\_{t+1}}-\log p(y\_{t+1}|x\_{t+1}) - \log p(x\_{t+1}|y\_{1:t})
$$
先验$p(x\_{t+1}|y\_{1:t})$通过前一个状态$x\_t$得到：
$$p(x\_{t+1}|y\_{1:t})=\int p(x\_{t+1},x\_t|y\_{1:t})dx\_t=\int p(x\_{t+1}|x\_t)p(x\_t|y\_{1:t})dx\_t$$
假定概率分布是高斯分布：
$$
p(x\_{t+1}|x\_t) \sim N(x\_{t+1}; f(x\_t),Q),\\\\
p(x\_{t}|y\_{t+1}) \sim N(x\_{t}; \hat x\_t,P\_{t|t}),
$$积分可以约等于下式：
$$
p(x\_{t+1}|y\_{1:t})\approx N(x\_{t+1}; f(\hat x\_t), F\_tP\_{t|t}F\_t^T+G\_tQG\_t^T)
$$其中$F\_t=\frac{\partial f(x\_t)}{\partial x\_t}$且$G\_t=\frac{\partial f(x\_t)}{\partial e\_t}$,$e\_t$是过程噪声。

### 扩展卡尔曼滤波
扩展卡尔曼滤波计算公式$\ref{a2}$的条件概率分布来进行滤波估计。扩展卡尔曼滤波可以认为是一步使用一次迭代的滤波问题的Guass-Newton优化。扩展卡尔曼假定测量噪声是可叠加的，且过程和测量噪声是零均值的具有固定协方差的高斯分布。状态空间模型如下：
$$
\begin{align\*}
x\_{t+1} &= f\_t(x\_t, u\_t, w\_t)  \label{k1} \tag{k1} \\\\ 
y\_t &= h\_t(x\_t) + e\_t  \label{k2} \tag{k2}
\end{align\*}
$$
其中，$w\_t\sim N(0,Q), e\_t\sim N(0,R)$.
系统状态通过递归的执行一个时间更新和一个测量更新来进行估计。时间更新用来预测下一个时间的状态，根据：
$$
\begin{align\*}
\hat x\_{t+1|t}&=f\_t(\hat x\_{t|t}, u\_t) \label{k3} \tag{k3}\\\\
P\_{t+1|t}&=F\_tP\_{t|t}F\_t^T+G\_tQG^T\_t\label{k4} \tag{k4}
\end{align\*}
$$
其中，
$$
F\_t=\frac{\partial f\_t(x\_t,u\_t,w\_t)}{\partial x}
\biggm|\_{w\_t=0,x\_t=\hat x\_{t|t}},\quad G\_t=\frac{\partial f\_t(x\_t,u\_t,w\_t)}{\partial u\_t}
\biggm|\_{w\_t=0, x\_t=\hat x\_{t|t}} \label{k5} \tag{k5}
$$矩阵$P$表示状态的协方差。$\hat x\_{t+1|t}$和$P\_{t+1|t}$表示:给定直到t时刻的测量，t+1时刻系统的状态估计和状态协方差。类似的，$\hat x\_{t|t}$和$P\_{t|t}$表示给定直到t时刻的测量，t时刻对系统的状态估计和状态协方差。
测量更新采用式$\ref{k2}$的测量模型结合测量值$y\_t$来更新预测的状态估计：
$$
\begin{align\*}
\hat x\_{t|t} &= \hat x\_{t|t-1} + K\_t\varepsilon\_t, \label{k6} \tag{k6} \\\\ P\_{t|t}&=P\_{t|t-1}-K\_tS\_tK\_t^T,\label{k7} \tag{k7}
\end{align\*}
$$其中,
$$
\begin{align\*}
\varepsilon\_t = y\_t - \hat y\_{t|t-1},\quad S\_t = H\_tP\_{t|t-1}H\_t^T,\quad K\_t=P\_{t|t-1}H\_t^TS\_t^{-1},\label{k8} \tag{k8} \\\\
y\_{t|t-1}=h(\hat x\_{t|t-1}),\quad H\_t=\frac{\partial h\_t(x\_t)}{\partial x\_t}\biggm|\_{x\_t=\hat x\_{t|t-1}}\label{k9} \tag{k9}
\end{align\*}
$$
根据$\ref{k6}$和$\ref{k7}$可以迭代执行时间更新和测量更新来估计系统状态和协方差。

<!-- #### 使用四元数作为状态估计姿态
根据上述分析，扩展卡尔曼滤波的难点在于计算矩阵$F\_t,G\_t,H\_t$来执行EKF时间和测量更新。使用四元数表示系统状态，运动模型为：
$$
\begin{align\*}
q^W\_{t+1} &= f\_t(q\_t^W, y\_{w,t},e\_{w,t})=q\_t^W\cdot Q(\frac T2(y\_{w,t} -e\_{w,t})) \\\\
&=(q\_t^W)^L Q(\frac T 2(y\_{w,t}-e\_{w,t})) \label{k10} \tag{k10}
\end{align\*}
$$
其中，$Q(\cdot)$表示将三维向量转化为四元数。对运动模型微分,有:
$$
\begin{align\*}
F\_t &= \frac{\partial f\_t(q\_t^{W/S}, y\_{w,t}, e\_{w,t})}{\partial q\_t^{W/S}}\biggm|\_{e\_{w,t}=0, q\_t^{W/S}=\hat q\_{t|t}^{W/S}}=(Q(\frac T 2 y\_{w,t}))^R, \label{k11} \tag{k11}\\\\
G\_t &= \frac{\partial f\_t(q\_t^{W/S}, y\_{w,t}, e\_{w,t})}{\partial e\_{w,t}}\biggm|\_{e\_{w,t}=0, q\_t^{W/S}=\hat q\_{t|t}^{W/S}} \\\\
&=\frac {\partial }{\partial e\_{w,t}}(q\_t^{W/S})^LQ(\frac T 2 (y\_{w,t}-e\_{w,t}))\biggm|\_{e\_{w,t}=0, q\_t^{W/S}=\hat q\_{t|t}^{W/S}} \\\\
&= -\frac T 2 (\hat q\_{t|t}^{W/S})^L\frac{\partial Q(e\_{w,t})}{\partial e\_{w,t}} \label{k12} \tag{k12}
\end{align\*}
$$
在扩展卡尔曼滤波的测量更新阶段，使用加速计和磁力计的测量值进行更新。测量模型为:
$$
y\_{a,t}=R\_t^{S/W}g + e\_{a,t}, y\_{m,t}=R\_t^{S/W}m^W + e\_{m,t}, \label{k13} \tag{k13}
$$矩阵$H\_t$为:
$$H\_t = \frac {\partial}{\partial q\_t^{W/S}}\begin{pmatrix} R\_t^{S/W}g^W \\\\ R\_t^{S/W}m^W\end{pmatrix}\biggm|\_{q\_t^{W/S}=\hat q\_{t|t-1}^{W/S}} = \begin{pmatrix}
\frac{\partial R\_{t|t-1}^{S/W}}{\partial q\_{t|t-1}^{W/S}}\biggm|\_{q\_t^{W/S}=\hat q\_{t|t-1}^{W/S}}\quad g^W\\\\ \frac{\partial R\_{t|t-1}^{S/W}}{\partial q\_{t|t-1}^{W/S}}\biggm|\_{q\_t^{W/S}=\hat q\_{t|t-1}^{W/S}}\quad m^W 
\end{pmatrix}\label{k14} \tag{k14}$$
微分$\frac{\partial R^{S/W}\_{t|t-1}}{\partial q^{W/S}\_{t|t-1}}$可以通过旋转矩阵与四元数的定义之间的关系进行计算。
$$
\begin{align\*}
R &= q\_vq\_v^T + q\_0^2I\_3+2q\_0[q\_v\times]+[q\_v\times]^2 \\\\
&= \begin{pmatrix}2q\_0^2 -1+2q\_1^2 & 2q\_1q\_2-2q\_0q\_3 & 2q\_1q\_3 + 2q\_0 q\_2 \\\\ 2q\_1q\_2 + 2q\_0q\_3 & 2q\_0^2 - 1 + 2q\_2^2 & 2q\_2q\_3 - 2q\_0 q\_1 \\\\ 2q\_1q\_3 -2q\_0q\_2 & 2q\_2q\_3 + 2q\_0q\_1  & 2q\_0^2-1+2q\_3^2  \end{pmatrix}
\end{align\*} \label{k15} \tag{k15}
$$
根据$\ref{k6}$和$\ref{k7}$来得到的四元数和协方差(记为$\tilde q\_{t|t}^{W/S}, \tilde P\_{t|t}$)不再是归一化的，需要进行归一化处理。
$$
\begin{align\*}
\hat q\_{t|t}^{W/S} = \frac{\tilde q\_{t|t}^{W/S}}{\left\\|\tilde q\_{t|t}^{W/S}\right\\|\_2} , P\_{t|t}=J\_t\tilde P\_{t|t}J\_t^T, \label{k16} \tag{k16}\\\\
J\_t = \frac{1}{\left\\|\tilde q\_{t|t}^{W/S}\right\\|\_2^3}\tilde q\_{t|t}^{W/S}(\tilde q\_{t|t}^{W/S})^T \label{k17} \tag{k17}
\end{align\*}
$$

#### 使用方向微分作为状态估计姿态
扩展卡尔曼滤波的另一个实现是在一个线性点处使用方向微分进行参数化。线性点通过四元数或旋转矩阵进行参数化，记为$\tilde q\_t^{W/S}$或$\tilde R\_t^{W/S}$。方向微分$\eta\_t^S$是扩展卡尔曼滤波中的状态向量。这个实现的优点在于只使用三维状态而不是四维。
在时间更新阶段，使用运动模型来直接更新线性化点：
$$\tilde q\_{t+1}^{W/S} = \tilde q\_t^{W/S}\odot Q(\frac T 2 y\_{w,t}) \label{k18} \tag{k18}$$
$$
\begin{align\*}
\eta\_{t+1}^S &= f\_t(\eta\_t^S,y\_{w,t}, e\_{w,t}) \\\\
&=2\log(\tilde q\_{t+1}^{S/W}\odot \tilde q\_{t}^{W/S}\odot Q(\frac {\eta\_t^b}{2})\odot Q(\frac T 2(y\_{w,t}-e\_{w,t}))) \\\\
&=2\log(Q(-\frac T2y\_{w,t})\odot Q(\frac {\eta\_t^S} 2) \odot Q(\frac T2(y\_{w,t} - e\_{w,t})))
\end{align\*}
$$
 -->

## 实验&mdash;使用扩展卡尔曼求解姿态
以四元数作为系统状态，由公式$\ref{b1}\sim\ref{b3}$，系统的时间更新方程为：
$$
\begin{align\*}
q\_{t+1} &= \left(I +\frac{\Delta t}2S(y\_{w,t})\right)q\_t + \frac {\Delta t}2\overline S(q\_t) \omega\_t \\\\
& = F\_t q\_t + G\_t\omega\_t \\\\
P\_{t+1} &=  F\_tP\_tF\_t^T + G\_tQG\_t^T
\end{align\*}
$$
认为加速计只受重力影响，加速计测量更新方程为：
$$
\begin{align\*}
y\_{a, t} &= Q^T(q\_t)g^W + e\_t^a \\\\
& = h\_t(q\_t) + e\_t^a \\\\
H\_t &= \frac{\partial h\_t(q\_t)}{\partial q\_t} = \left(\frac{\partial Q(q\_t)}{\partial q\_t}\right)^T\\\\
S\_t &= H\_tP\_tH\_t^T + R \\\\
K\_t &= P\_tH\_t^TS\_t^{-1} \\\\
\varepsilon\_t & = y\_{a,t}-Q^T(q\_T)g^W \\\\ 
\hat q\_t &= q\_t + \varepsilon\_t \\\\
\hat P\_t &= P\_t - K\_tS\_tK\_t^T
\end{align\*}
$$
假定周围环境不存在其他磁场，磁力计测量更新方程为：
$$
\begin{align\*}
y\_{m, t} &= Q^T(q\_t)m^W + e\_t^m \\\\
& = h\_t(q\_t) + e\_t^m \\\\
H\_t &= \frac{\partial h\_t(q\_t)}{\partial q\_t} = \left(\frac{\partial Q(q\_t)}{\partial q\_t}\right)^T\\\\
S\_t &= H\_tP\_tH\_t^T + R \\\\
K\_t &= P\_tH\_t^TS\_t^{-1} \\\\
\varepsilon\_t & = y\_{m,t}-Q^T(q\_T)m^W \\\\ 
\hat q\_t &= q\_t + \varepsilon\_t \\\\
\hat P\_t &= P\_t - K\_tS\_tK\_t^T
\end{align\*}
$$

经过一次时间更新方程和两次加速计与磁力计的更新，可以估计出系统状态。


[TOC]















