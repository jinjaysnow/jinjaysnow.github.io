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
import os, datetime, string

createTime = os.path.getctime("first.md")
dateFolder = datetime.date.fromtimestamp(createTime).strftime("%Y-%M")
datetime.datetime.fromtimestamp(os.path.getmtime("first.md"))

html = markdown2.markdown_path("first.md")
num = string.find(html, "</h1>")
title = html[0:(num+6)]
print title

if os.path.isdir(dateFolder):
	pass
else:
	os.mkdir(dateFolder)

