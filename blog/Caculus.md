Title:   Caculus
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




[TOC]
