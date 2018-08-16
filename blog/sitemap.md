Title:   让搜索引擎索引你的网站
description:   设置一些内容让搜索引擎索引你的网站。
Author: Jin Jay
Date:    2014-10
keywords: webmaster
          网站站长
          

## Robots.txt
在网站根目录下放置一个文本档案，告诉搜索引擎如何处理你的目录信息。
如：

    User-Agent: *
    Disallow: /brief/
    Disallow: /markdownPreview/
    Disallow: /templates/

## sitemap.xml
使用网站地图文件sitemap.xml告诉搜索引擎文档内容。
如：

    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>http://ijinjay.github.io/</loc>
            <lastmod>2014-10-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
        </url>
        <url>
            <loc>http://ijinjay.github.io/blog/index.html</loc>
            <lastmod>2014-10-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
        </url>
    </urlset>


[TOC]
