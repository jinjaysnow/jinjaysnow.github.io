##########################
# Author: Jinjay
# Created On: 201408
# Vision: v0.1
# Used to generate my blog html file
##########################

import markdown, codecs
import os, datetime, sys
from mako.template import Template
import json

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
	md = markdown.Markdown(extensions = ['codehilite', 'extra', 'meta', 'fenced_code', 'tables'])
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

	# generate Keywords files
	if not meta.has_key("keywords"):
		keywords = ["default"]
	else:
		keywords = meta["keywords"]
	print keywords
	for keyword in keywords:
		print "write keywords file w+"
		if not os.path.isfile("keywords.json"):
			element = {keyword: [ dateFolder + "/" + fileName + ".html" ]}
			f = open("keywords.json","w+")
			json.dump(element, f)
			f.close()
		else:
			with open("keywords.json") as f:
				fc = json.load(f)
			if not fc.has_key(keyword):
				fc[keyword] = [dateFolder + "/" +fileName + ".html"]
			else:
				if not (dateFolder + "/" +fileName + ".html") in fc[keyword]:
					fc[keyword].append(dateFolder + "/" +fileName + ".html")
			# delete duplicate elements in the list
			f = open("keywords.json","w+")
			json.dump(fc, f)
			f.close()

	# generate full blog html file
	# TODO: add the blog css
	if not os.path.isdir(dateFolder):
		os.mkdir(dateFolder)

	mytempFile = Template(codecs.open("../templates/head.tm.html", "r", encoding="utf-8").read())
	finalHtml = mytempFile.render(title=fileName, blogbody=html, modifydate=modifyTime.strftime("%Y-%m-%d %H:%I:%S"))

	output_file = codecs.open(dateFolder + "/" + fileName + ".html", "w",
                          encoding="utf-8", 
                          errors="xmlcharrefreplace")
	output_file.write(finalHtml)
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
