Title:   test
Image:	 images/snow.jpg
Author: Jin Jay
Date:    2014-08
description: 测试博客开发使用的test文档。
keywords: code
		markdown

# 一级标题
## 二级标题

[百度](http://www.baidu.com)

[<img src="../../images/snow.jpg" width="50px">](http://jinjaysnow.github.io)
> 一盏灯， 一片昏黄； 一简书， 一杯淡茶。 守着那一份淡定， **品读**属于自己的寂寞。 保持淡定， 才能欣赏到最美丽的风景！ *保持淡定*， \*人生从此不再寂寞\*。
  
 
here is code`printf`

```javascript
	for (var i = 0; i < items.length; i++) {
	    console.log(items[i], i); // log them
	}
```

```python
	import markdown2
	import os, datetime, sys

	def generateFile(filePath):
		if not os.path.isfile(filePath):
			print "filepath is not reasonable"
			return
		createTime = os.path.getctime(filePath)
		dateFolder = datetime.date.fromtimestamp(createTime).strftime("%Y-%M")
		modifyTime = datetime.datetime.fromtimestamp(os.path.getmtime("first.md"))
		# generate html file
		html = markdown2.markdown_path(filePath, extras = ["footnotes", "code-color"])
		num = html.find("</h1>")
		if num == -1:
			print "Cannot get the title"
			return
		title = html[0 : (num + 5)]

		html = html[(num + 7):]
		fileName = title[4:(len(title) - 5)]

		if not os.path.isdir(dateFolder):
			os.mkdir(dateFolder)

		f = open(dateFolder + "/" + fileName + ".html", "w")
		f.write(html.encode('utf-8'))
		f.write("<p>" + modifyTime.strftime("%Y-%m-%d %H:%I:%S") + "</p>\r\n")
		f.close()

	# if __name__ == '__main__':
		# sys.exit(generateFile("getFile.md"))

	generateFile("first.md")
```

1. printf
2. cout
3. print

%We could also consider situations such as:%

$ \begin{tabular}{|c|c|c|c|} Name & Age & Degree & Happy \ \hline \ Justin & 21 & Electrical Engineering & Yes \ Miuche & 39 & None & No \ \hline \ \end{tabular} $

Or even: $y = mx + b$
Or even: $e^{\imath x} = \cos{x} + \imath\sin{x}$

$\int ^{1}\_{0}\int ^{x}\_{0}\dfrac {xf\_{x}+yf\_{y}}{x^{2}+y{2}}dxdy$

```
http://jinjaysnow.github.com
```
<http://jinjaysnow.github.com/>

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

[TOC]

