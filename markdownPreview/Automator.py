##########################
# Author: Jinjay
# Created On: 201408
# Vision: v0.1
# Used to generate my blog html file
##########################

import markdown, codecs
import os, datetime, sys
# from mako.template import Template
import json
from MarkdownPreview import MarkdownCompiler
# from markdownPreview.MarkdownPreview import MarkdownCompiler

def generateFile(filePath):
	if not os.path.isfile(filePath):
		print "filepath is not reasonable"
		return
	# modifyTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))

	# generate full blog html file
	# TODO: add the changedTime

	mdc = MarkdownCompiler(filePath)
	mdc.default_css = "mymarkdown.css"
	finalHtml, body = mdc.run()

	meta = mdc.settings.get("meta", {})

	try:
		fileName = meta["title"][0]
		dateFolder = meta["date"][0]
		brief = meta["brief"][0]
	except :
		print "there is no essential meta"
		return

	if not os.path.isdir("../blog/" + dateFolder):
		os.mkdir("../blog/" + dateFolder)

	output_file = codecs.open("../blog/" + dateFolder + "/" + fileName + ".html", "w",
                          encoding="utf-8", 
                          errors="xmlcharrefreplace")
	
	output_file.write(finalHtml)
	output_file.close()

	# generate Brief File to be used by updateIndex
	if not os.path.isdir("../brief"):
		os.mkdir("../brief")
	briefFile = codecs.open("../brief/" + fileName, "w", encoding="utf-8", errors="xmlcharrefreplace")	
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

if __name__ == '__main__':
	# When there is no args, it will generate all "../blog/.*md" files by default. 
	if len(sys.argv) == 1:
		currentDir = os.listdir('../blog/')
		import re
		pattern = re.compile(r".*md$")
		for afile in currentDir:
			if pattern.match(afile) is not None:
				print "generate file ",afile
				try:
					generateFile('../blog/' + afile)
				except Exception, e:
					raise e
	else:
		SystemExit(generateFile(sys.argv[1]))
