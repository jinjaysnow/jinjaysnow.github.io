# encoding: utf-8
import os
import datetime
import json
import codecs

color = (
    "233, 30, 99",
    "156, 39, 176",
    "255, 87, 34",
    "139, 195, 74",
    "205, 220, 57",
    "76, 175, 80",
    "0, 150, 136",
    "0, 188, 212",
    "3, 169, 244",
    "33, 150, 243",
    "63, 81, 181"
)

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


def saveFinalFile(filePath, tempFilePath, keyword, tempData):
    finalTemp = load_utf8(tempFilePath).encode("utf-8")
    finalTemp = finalTemp.replace(keyword, tempData)
    # replace the DATA_FOLDER in blog/index.html
    data_floder = '<a class="mdl-navigation__link" href="#">所有</a>'
    temp = '\n<a class="mdl-navigation__link" href="#">%s</a>'
    try:
        currentDir = os.listdir('blog/')
        for a in currentDir:
            if "20" in a:
                t2 = temp % (a)
                data_floder = data_floder + t2
        finalTemp = finalTemp.replace("{{ DATE_FOLDER }}", data_floder)
    except Exception, e:
        print e
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
    if ("imgurl") in tempData:
        template = imgbox
        data = tempData["imgurl"]
        template = template.replace("{{IMGURL}}", tempData["imgurl"].encode("utf-8"))
    else:
        template = textbox
        template = template.replace("{{BRIEF}}", tempData["brief"].encode("utf-8"))
    blogTemplate = blogTemplate.replace("{{BRIEF}}", tempData["brief"].encode("utf-8"))
    # replace color of blog index.html
    from random import randint
    color_num = randint(0, len(color)-1)
    blogTemplate = blogTemplate.replace("{{COLOR}}", color[color_num])
    blogTemplate = blogTemplate.replace("{{SIDE_COLOR}}", color[(color_num - (len(color)+1)/2)])
    try:
        # replace keywords of blog index.html
        if "default" in tempData["keywords"]:
            blogTemplate = blogTemplate.replace("{{KEYWORDS}}", "无")
        else:
            keyword = ""
            for k in tempData["keywords"]:
                keyword = keyword + k.encode("utf-8") + " "
            blogTemplate = blogTemplate.replace("{{KEYWORDS}}", keyword)
    except Exception, e:
        print "------"
        print tempData
    # replace title of the index.html
    template = template.replace("{{TITLE}}", x)
    template = template.replace("{{URL}}", tempData["url"].encode("utf-8"))
    allbox = allbox + template
    blogTemplate = blogTemplate.replace("{{TITLE}}", x)
    blogTemplate = blogTemplate.replace("{{URL}}", tempData["url"].encode("utf-8"))
    blogbox = blogbox + blogTemplate
    # sitemap
    sitemapTemplate = siteMap.replace("{{URL}}", tempData["url"].encode("utf-8"))
    sitemapTemplate = sitemapTemplate.replace("{{DATE}}", datetime.datetime.fromtimestamp(os.path.getmtime("brief/" + x)).strftime("%Y-%m-%d"))
    sites = sites + sitemapTemplate


saveFinalFile("index.html", "templates/newindex.html", "{{BLOG}}", allbox)
saveFinalFile("blog/index.html", "blog/indextemplate.html", "{{BODY}}", blogbox)
saveFinalFile("sitemap.xml", "sitemapTemplate.xml", "{{URLS}}", sites)
