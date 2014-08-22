## Universal
```
* {
	margin: 0; // 外部边距
	padding: 0; // 内部边距
	font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
	box-sizing: border-box; // 允许以特定的方式定义某个区域的特定元素,元素的任何内边距和边框都将在已设定的宽度和高度内绘制。
				// 通过已设定的宽度和高度减去边框和内编剧才能得到内容的宽度和高度。
	-moz-box-sizing: border-box; // Firefox
	-webkit-box-sizing: border-box; // Safari
	font-size: 14px;
}
```

## Body
body {
	-webkit-foot-smoothing: antialiaseda; // 设置字体抗锯齿
	-webkit-text-size-adjust: none;
	width: 100% !important;
	height: 100%;
	line-height: 1.5; // 行高
}
```

## Image
```
img {
	max-width: 100%;
}
```

## Container
```
.container {
	display: block !important; // 显示为块级元素，元素前后带有换行符
	margin: 0 auto !important;
	clear: both !important; // 在元素左右两边都不能出现浮动元素
}
```

## Typography
```
h1, h2, h3 {
	font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
	color: #000; // 黑色
	margin: 40px 0 0;
	line-height: 1.2;
	font-weight: 400;
}
h1 {
	font-size: 32px;
	font-weight: 500;
}
h2 {
	font-size: 24px;
}
h3 {
	font-size: 18px;
}
h4 {
	font-size: 14px;
	font-weight: 600;
}
p, ul, ol{
	marigin-bottom: 10px;
	font-weight: normal;
}
p li, ul li, ol li {
	margin-left: 5px;
	list-style-position: inside; // 列表项标记放置在文本以内，且环绕文本根据标记对齐
}
```

## Links
```
a {
	color: white;
	text-decoration: none;
}
```

## Nav-bar
```
.nav {
	background: rgb();
	z-index: 1023;
	position: fixed; // 固定
	height: 10%;
	width: 100%;
	margin: 0;
	border: solid; // 待定
	filter: alpha(Opacity=80);// 半透明
	-moz-opacity:0.5;
	opacity: 0.5;
}
```

## Right-side
```
.right-side {
	position: fixed;
	left: 61.8%;
}
```

## Button&Select
```
button, select {
	background: transparent; // 透明
	min-height: 40px;
	position: absolute; // 相对于包含它的元素的坐标，通过left、top、right、bottom设定。
}
```

## ImageBox
```
.imagebox {
	background: transparent;
}
```

## Wordbox
```
.wordbox {
	background: transparent;
}
```

## Responsive and mobile friendly styles
```
@media only screen and (max-width: 640px) {
	h1, h2, h3, h4 {
		font-weight: 600 !important;
		margin: 20px 0 5px !important;
	}
	h1 {
		font-size: 22px !important;
	}
	h2 {
		font-size: 18px !important;
	}
	h3 {
		font-size: 16px !important;
	}
	.container {
		width: 100% !important;
	}
}
```
