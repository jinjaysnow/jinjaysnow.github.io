Title: 	 Use MarkDownPy
Brief:   This is a file introducing how to use python-makdown.
Authors: Jin Jay
Date:    2014-08
base_url: http://jinjaysnow.github.io
keywords: code

## pygmentize 产生代码高亮的css文件
```
pygmentize -S default -f html > default.css
```

## markdown_py 产生html文件
```
markdown_py/markdown2 \*\*.md > \*\*.html
```

## mako 将template变为最终的文件
```
from mako.template import Template
print Template("hello ${data}!").render(data="world")
```

## mako Template 使用
```
% for x in SomeList: // SomeList 不需要用${}括起来
	print ${x}
% endfor
```