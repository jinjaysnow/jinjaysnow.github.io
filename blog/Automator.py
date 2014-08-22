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


# import markdown2
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
	text = codecs.open(filePath, mode="r", encoding="utf-8")
	text = text.read()
	# markdown extensions
	md = markdown.Markdown(extensions = ['codehilite', 'extra', 'meta'])
	html = md.convert(text)
	meta = md.Meta

	try:
		fileName = meta["title"][0]
		dateFolder = meta["date"][0]
		brief = meta["brief"][0]
	except Exception, e:
		print "there is no essential meta"
		return

	# generate Brief File to be used by updateIndex
	if not os.path.isdir("../brief"):
		os.mkdir("../brief")
	briefFile = codecs.open("../brief" + "/" + fileName, "w", encoding="utf-8", errors="xmlcharrefreplace")	
	if meta.has_key("image"):
		# TODO: add the imagebox css
		briefFile.write("<div class=\"imagebox\"><h1>" + fileName + "</h1>")
		briefFile.write("<img src=\""+ meta["image"][0] + "\">")
	else:
		# TODO: add the wordbox css
		briefFile.write("<div class=\"wordbox\"><h1>" + fileName + "</h1>")
	briefFile.write(markdown.markdown(brief))
	briefFile.write("</div>")
	briefFile.close()

	# generate full blog html file
	# TODO: add the blog css
	if not os.path.isdir(dateFolder):
		os.mkdir(dateFolder)

	output_file = codecs.open(dateFolder + "/" + fileName + ".html", "w",
                          encoding="utf-8", 
                          errors="xmlcharrefreplace")
	output_file.write(codecs.open("../templates/head.tm.html", "r", encoding="utf-8").read())
	output_file.write(html)
	output_file.write("<p>" + modifyTime.strftime("%Y-%m-%d %H:%I:%S") + "</p>\r\n\t<body>\r\n</html>")
	output_file.close()

if __name__ == '__main__':
	# When there is no args, it will generate all ".*md" files by default. 
	if len(sys.argv) == 1:
		currentDir = os.listdir('./')
		import re
		pattern = re.compile(r".*md$")
		for afile in currentDir:
			if pattern.match(afile) is not None:
				print "generate file ",afile
				try:
					generateFile(afile)
				except Exception, e:
					raise e
	else:
		SystemExit(generateFile(sys.argv[1]))
