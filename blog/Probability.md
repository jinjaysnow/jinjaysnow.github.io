Title:   概率论
description:   概率论相关知识：全概率公式、分布函数、随机变量分布、数字特征、中心极限定理、矩估计等等。
Author: Jin Jay
Date:    2014-09


## 考研概率论复习
### 概率基本公式
$P(A-B) = P(A-AB) = P(A)-P(AB)$
全概率公式： $${A}\_{1}\cdots{A}\_{n} 是 \Omega 的一个分划, 则有 P(B)=\sum \_{i=1}^{n}{P(B|{A}\_{i})\cdot P({A}\_{i})}$$
贝叶斯公式：
$$P({A}\_{i}|B)=\frac {P(B|{A}\_{i})\cdot P({A}\_{i})}{\sum \_{j=1}^{n}{P(B|{A}\_{j})P({A}\_{j})}}$$
条件概率：$$P(A|B)=\frac {P(AB)}{P(B)}$$
独立事件：$P(AB)=P(A)P(B)$ A独立于B，`零概率事件与任何时间相互独立`。

### 分布函数
>设有随机变量X，对任意的$x\in(-\infty,+\infty)$，称$F(x)=P(X\le x)$为随机变量X的分布函数。

#### 分布函数F(x)性质
1. 有界性：$0\le F(x) \le 1$。
2. $F(x)$是$x$的非降函数。
3. $F(x)$右连续。
4. $F(-\infty)=0, F(+\infty)=1$ 。

### 常用离散随机变量分布
#### 两点分布
$X\sim (0-1) \quad 期望EX=p \quad 方差DX=pq$
#### 二项分布
$X\sim B(n,p) \quad P(x=k)=C\_{n}^{k}p^kq^{n-k} 中心项为[(n+1)P] \quad EX=np \quad DX=npq$
#### 泊松定理
$若\lim \_{n\rightarrow \infty}{nP\_n}=\lambda 则$ $$\lim \_{n\rightarrow \infty}{C \_{n}^{k}P\_{n}^{k}(1-P\_{n})^{n-k}} = \frac {\lambda ^{k} \cdot e^{-\lambda}}{k!}$$ $在[\lambda]处取得中心项，EX=\lambda \quad DX=\lambda$
#### 几何分布
$X\sim G(P) \quad P(x=k)=(1-p)^{k-1}p \quad EX=\frac {1}{p} \quad DX=\frac {1-p}{p^2}$
#### 负二项分布
$时间发生k次\quad P(x=k)=C\_{k-1}^{r-1}p^r(1-p)^{k-r} \quad EX=\frac {r}{q} DX=\frac {r(1-p)}{p^2}$

### 概率密度函数
>设随机变量$X$的分布函数为$F(x)$，若存在非负函数$f(x)$，使得对任意实数$x$，有$$F(x)=\int \_{-\infty}^{x}{f(t)}{dt}，$$则称$X$为连续型变量。$f(x)$称为$X$的**概率密度函数**。

#### 概率密度函数性质
1. 非负性 $f(x) \ge 0$。
2. 规范性 $\int \_{-\infty}^{+\infty}{f(x)}{dx}$
$$F(x)=\int \_{-\infty}^x{f(x)}{dx},\quad P(x\in D)=\int \_{D}{f(x)}dx$$

### 常用连续性随机变量分布
#### 均匀分布
$X\sim U[a, b]\quad EX=\frac {a+b}{2} \quad DX=\frac {(b-a)^2}{12}$
#### 指数分布
$X\sim E(\lambda) \quad f(x)=\begin{cases} \lambda e^{-\lambda x} \quad,x\ge 0 \\\\ 0\quad \quad \quad ,x < 0 \end{cases}\quad EX=\frac{1}{\lambda}\quad DX=\frac{1}{\lambda  ^2}$
#### 正态分布
$X\sim N(\mu, \sigma ^2)$ $$f(x)=\frac {1}{\sqrt{2\pi}\sigma}e^{-\frac {(x-\mu)^2}{2\sigma ^2}}$$ $\sigma$越小，曲线越陡峭。标准正态：$X\sim N(0,1)$。

### 随机变量函数的分布
对于$y=g(x)$，利用$f\_{Y}(y)=F\_{Y}^{\prime}(y)$有：$$F\_{Y}(y)=F\_{Y}(Y\le y)=P(g(x)\le y)$$

### 二维随机变量
>联合分布函数$F(x,y)=P(X\le x,Y\le y)=\int \_{-\infty}^{y}{f(x,y)}{dxdy}$
边缘分布$\quad \quad F\_{X}(x)=F(x,+\infty )=\int \_{-\infty}^{x}\int \_{-\infty}^{+\infty}f(x,y)dxdy$
边缘概率密度$\quad f\_{X}(x)=F\_{X}^{\prime}(x)=\int \_{-\infty}^{+\infty}f(x,y)dy$
重要的积分式$\quad\int \_{-\infty}^{+\infty}e^{-x^2}dx=\sqrt{\pi}$
条件分布$\quad \quad f\_{X|Y}(x|y)=\frac {f(x,y)}{f\_{Y}(y)}$($Y=y$条件下$X$的条件概率密度)

### 多维随机变量函数的分布
和的分布$Z=X+Y\quad f\_{Z}(z)=\int \{-\infty}^{+\infty}f(z-y,y)dy=\int \_{-\infty}^{+\infty}f(x,z-x)dx$;$$x,y相互独立时，\quad f\_{z}(z)=\int \_{-\infty}^{+\infty}f\_{X}(x)f\_{Y}(z-x)dx=f\_{X}(x)\*f\_{Y}(x)$$  
商的分布$Z=\frac {X}{Y}\quad f\_{Z}(z)=\int \_{-\infty}^{+\infty}|y|f(zy,y)dy$  
$max\\{X\_1,X\_2,\cdots,X\_n\\}$和$min\\{X\_1,X\_2,\cdots,X\_n\\}$的分布:$$F\_{max}(x)=F\_1(x)F\_2(x)\cdots F\_n(x)\quad \quad F\_{min}(x)=1-[1-F\_1(x)]\cdots[1-F\_n(x)]$$

### 连续型随机变量函数的分布
①. $Y=g(X)$具有单调性时，利用公式求解：
$$f\_Y(y)=\begin{cases} f\_X[g^{-1}(y)]\cdot|[g^{-1}(y)]|, \quad \alpha < x < \beta \\\\ 0,\quad \quad \quad \quad \quad \quad \quad \quad \quad 其他 \end{cases}$$
②. $Y=g(X)$不具有单调性时，用定义求解  
> a. $F\_Y(y) = P(Y\le y)=P(g(x)\le y) = P(x\in D\_y),\quad$其中 $D\_y=\\{x:g(x)\le y\\}$. 
> b. $f\_Y(y)=F\_Y^\prime (y)$.

### 数字特征
#### 期望
离散型$EX=\sum \_{i=1}^{n}x\_ip\_i$，连续型$EX=\int \_{-\infty}^{+\infty}xf(x)dx$  
定理1：$\quad E(Y)=E(g(x))=\int \_{-\infty}^{+\infty}g(x)f(x)dx$  
定理2：$\quad EZ=Eg(X,Y)=\int \_{-\infty}^{+\infty}\int \_{-\infty}^{+\infty}g(xmy)f(x,y)dxdy$  
性质：$\quad EC=C,\quad E(\sum k\_iX\_i)=\sum k\_iEX\_i$，若$X\_1,\cdots,X\_n$相互独立，$E(\prod X\_i)=\prod EX\_i$  
柯西-施瓦兹不等式：$[E(XY)]^2 \le EX^2EY^2$

#### 方差
定义：$DX=E(X-EX)^2\quad $离散型：$DX=\sum (x\_i-EX)^2p\_i\quad $连续型：$DX=\int \_{-\infty}^{+\infty}(x-EX)^2f(x)dx$  
常用公式：$DX=EX^2-(EX)^2$  
切比雪夫不等式：$P(|X-EX|\ge \varepsilon)\le \frac {DX}{\varepsilon ^2}$  
性质：$D(CX)=C^2DX$，$X\_1\cdots X\_n$相互独立时，$D(X\_1+\cdots+D\_n)=DX\_1+\cdots+DX\_n$

#### 协方差
$Cov(X,Y)=E(X-EX)(Y-EY)=E(XY)-EXEY$

#### 相关系数
$\rho\_{XY}=\frac {Cov(X,Y)}{\sqrt {DX}\sqrt {DY}}$  
性质：$|\rho|\le1$，$|\rho|=1$的充要条件是$P(Y=aX+b)=1$，其中a、b为常数.

### 中心极限定理
>随机变量列$\\{X\_n\\}$有有限的期望和方差$EX\_n=\mu,\quad DX\_n=\sigma ^2\neq0$，则$$Y\_n=\frac {\sum \_{i=1}^{n}X\_i-n\mu}{\sqrt n\sigma} = \frac {\frac 1n \sum\_{i=1}^n X\_i-\mu}{\frac {\sigma}{\sqrt n}} \sim N(0,1)$$

### 矩估计
用样本矩估计总体矩。
### 极大似然估计
>寻找似然函数$L(X\_1,\cdots,X\_n;\theta)$，使得$L$取极大的$\theta$即为所求。一般情况，使用$L(\theta)=\prod \_{i=1}^{n}f(X\_i;\theta)$，然后对其求导或取对数后求导$\frac {\partial lnL}{\partial \theta}=0$.

### 无偏性
>设$\hat \theta = \hat \theta (X\_1,\cdots,X\_n)$是参数$\theta$的样本估计量，若$\forall \theta \in \Theta$，有$E\hat \theta = \theta$，则称$\hat theta$是$\theta$的无偏估计。  
话句话说，样本均值$\bar X$总是总体均值$EX$的无偏估计，即$EX=\bar X$.  
$ES^2=\sigma ^2$

性质：$\forall c\_i, \sum c\_i=1;\quad \sum c\_iX\_i = EX$.  
另:$\hat \theta$是$\theta$的无偏估计，$g(\theta)$是$\theta$的函数，$g(\hat \theta)$不一定是$g(\theta)$的无偏估计。且参数$\theta$的无偏估计不唯一。

[TOC]