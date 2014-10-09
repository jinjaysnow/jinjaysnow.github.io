# encoding:utf8
import urllib2
import os
import threading
import json

# 从文件中读取股票代码
def readCode(filename, codes):
	f = open(filename, "r")
	for line in f.readlines():
		line.strip()
		codes.append(line)
	f.close()

# 根据股票代码获取股票的当日信息，信息格式为
# 0：”大秦铁路”，股票名字；
# 1：”27.55″，今日开盘价；
# 2：”27.25″，昨日收盘价；
# 3：”26.91″，当前价格；
# 4：”27.55″，今日最高价；
# 5：”26.20″，今日最低价；
# 6：”26.91″，竞买价，即“买一”报价；
# 7：”26.92″，竞卖价，即“卖一”报价；
# 8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
# 9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
# 10：”4695″，“买一”申请4695股，即47手；
# 11：”26.91″，“买一”报价；
# 12：”57590″，“买二”
# 13：”26.90″，“买二”
# 14：”14700″，“买三”
# 15：”26.89″，“买三”
# 16：”14300″，“买四”
# 17：”26.88″，“买四”
# 18：”15100″，“买五”
# 19：”26.87″，“买五”
# 20：”3100″，“卖一”申报3100股，即31手；
# 21：”26.92″，“卖一”报价
# (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
# 30：”2008-01-11″，日期；
# 31：”15:05:32″，时间；
# 
def getComInfo(code):
	# 抓取股票信息
	url = "http://hq.sinajs.cn/list=%s" % code
	response = urllib2.urlopen(url)
	javascriptInfo = response.read()
	# 解析成python可识别的信息
	pythonInfo = javascriptInfo[4:]
	exec(pythonInfo)
	company = "hq_str_" + code
	companyInfo = eval(company)
	companyInfo = companyInfo.split(",")
	# 部分股票由于特殊情况没有相应信息
	if len(companyInfo) < 3:
		return
	currentPrice = companyInfo[3]
	# 当前票价小于5元时保存
	if float(currentPrice) < 5.0:
		saveGoodTicket(code)
		print code, companyInfo[0]

# 保存好的股票日K线
def saveGoodTicket(code):
	# # 日K线
	# url = "http://image.sinajs.cn/newchart/daily/n/%s.gif" % code
	# # 周K线
	# url = "http://image.sinajs.cn/newchart/weekly/n/%s.gif" % code
	# 月K线
	url = "http://image.sinajs.cn/newchart/monthly/n/%s.gif" % code
	# 分时线
	# url = "http://image.sinajs.cn/newchart/min/n/%s.gif" % code
	try:
		response = urllib2.urlopen(url)
		data = response.read()
		f = open("goodTicket/" + code +'.gif', "wb")
		f.write(data)
		f.close()
	except Exception, e:
		print e
	finally:
		pass

# 单个线程进行的工作
def singleHandle(codes, test):
	print test
	for code in codes:
		# 去除code中的空白字符
		code = code.strip()
		# 获取信息
		getComInfo(code)

# 每次四个线程获取股票信息
def multiHandle(fourcodes, test):
	threads = [threading.Thread(target=singleHandle, args=(codes, test)) for codes in fourcodes]
	for t in threads:
		t.start()
	for t in threads:
		t.join()

if __name__ == '__main__':
	codes = []
	readCode("codes.txt", codes)
	num = len(codes)
	if not os.path.isdir("goodTicket"):
		os.mkdir("goodTicket")
		print "make dir pic"

	# 设置4个线程
	threadLen = num / 4

	t1 = codes[0: threadLen]
	t2 = codes[threadLen : threadLen*2]
	t3 = codes[threadLen*2 : threadLen *3]
	t4 = codes[threadLen*3 : ]
	t = [t1, t2, t3, t4]
	multiHandle(t, "To Beautiful You")

	print "success"
