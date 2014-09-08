Title:   Probability
Brief:   考研概率论复习。
Authors: Jin Jay
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