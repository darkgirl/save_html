#!/usr/bin/env python
# coding=utf-8
import os
import re
import time
import logging
import traceback
# import pdfkit
import requests
from bs4 import BeautifulSoup
from lxml import etree as e, html as h
import lxml
# from PyPDF2 import PdfFileMerger

import save_html

html_template = """
<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8"/>
	<title>%(title)s</title>
	<style type="text/css">
		* {
			word-wrap:break-word;
		}
		pre {
			white-space: pre-wrap;
			word-wrap: break-word;
		}
	</style>
</head>

<body>
%(content)s
</body>

<script>
	let imgNodeList = document.getElementsByTagName("img");
	for (let i = 0; i < imgNodeList.length; i++) {
		if (imgNodeList[i].width > document.body.clientWidth) {
			imgNodeList[i].width = document.body.clientWidth;
		}
	}

	let preArray = document.getElementsByTagName("pre");
	for (let i = 0; i < preArray.length; i++) {
		let width = preArray[i].getBoundingClientRect().width;
		if (width > document.body.clientWidth) {
        		let x = preArray[i].getBoundingClientRect().x;
        		preArray[i].setAttribute("style", "width:" + (document.body.clientWidth - x) + "px");
		}
	}
</script>
</html>
"""

exclude_tags_default = ["script", "style", "video", "audio", "source", "track", "embed"]
config = {
	"include_tags": ["body"],
	"exclude_tags": exclude_tags_default,
	"directory": "./",
	"render": False,
	"overwrite": False,
}

def article_content(html, tag):
	soup = BeautifulSoup(html, "lxml")
	return str(soup.select(tag)[0])

# def fill_page(title, content):
# 	soup = BeautifulSoup(html_template, "lxml")
# 	title_node = soup.select("title")[0]
# 	body_node = soup.select("body")[0]
# 	title_node.append(title)
# 	content_soup = BeautifulSoup(content, "lxml")
# 	body_node.append(content_soup.contents[0])
# 	return str(soup)

def fill_page(title, content):
	return html_template % ({"title": title, "content": content})

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# 1       0.000    0.000    6.618    6.618   save_pdf.py:82(remove_tag)
# def remove_tags(html, exclude_tags):
# 	soup = BeautifulSoup(html, "lxml")
# 	tag_list = []
# 	for tag in exclude_tags:
# 		tag_list.extend(soup.select(tag))
# 	for tag in tag_list:
# 		# print str(tag)
# 		tag.decompose()
# 		# tag.extract()
# 		pass
# 	return str(soup)

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# 1       0.000    0.000    0.076    0.076   save_pdf.py:97(remove_tags)
def remove_tags(html, exclude_tags):
	tag_list = []
	utf8_parser = h.HTMLParser(encoding='utf8')
	page = h.fromstring(html, parser=utf8_parser)
	for tag in exclude_tags:
		tag_list.extend(page.cssselect(tag))
	for tag in tag_list:
		tag.drop_tree()
	return h.tostring(page)

def validate_filename(file_name):
	rstr = r"[\/\\\:\*\?\"\<\>\|]" # '/\:*?"<>|'
	file_name = re.sub(rstr, "", file_name)
	return file_name

def save_pdf(url, include_tags = [], exclude_tags=exclude_tags_default, directory="./", render=False, headers={}, overwrite=False):
	save_html.get_host(url)
	# headers = {
	# 	"Cookie": "PHPSESSID=kpgn3m9rh5jp1dhnqbbfm380d2; acw_sc__=5b7eb8d3efefea56dbba1714e16cc2db139164c1;",
	# 	# "Cookie": "acw_tc=AQAAAGe8mj2GEAYAFQto36egtfafo+cz;",
	# }
	html = ""
	if render:
		html = save_html.get_rendered_data(url)
	else:
		html = save_html.get_data(url, headers)
	# print html
	title = save_html.page_title(html)
	print title

	# file_name = os.path.join(directory , title.strip() + ".html")
	# file_name = directory + title.strip().replace("/", " ").replace("|", " ").replace("?", " ") + ".html"
	file_name = directory + validate_filename(title.strip()) + ".html"
	file_name = file_name.decode("utf-8")
	if os.path.exists(file_name) and not overwrite:
		return

	content = ""
	for tag in include_tags:
		html = article_content(html, tag)
		content += save_html.find_image_url(html)

	content = remove_tags(content, exclude_tags)

	html = fill_page(title, content)
	if not os.path.exists(directory):
		os.makedirs(directory)
	print file_name
	try:
		fhandle = open(file_name, "w")
		print file_name
		fhandle.write(html)
		fhandle.close()
	except Exception as e:
		print e.message
		traceback.print_exc()
		raise e
	finally:
		# fd.close()
		pass

def save_pdf_config(url, config = config):
	save_pdf(url, config["include_tags"], config["exclude_tags"], config["directory"], config["render"])

def main():
	# # save_pdf("https://paper.seebug.org/676/", "main")
	# exclude_tags_default.extend([".panel-weixin", "script", "style"])
	# save_pdf("http://www.freebuf.com/articles/database/182160.html", ["div .articlecontent"])
	# save_pdf("https://linux.cn/article-9942-1.html", "#article_content")
	# save_pdf("https://xz.aliyun.com/t/2622", ["div .content"])
	# save_pdf("https://bbs.pediy.com/thread-246362.htm", "div .card")
	# save_pdf("http://www.4hou.com/technology/13031.html", ".article_cen")
	# save_pdf("https://lichao890427.github.io/wiki/static%20binary%20analysis/", ".article-content")
	# save_pdf("https://kymjs.com/code/2018/08/22/01/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io", ["#myArticle"], ["script", "style", ".support-author"])
	# save_pdf("https://blog.csdn.net/class_brick/article/details/72782772", [".blog-content-box"])
	# save_pdf("http://skysec.top/2018/08/24/Crypto%E4%B9%8B%E5%87%BB%E7%A0%B4%E5%A4%9A%E5%B1%82%E5%8A%A0%E5%AF%86/#%E5%90%8E%E8%AE%B0", ["article"], render = True)
	# save_pdf("https://www.jb51.net/article/92684.htm", ["#content"])
	# save_pdf("https://lgtm.com/blog/apache_struts_CVE-2018-11776", [".postContent"], render = True)
	# save_pdf("https://ialloc.org/blog/python-runtime-debugging/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io", ["article"])
	# save_pdf("https://mp.weixin.qq.com/s/aOQUnuf2_V_XehOxi2FdSQ", ["#img-content"], ["script", "style", "[data-mpa-template-id=\"527\"]", "[data-mpa-template-id=\"1025112\"]"])
	# save_pdf("http://www.w3school.com.cn/cssref/css_selectors.asp", [".dataintable"])
	# save_pdf("https://blog.csdn.net/prefect2011/article/details/79209410", [".blog-content-box"])
	# save_pdf("https://www.cnblogs.com/lsgxeva/p/7689995.html", ["#cnblogs_post_body"])
	exclude_tags_default.append(".art_xg")
	save_pdf("https://www.jb51.net/article/63244.htm", ["#content"], exclude_tags_default, overwrite=True)
	# save_pdf("https://mp.weixin.qq.com/s?__biz=MzAxMTg2MjA2OA==&mid=2649842700&idx=1&sn=3ea966869a96c36836aba920c774f0c3&chksm=83bf6d57b4c8e44110a7ce046a1a95d9847e2ccf3e7c0a1fac95b889ae2a55ace725e2630694&mpshare=1&scene=1&srcid=08274jZrmzWIsIE0XWe7Twtf&key=a417f84fa8900397b35f2e488345d9bb3d92fba17790a91b7424e786c80aee8480c7e4c4daea89bfdb90b2bc4643d2bcf5c78bb15f5a7b73d5f12c820eeddaa150ce7e529f6a55942ba1f534c35e5a45&ascene=1&uin=MTk4MjE1MDAyMA%3D%3D&devicetype=Windows-QQBrowser&version=6103000b&lang=zh_CN&pass_ticket=IEN1TfnhjFVmNuqr%2FHIZyI%2BpHw53DMZ6S7gaoqqMhUc2jisZbNIHCJyqrA5AQXsm",
	# 	["#img-content"],
	# 	["script", "style", "[data-copyright]"])
	# save_pdf("https://daily.zhihu.com/story/9693893?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io", [".question"])
	# save_pdf("https://mp.weixin.qq.com/s/H5wBNAm93uPJDvCQCg0_cg", ["#img-content"])
	# config["include_tags"] = ["article"]
	# config["exclude_tags"].append(".copyright+div")
	# save_pdf_config("https://kiwenlau.com/2018/08/27/code-interview-data-structure/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io", config)
	# config["include_tags"].append(".post-body__content")
	# save_pdf_config("https://code.tutsplus.com/zh-hans/tutorials/the-30-css-selectors-you-must-memorize--net-16048", config)
	# config["directory"] = "./anquan/"
	# save_pdf_config("https://wooyun.js.org/drops/黑狐木马最新变种——“肥兔”详细分析.html", config)
	pass

if __name__ == '__main__':
	main()