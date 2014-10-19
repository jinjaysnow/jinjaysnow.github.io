Title:   Calculus
Brief:   微积分要点归纳。
Authors: Jin Jay
Date:    2014-09
Description: 微积分总结,Calculus

# 高等数学微积分
## 初等函数
>由常数和基本初等函数经过有限次的四则运算和有限次的函数复合步骤所构成并可用一个式子表示的函数成为初等函数。  

### 极限
#### 数列极限
$\\{x\_n\\}$为一数列，若$\exists  a$，$\forall $给定的正数$\epsilon $，$\exists$正整数$N$，使得$n > N$时，有$|x\_n - a| < \epsilon $，则称常数$a$是数列$\\{x\_n\\}$的极限，$\lim \_{n\rightarrow \infty}{x\_n} = a$.

1. 极限的唯一性：如果{$x\_n$}收敛，那么它的极限唯一。
2. 收敛数列的有界性：{$x\_n$}收敛，则{$x\_n$}一定有界。
3. 收敛数列的保号性：$\lim \_{n\rightarrow \infty}{x\_n} = a$，且$a > 0$，则$\exists N > 0, n > N$时，$x\_n > 0$。
4. 收敛数列与其子数列间的关系：如果{$x\_n$}收敛于a，则它的任意子数列也收敛于a。

#### 函数极限
1. 函数极限的唯一性：如果$\lim \_{x\rightarrow x\_0}{f(x)}$存在，那么这极限唯一。
2. 函数极限的局部有界性：如果$ \lim \_{x\rightarrow x\_0}{f(x)}=A$， 则$\exists$常数$M>0$和$\delta >0$，使得当$0<|x-x\_0|<\delta$时，有$|f(x)|\le M$。
3. 函数极限的局部保号性：如果$\lim \_{x\rightarrow x\_0}{f(x)}=A$，且$A>0$（或$A<0$），则$\exists \delta >0$，使得当$0<|x-x\_0|<\delta$时，有$f(x)>0$（或$f(x)<0$）。
4. 函数极限与数列极限的关系：如果$\lim \_{x\rightarrow x\_0}{f(x)}$存在，{$x\_n$}为函数$f(x)$定义域内任一收敛于$x\_0$的数列，且满足$x\_n\neq x\_0(n\in N^\*)$，则相应的函数值数列{$f(x\_n)$}必收敛，且$\lim \_{n\rightarrow \infty}{f(x\_n)}=\lim \_{x\rightarrow x\_0}{f(x)}$。

#### 极限存在准则
1. 夹逼准则：若{$x\_n$}、{$y\_n$}、{$z\_n$}满足，当$n<n\_0$时，$y\_n\le x\_n \le z\_n$，且$\lim \_{n\rightarrow \infty}{y\_n}=a,\lim \_{n\rightarrow \infty}{z\_n}=a$，则{$x\_n$}的极限存在，且$\lim \_{n\rightarrow \infty}{x\_n}=a$。
2. 单调有界数列必有极限。

### 间断点
如果$x\_0$是函数f(x)的间断点，但左极限$f(x\_0^-)$和右极限$f(x\_0^+)$都存在，则称$x\_0$为f(x)的第一类间断点，不是第一类间断点的任何间断点都称为第二类间断点。  
在第一类间断点中，$f(x\_0^-)=f(x\_0^+)$称可去间断点，否则为跳跃间断点。

### 零点定理
设函数f(x)在闭区间[a,b]上连续，且f(a)与f(b)异号，则在开区间(a,b)内至少有一点$\xi$，使得$f(\xi)=0$。

### 介值定理
设f(x)在[a,b]上连续，且f(a)=A,f(b)=B，那么对A与B之间任意的一个数C，在(a,b)内至少有一点$\xi$，使得$f(\xi)=C$。

## 导数
### 求导法则
1. $[\mu(x)\pm \nu(x)]^\prime = \mu(x)^\prime\pm \nu(x)^\prime$
2. $[\mu(x)\nu(x)]^\prime=\mu^\prime(x)\nu(x)+\mu(x)\nu^\prime(x)$
3. $[\frac{\mu(x)}{\nu(x)}]^\prime=\frac{\mu^\prime(x)\nu(x)-\mu(x)\nu^\prime(x)}{\nu^2(x)}$
4. 反函数的求导法则
    如果函数x=f(y)在区间$I\_y$内单调、可导且$f^\prime(y)\neq 0$，则它的反函数$y=f^{-1}(x)$在区间$I\_x=\\{x | x=f(y)\\}$内也可导，且$[f^{-1}(x)]^\prime=\frac{1}{f^\prime(y)}$或$\frac{dx}{dy}=\frac{1}{\frac{dy}{dx}}$。
5. 复合函数的求导法则
    设y=f($\mu$)，而$\mu=g(x)$且$f(\mu)$与g(x)均可导，则f[g(x)]的符合导数为：
    $$\frac{dy}{dx}=\frac{dy}{d\mu}\cdot\frac{d\mu}{dx}\quad or \quad y^\prime(x)=f^\prime(\mu)\cdot g^\prime(x)$$


### 常用导数表

|      |      |      |      |
| ---- | ---- | ---- | ---- |
| $(x^n)^\prime=nx^{n-1}$ | $(\sin x)^\prime=\cos x$ | $(\cos x)^\prime=-\sin x$ | $(\tan x)^\prime=\sec^2{x}$ |
| $(\cot x)^\prime=-\csc ^2x$ | $(\sec x)^\prime=\sec x\tan x$ | $(\csc x)^\prime=-\csc x\cot x$ | $(a^x)^\prime=a^x\ln a$ |
| $(e^x)^\prime = e^x$ | $(\log \_ax)^\prime=$ $\frac1\{x\ln a\}$ | $(\ln x)^\prime=\frac1x$ | $(\arcsin x)^\prime = \frac 1\{\sqrt\{1-x^2\}\}$ |
| $(\arccos x)^\prime = -\frac 1\{\sqrt\{1-x^2\}\}$ | $(\arctan x)^\prime=\frac1\{1+x^2\}$ | $($arccot $x)^\prime=-\frac 1\{1+x^2\}$ | $\quad$ |

### 罗尔定理
如果函数f(x)满足①在区间[a,b]上连续；②在开区间(a,b)内可导；③在区间端点处的函数值相等，即f(a)=f(b)；那么在(a,b)内至少有一点$\xi (a<\xi <b)$，使得$f^\prime(\xi)=0$。

### 拉格朗日中值定理
如果函数f(x)满足①在闭区间[a,b]上连续；②在开区间(a,b)内可导；那么在(a,b)内至少有一点$\xi(a<\xi<b)$，使等式$f(b)-f(a)=f^\prime(\xi)(b-a)$成立。

### 柯西中值定理
如果函数f(x)及F(x)满足①在区间[a,b]上连续；②在开区间(a,b)内可导；③对任一$x\in(a,b)$，$F^\prime(x)\neq 0$，那么在(a,b)内至少存在一点$\xi$，使等式$\frac{f(b)-f(a)}{F(b)-F(a)}=\frac{f^\prime(\xi)}{F^\prime(\xi)}$成立。

### 洛必达法则
设①当$x\rightarrow a$时，函数f(x)及F(x)都趋近于0；②在点a的某去心邻域内，$f^\prime(x)$及$F^\prime(x)$都存在且$F^\prime(x)\neq0$；③$\lim \_{x\rightarrow a}\frac{f(x)}{F(x)}=\lim \_{x\rightarrow a}\frac{f^\prime(x)}{F^\prime(x)}$。

### 泰勒中值定理
如果函数f(x)在含有$x\_0$的某个开区间(a,b)内具有直到(n+1)阶的导数，则$\forall x\in(a,b)$，有$$f(x)=f(x\_0)+f^\prime(x\_0)(x-x\_0)+\frac{f^{\prime\prime}(x\_0)}{2}(x-x\_0)^2+\cdots+\frac{f^{(n)}(x\_0)_)}{n!}(x-x\_0)^n+R\_n(x),$$其中$R\_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-x\_0)^{n+1}$。

### 凹凸性
设f(x)在(a,b)内具有一阶和二阶导数，在[a,b]上连续，则  
(1) 若在(a,b)内$f^{\prime\prime}>0$，则f(x)在[a,b]上是凹函数。即：$$f(\frac{x\_1+x\_2}2)<\frac{f(x\_1)+f(x\_2)}2$$
(2) 若在(a,b)内$f^{\prime\prime}<0$，则f(x)在[a,b]上是凸函数。即：$$f(\frac{x\_1+x\_2}2)>\frac{f(x\_1)+f(x\_2)}2$$

### 拐点的求法
1. 求$f^{\prime\prime}(x)$
2. 令$f^{\prime\prime}(x)=0$，解出这个方程在区间I内的实数根，并求出在区间I内$f^{\prime\prime}(x)$不存在的点
3. 对步骤2中求出的每一个是跟或二阶导数不存在的点$x\_0$，检查$f^{\prime\prime}(x\_0^-)$，$f^{\prime\prime}(x\_0^+)$，符号相反时，$x\_0$是拐点。

### 极值
设函数f(x)在$x\_0$处可导，且在$x\_0$处取得极值，那么$f^\prime(x)=0$.[**必要条件**]  
设f(x)在$x\_0$处具有二阶导数且$f^\prime(x\_0)=0,f^{\prime\prime}(x\_0)\neq0$，那么  
(1)当$f^{\prime\prime}(x)<0$时，函数f(x)在$x\_0$处取得极大值。  
(2)当$f^{\prime\prime}(x)>0$时，函数f(x)在$x\_0$处取得极小值。

### 高阶导数
|   |   |
|---|---|
| $(e^2)^\{(n)\}=e^2$ | $(\sin x)^\{(n)\}=\sin(x+\frac\{n\pi\}2)$ |
| $(\cos x)^\{(n)\}=\cos(x+\frac\{n\pi\}2)$ | $[\ln(1+x)]^\{(n)\}=(-1)^\{n-1\}\frac\{(n-1)!\}\{(1+x)^n\}$ |
| $(\mu\nu)^\{(n)\}=\sum\_\{k=0\}^nC\_n^k\mu^\{(n-k)\}\nu^\{(k)\}$ |   |

## 积分
### 常用积分表
|      |      |
| ---- | ---- | 
| $\int x^\mu dx=\frac\{x^\{\mu+1\}\}\{\mu+1\}$ | $\int \frac\{dx\}\{x\}=\ln &#124;x&#124;$ |
|$\int \frac\{dx\}\{1+x^2\}=\arctan x$ | $\int \frac\{dx\}\{\sqrt\{1-x^2\}\}=\arcsin x$ | 
| $\int \sin xdx=-cosx$ | $\int \cos xdx=\sin x$ |
| $\int e^xdx=e^x$ |  $\int a^xdx=\frac\{a^x\}\{\ln a\}$ |
| $\int \frac\{dx\}\{a^2+x^2\}=\frac1a\arctan \frac xa$ | $\int \frac\{dx\}\{x^2-a^2\}=frac1\{2a\}\ln&#124;\frac\{x-a\}\{x+a\}&#124;$ |
| $\int \frac\{dx\}\{\sqrt\{a^2-x^2\}\}=\arcsin \frac xa$ | $\int \{dx\}\{\sqrt\{x^2\pm a^2\}\}=\ln (x+\sqrt\{x^2\pm a^2\})$ |
| $\int \sqrt\{a^2-x^2\}dx=\frac\{a^2\}2\arcsin \frac xa+\frac x2\sqrt\{a^2-x^2\}$ | $\int \sqrt\{x^2\pm a^2\}dx=\pm \frac\{a^2\}2\ln&#124;x+\sqrt\{x^2+a^2\}&#124;+\frac x2\sqrt\{x^2+a^2\}$ | 

`注：积分省略了最后的常数项`

### 第一类换元法
设$f(\mu)$具有原函数，$\mu=\varphi(x)$可导，则有$\int f(\varphi(x))\varphi^\prime(x)dx=[f(\mu)d\mu]\_{\mu=\varphi(x)}$。

### 第二类换元法
设$x=\varphi(t)$是单调的、可导的函数，并且$\varphi^\prime(t)\neq0$，又设$f[\varphi(t)],\varphi^\prime(t)$具有原函数，则有$\int f(x)dx=[\int f[\varphi(t)]\varphi^\prime(t)dt]\_{t=\varphi^{-1}(x)}$。

### 分部积分法
$$\int \mu\nu^\prime dx= \mu\nu-\int\mu\prime\nu dx$$

### 定积分中值定理
如果函数f(x)在积分区间[a,b]上连续，则在[a,b]上至少存在一个点$\xi$，有$$\int \_a^bf(x)dx=f(\xi)(b-a).\quad (a\le \xi \le b)$$






[TOC]
