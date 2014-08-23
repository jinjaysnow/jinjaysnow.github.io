import os, sys
import re, json
import codecs
from mako.template import Template

if not os.path.isdir("brief"):
	print "There is no brief folder"
	SystemExit("There is no brief folder")
if not os.path.isfile("blog/keywords.json"):
	print "there is no keyword file"
	SystemExit("no keyword")

# add date folder
datedir = os.listdir("blog")
dateFolder = []
for x in datedir:
	if os.path.isdir("blog/" + x):
		dateFolder.append("blog/" + x)

# add keyword folder
with open("blog/keywords.json", mode='r') as f:
	keywords = json.load(f)

mytempFile = Template(codecs.open("templates/index.tm.html", "r", encoding="utf-8").read())
html = mytempFile.render(dateFolder = dateFolder, keywordsFolder = keywords.keys(), body="I am desiging...")
print html
