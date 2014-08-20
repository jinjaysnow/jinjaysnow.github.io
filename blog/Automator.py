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