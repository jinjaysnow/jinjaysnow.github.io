# encoding: utf-8
import os
import datetime
import json
import codecs

if not os.path.isdir("brief"):
	print "There is no brief folder"
	SystemExit("There is no brief folder")
if not os.path.isfile("blog/keywords.json"):
	print "there is no keyword file"
	SystemExit("no keyword")

datedir = os.listdir("blog")
dateFolder = []
for x in datedir:
	if os.path.isdir("blog/" + x):
		dateFolder.append("blog/" + x)

def save_utf8(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)
def load_utf8(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def urlToXml(url):
	return url.replace("&", "&amp;")

def saveFinalFile(filePath, tempFilePath, keyword, tempData):	
	finalTemp = load_utf8(tempFilePath).encode("utf-8")
	finalTemp = finalTemp.replace(keyword, tempData)
	output_file = codecs.open(filePath, "w", encoding="utf-8")
	output_file.write(finalTemp.decode("utf-8"))
	output_file.close()
	print "success generate ", filePath


briefdir = os.listdir("brief")

textbox = load_utf8("templates/textbox.tm.html").encode("utf-8")
imgbox = load_utf8("templates/imagebox.tm.html").encode("utf-8")
blogText = load_utf8("templates/blogindex.html").encode("utf-8")
siteMap = load_utf8("templates/sitemap.tm.xml").encode("utf-8")

allbox = ""
blogbox = ""
sites = ""
for x in briefdir:
	with open("brief/" + x) as f:
		tempData = json.load(f)
	# blog template
	blogTemplate = blogText
	if tempData.has_key("imgurl"):
		template = imgbox
		data = tempData["imgurl"]
		template = template.replace("{{IMGURL}}", tempData["imgurl"].encode("utf-8"))
		blogTemplate = blogTemplate.replace("{{BRIEF}}", "This is an image box, no brief!")
	else:
		template = textbox
		blogTemplate = blogTemplate.replace("{{BRIEF}}", tempData["brief"].encode("utf-8"))
		template = template.replace("{{BRIEF}}", tempData["brief"].encode("utf-8"))
	template = template.replace("{{TITLE}}", x)
	template = template.replace("{{URL}}", tempData["url"].encode("utf-8"))
	allbox = allbox + template
	blogTemplate = blogTemplate.replace("{{TITLE}}", x)
	blogTemplate = blogTemplate.replace("{{URL}}", tempData["url"].encode("utf-8"))
	blogbox = blogbox + blogTemplate
	# sitemap
	sitemapTemplate = siteMap.replace("{{URL}}", urlToXml(tempData["url"].encode("utf-8")))
	sitemapTemplate = sitemapTemplate.replace("{{DATE}}", datetime.datetime.fromtimestamp(os.path.getmtime("brief/" + x)).strftime("%Y-%m-%d"))
	sites = sites + sitemapTemplate


saveFinalFile("index.html", "templates/indextemplate.html", "{{BLOG}}", allbox)
saveFinalFile("blog/index.html", "blog/indextemplate.html", "{{BODY}}", blogbox)
saveFinalFile("sitemap.xml", "sitemapTemplate.xml", "{{URLS}}", sites)

