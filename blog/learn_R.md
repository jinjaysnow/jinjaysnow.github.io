Author: Jin Jay  
Title: R语言学习之路
Date: 2014-05
description: 学习R语言的一些问题整理，心得体会。 
keywords: R


### [学习R语言之路](https://github.com/ijinjay/R)

---

#### 记录学到的一些函数
安装包 install.packages(packageName)

使用包require()/libarary()

list() 列表类型，访问使用$ 或 [[]] 

data.frame(a, b, c) 数据帧，长度相同的向量的列表； 访问data.frame中的元素使用[[]]双中括号，或者使用 frameName$elementName 访问, 与list不同的是data.frame 是一种类似数据库存储的结构，每一行代表一个数据项。

new.env(hash = TRUE, parent = parent.frame(), size = 29L) environment 与 list 的区别主要在两个方面：

> environment只能通过子变量名来访问（使用operator $ or [[），它的子变量没有排序，所以不能通过id来访问。
> environment在做为参数传入程序时，并不进行拷贝，而是传递一个地址。这就意味着我们在编写程序时可以使用environment来实现以形参的形式来对数据进行修改。

``` R
f <- function();
enviroment(f);
mget(c(...), envir = env, ifnotfound=NA);# 获取所有的环境值
```
contour(matrix): 绘制矩阵的等高线图

persp(matrix, expand = 0.2): 矩阵透视图, expand参数可选，表示z轴放大比例

image(matrix): 矩阵彩色热图

barplot(x): 绘制条形图

abline(h=?,v=?): 绘制一条参考的直线，h代表水平线，v代表垂直线

mean(): 平均值 median(): 众数 sd(): 方差 

legend(): 在图的某一个位置做标记对图进行说明

``` R
legend("topright", c("gems", "gold", "silver"), pch=1:3)
```

读取文件中的数据 csv格式： read.csv(filename) 返回一个frame对象

通用读取文件的方法

``` R
read.table(file, header = FALSE, sep = "", quote = "\"'",
           dec = ".", row.names, col.names,
           as.is = !stringsAsFactors,
           na.strings = "NA", colClasses = NA, nrows = -1,
           skip = 0, check.names = TRUE, fill = !blank.lines.skip,
           strip.white = FALSE, blank.lines.skip = TRUE,
           comment.char = "#",
           allowEscapes = FALSE, flush = FALSE,
           stringsAsFactors = default.stringsAsFactors(),
           fileEncoding = "", encoding = "unknown", text, skipNul = FALSE)
           # header表示是否包含数据的标题， sep表示数据间隔的字符（一般为\t）
```

```R
plot（x, y, xlab="recall", ylab="precision", type="l", lty=1, col=3, xlim=c(0,1), ylim=c(0, 0.04), lab=c(10, 10, 5), las=1, mgp=c(3. 0.5, 0), tck=0.02, xaxs="i", yaxs="i")

xlim：这是x轴数据的边界；

lab：The first two numbers are the desired number of tick intervals on the x and y axes respectively. The third number is the desired length of axis labels, in characters (including the decimal point.)

las=1 ：Orientation of axis labels. 0 means always parallel to axis, 1 means always horizontal, and 2 means always perpendicular to the axis.

mgp=c(3. 0.5, 0)：Positions of axis components. The first component is the distance from the axis label to the axis position, in text lines. The second component is the distance to the tick labels, and the final component is the distance from the axis position to the axis line (usually zero). Positive numbers measure outside the plot region,

negative numbers inside.

tck=0.02：Length of tick marks, as a fraction of the size of the plotting region. When tck is small (less than 0.5) the tick marks on the x and y axes are forced to be the same size.

yaxs="i" Axis styles for the x and y axes, respectively. With styles "i" (internal) and "r" (the default) tick marks always fall within the range of the data, however style "r" leaves a small amount of space at the edges. (S has other styles not implemented in R.)

要想坐标（0，0）在坐标轴原点，xlim和ylim必须从0开始，xaxs和yaxs也必须是i。
```

#### 外存存取数据
| 包 | 描述 |
|----|------|
| ff | 提供了一种数据结构，保存在硬盘中，但是操作起来就如同在内存中一样|
| bigmemory | 支持大规模矩阵的创建、储存、读取和操作。矩阵被分配到共享内存或内存映射的文件中（memory-mapped files） |
| filehash | 实现了简单的key-value数据库，在其中特征字符串key与存储在硬盘中的数据value相关联。 |
| RODBC, RMySQL, ROracle, RPostgreSQL, RSQLite | 可以用这些包读取外部关系数据库管理系统的数据 |

[TOC]