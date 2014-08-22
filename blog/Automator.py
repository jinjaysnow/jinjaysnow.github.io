# import markdown2
# # markdown(text, html4tags=False, tab_width=4, safe_mode=None, extras=None, link_patterns=None, use_file_vars=False)

# # markdown_path(path, 
# # 				encoding='utf-8', 
# # 				html4tags=False, 
# # 				tab_width=4, 
# # 				safe_mode=None, 
# # 				extras=None, 
# # 				link_patterns=None, 
# # 				use_file_vars=False)


import markdown2
import markdown, codecs
import os, datetime, sys

def generateFile(filePath):
	if not os.path.isfile(filePath):
		print "filepath is not reasonable"
		return
	createTime = os.path.getctime(filePath)
	# dateFolder = datetime.date.fromtimestamp(createTime).strftime("%Y-%m")
	modifyTime = datetime.datetime.fromtimestamp(os.path.getmtime("first.md"))
	# generate html file
	# html = markdown2.markdown_path(filePath, extras = ["footnotes", "code-color"])
	text = codecs.open(filePath, mode="r", encoding="utf-8")
	text = text.read()
	md = markdown.Markdown(extensions = ['codehilite', 'extra', 'meta'])
	html = md.convert(text)
	meta = md.Meta

	try:
		fileName = meta["title"][0]
		dateFolder = meta["date"][0]
	except Exception, e:
		print "there is no essential meta"
		return


	if not os.path.isdir(dateFolder):
		os.mkdir(dateFolder)

	f = open(dateFolder + "/" + fileName + ".html", "w")
	f.write(html.encode('utf-8'))
	f.write("<p>" + modifyTime.strftime("%Y-%m-%d %H:%I:%S") + "</p>\r\n")
	f.close()
# if __name__ == '__main__':
	# sys.exit(generateFile("getFile.md"))

generateFile("first.md")