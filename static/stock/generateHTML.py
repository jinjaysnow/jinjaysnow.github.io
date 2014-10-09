# encoding=utf8
import os
htmlHead = '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html>
</head>
<body>
{{BODY}}
</body>
</html>
'''
if __name__ == '__main__':
	files = os.listdir("goodTicket")
	htmlBody = "<ul>"
	for filename in files:
		htmlBody = htmlBody  + "<li><img src=\"%s\"></li>" % ("goodTicket/" + filename)

	htmlBody = htmlBody + "</ul>"

	html = htmlHead.replace("{{BODY}}", htmlBody)
	f = open("pic.html", "w")
	f.write(html)
	f.close()

