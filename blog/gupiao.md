Author: Jin Jay
Title: Python抓取股票信息
Date: 2014-10
Image:  static/stock/sh000001.gif
description: 使用Python实现网页信息抓取，对股票进行分形，筛选出个人感兴趣的股票，查看详情。
Keywords: Python
          网页抓取
          股票信息

## Python抓取股票信息
主要参考信息来源：[http://blog.sciencenet.cn/blog-461456-455211.html](http://blog.sciencenet.cn/blog-461456-455211.html)

### 步骤一：获取所有的股票代码
可以在网上搜索股票代码一览表获得，我自己是在东方财富网上获取的，获取时间为2014年10月8日，通过提取html内容得到一个[codes.txt](../../static/stock/codes.txt)

### 步骤二：Python抓取股票信息
主要通过`http://hq.sinajs.cn/list=%s`获取当日股票信息，其中%s为股票代码，得到的是一个JavaScript的语句，需要转化成Python可以识别的语句。新浪的股票数据接口实例：
```
http://hq.sinajs.cn/list=sh601006
```
返回数据为：
```
var hq_str_sh601006="大秦铁路,7.90,7.93,7.92,7.98,7.89,7.91,7.92,29388117,232721144,34300,7.91,117258,7.90,262584,7.89,261200,7.88,138300,7.87,8800,7.92,80770,7.93,364800,7.94,473882,7.95,336194,7.96,2014-10-09,15:03:04,00";
```
数据意义：
```
0：”大秦铁路”，股票名字；
1：”7.90″，今日开盘价；
2：”7.93″，昨日收盘价；
3：”7.92″，当前价格；
4：”7.98″，今日最高价；
5：”7.89″，今日最低价；
6：”7.91″，竞买价，即“买一”报价；
7：”7.92″，竞卖价，即“卖一”报价；
8：”29388117″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”232721144″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”34300″，“买一”申请34300股；
11：”7.91″，“买一”报价；
12：”117258″，“买二”
13：”7.90″，“买二”
14：”262584″，“买三”
15：”7.89″，“买三”
16：”261200″，“买四”
17：”7.88″，“买四”
18：”138300″，“买五”
19：”7.87″，“买五”
20：”8800″，“卖一”申报3100股，即31手；
21：”7.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
30：”2014-10-09″，日期；
31：”15:03:04″，时间；
```

Python抓取部分代码为:
```
# code为股票代码
url = "http://hq.sinajs.cn/list=%s" % code
response = urllib2.urlopen(url)
javascriptInfo = response.read()
# 解析成python可识别的信息
pythonInfo = javascriptInfo[4:]
exec(pythonInfo)
company = "hq_str_" + code
companyInfo = eval(company)
companyInfo = companyInfo.split(",")
```
通过执行上述代码便在companyInfo中存储了股票相应的信息。

### 步骤三：筛选出自己感兴趣的股票
在这里，我设置筛选条件为`当前股票价格<5元`，然后获取月K线图。通过观察月K线来确定是否投资。  
月K线获取的url为：`http://image.sinajs.cn/newchart/monthly/n/%s.gif`，%s为股票代码。  
实例：
```
http://image.sinajs.cn/newchart/monthly/n/sh000001.gif
```
<img src="../../static/stock/sh000001.gif">

### 步骤四：股票数量众多，采用多线程加速获取数据
一般来说，浏览器使用的线程数为4，此处我们也每次采用4个线程。  
```
# 单个线程进行的工作
def singleHandle(codes, hello):
    print hello
    for code in codes:
        # 去除code中的空白字符
        code = code.strip()
        # 获取信息
        getComInfo(code)

# 每次四个线程获取股票信息
def multiHandle(fourcodes, hello):
    threads = [threading.Thread(target=singleHandle, args=(codes, hello)) for codes in fourcodes]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
```
注意：hello字段基本无用，主要是使用一个参数时，Python的线程函数会报参数个数的错误。我尝试去解决它，不过目前无解。

### 步骤五：显示满足条件的股票月K线
虽然可以直接一张一张的翻看图片，但是每次都需要点击鼠标，比较麻烦。我将产生的文件地址写入一个HTML文件中，通过浏览器便可以在一个界面里显示所有的图片文件，便于分析。  

## 总结
Python的网络库很容易上手抓取网页数据，这里只是简单的应用了一下，没有使用正则表达式匹配等手段获取局部数据，程序可以改进的地方还有很多。比如对股票的详细筛选：获取满足条件的股票数据，通过进一步获取更多的信息（公司详情，股本结构等），来进行股票投资。  


## 程序源码
[抓取信息程序源码](../../static/stock/getinfo.py)
[生成网页文件源码](../../static/stock/generateHTML.py)


[TOC]