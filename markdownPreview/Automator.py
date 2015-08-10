#!/usr/bin/env python
#coding=utf-8
##########################
# Author: Jinjay
# Created On: 201408
# Vision: v0.1
# Used to generate my blog html file
##########################

import codecs
import os, datetime, sys
import json
from MarkdownPreview import MarkdownCompiler

# color of the web
color = (
    "blue-green",
    "blue-indigo",
    "blue-light_green",
    "blue-red",
    "deep_orange-blue",
    "deep_orange-pink",
    "deep_orange-red",
    "deep_purple-blue",
    "indigo-pink",
    "lime-blue",
    "orange-blue",
    "pink-blue",
    "pink-indigo",
    "purple-blue",
    "purple-green",
    "red-blue",
    "red-deep_orange",
    "red-pink",
    "teal-blue"
)


def jsonWrite(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def fileNameToUrl(fileName):
    return fileName.replace(' ', "%20").replace("&", "&amp;")


def generateFile(filePath):
    if not os.path.isfile(filePath):
        print "filepath is not reasonable"
        return
    modifyTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))

    # generate full blog html file
    mdc = MarkdownCompiler(filePath)
    mdc.default_css = "newmarkdown.css"

    finalHtml, body = mdc.run()
    # delete <div class="toc">
    import re
    toc_pattern = re.compile('<div class="toc">.*?</div>', re.DOTALL)
    match = toc_pattern.search(finalHtml)
    if match:
        toc_content = match.group(0)
        try:
            finalHtml = finalHtml.replace(toc_content, " ")
            finalHtml = finalHtml.replace("{{ TOC }}", toc_content)
            from random import randint
            color_num = randint(0, len(color)-1)
            finalHtml = finalHtml.replace("{{ COLOR }}", color[color_num])
        except Exception, e:
            print "-----color error"
            print e

    # add date
    finalHtml = finalHtml.replace('{{ DATE }}', "<p style=\"text-align: right; color: gray;\"><br>" + modifyTime.strftime("%Y-%m-%d %H:%M:%S") + u"</p>", 1)

    meta = mdc.settings.get("meta", {})
    try:
        fileName = meta["title"][0]
        dateFolder = meta["date"][0]
        brief = meta["description"][0]
    except:
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
    # change use json open
    if meta.has_key("image"):
        briefData = {"brief": brief, "imgurl": "http://jinjaysnow.github.io/" + meta["image"][0], "url": "http://jinjaysnow.github.io/blog/"+dateFolder+"/"+fileName+".html"}
        jsonWrite("../brief/" + fileName, briefData)

    else:
        briefData = {"brief": brief, "url": "http://jinjaysnow.github.io/blog/"+dateFolder+"/"+fileNameToUrl(fileName)+".html"}
        jsonWrite("../brief/" + fileName, briefData)

    # generate Keywords files
    if not meta.has_key("keywords"):
        keywords = ["default"]
    else:
        keywords = meta["keywords"]
    # print keywords
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
                fc[keyword] = [dateFolder + "/" + fileNameToUrl(fileName) + ".html"]
            else:
                if not (dateFolder + "/" +fileName + ".html") in fc[keyword]:
                    fc[keyword].append(dateFolder + "/" + fileNameToUrl(fileName) + ".html")
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
