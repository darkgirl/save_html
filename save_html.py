#!/usr/bin/env python
#coding=utf-8


import urllib
import urllib2
import  ssl
from bs4 import BeautifulSoup
import base64
import re
import sys
from gzip import GzipFile
from StringIO import StringIO
from selenium import webdriver

import time
import os
# set the position of chrome-driver
if os.uname()[0] == "Linux":
	os.environ['PATH'] = "/usr/lib/chromium-browser/:" + os.environ['PATH']
elif os.uname()[0] == "Windows":
	os.environ['PATH'] = "./Chrome/Application/;" + os.environ['PATH']


# import cookielib
# #声明一个CookieJar对象实例来保存cookie
# cookie = cookielib.CookieJar()
# #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
# handler = urllib2.HTTPCookieProcessor(cookie)
# #通过handler来构建opener
# opener = urllib2.build_opener(handler)
# #此处的open方法同urllib2的urlopen方法，也可以传入request

data_url_format = "data:image/%(image_type)s;base64,%(image_base64)s"
style_format = "<style type=\"text/css\">\n%(css_text)s</style>"

protocol = ""
host = ""
referer = ""
website = ""
path = ""
global_headers = {}

_protocol = ""
_host = ""
_referer = ""
_website = ""
_path = ""

# def set_extra_headers(_headers):
# 	global headers

def get_host(url):
	global protocol
	global host
	global referer
	global website
	global path
	protocol, s1 = urllib.splittype(url)
	host, path = urllib.splithost(s1)
	website = protocol + "://" + host
	referer = website  + "/"

	# print protocol
	# print host
	# print referer
	# exit(0)
	return host

def get_temp_host(url):
	global _protocol
	global _host
	global _referer
	global _website
	global _path
	_protocol, s1 = urllib.splittype(url)
	_host, _path = urllib.splithost(s1)
	_website = _protocol + "://" + _host
	_referer = _website  + "/"

	# print protocol
	# print host
	# print referer
	# exit(0)
	return _host

def page_title(html):
	bsObj = BeautifulSoup(html, "lxml")
	title = bsObj.select("title")
	return str(title[0].contents[0].encode('utf-8'))

# 外部样式表
# 当样式需要被应用到很多页面的时候，外部样式表将是理想的选择。使用外部样式表，你就可以通过更改一个文件来改变整个站点的外观。

# <head>
# <link rel="stylesheet" type="text/css" href="mystyle.css">
# </head>
# 内部样式表
# 当单个文件需要特别样式时，就可以使用内部样式表。你可以在 head 部分通过 <style> 标签定义内部样式表。

# <head>

# <style type="text/css">
# body {background-color: red}
# p {margin-left: 20px}
# </style>
# </head>
def external_css_to_internal_css(css_url):
	return get_data(css_url)
	# pass
def gzip_unpack(data):
	buf = StringIO(data)
	f = GzipFile(fileobj=buf)
	return f.read()

def get_data(url, headers = {}, content_type = {}):
	print url
	get_temp_host(url)
	global _host
	global _referer
	global global_headers
	if len(headers) > 0:
		global_headers = headers
	_headers = {
		"Host": _host,
		"Referer": _referer,
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36",
		# "Cookie": "comment_author_email_e7382aacd190d171a15486ff88d472d4=178344859%40qq.com; comment_author_e7382aacd190d171a15486ff88d472d4=%E5%B9%95%E5%88%83; acw_tc=AQAAAM+xtjBw7QoAyjKIdSS0WtHc1ekT; PHPSESSID=hktconai6jh2934b4htm4vlmo1; Hm_lvt_cc53db168808048541c6735ce30421f5=1534786653,1534818378,1534826430,1534905415; 3cb185a485c81b23211eb80b75a406fd=1534925182; acw_sc__=5b7d2e3e4dea9aa5630697a57b5f3722d705a095; Hm_lpvt_cc53db168808048541c6735ce30421f5=1534930892"
	}
	_headers.update(headers)
	_headers.update(global_headers)
	print _headers
	req = urllib2.Request(url, headers = _headers)
	# res = urllib2.urlopen(req)
	# solve ssl error
	res = urllib2.urlopen(req, context=ssl._create_unverified_context())
	print res.info()
	# print res.headers["Content-Type"]\
	try:
		content_type["type"] = res.headers["Content-Type"].split("/")[1]
		pass
	except Exception as e:
		pass
	print content_type

	data = res.read()
	return data
	# return gzip_unpack(data)

def get_rendered_data(url, headers = {}):
	# 创建chrome参数对象
	chrome_options = webdriver.ChromeOptions()


	# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
	chrome_options.set_headless()
	# chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错

	chrome_options.add_argument("–start-maximized") # –start-maximized 启动就最大化
	# chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
	chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
	chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
	chrome_options.add_argument('--blink-settings=imagesEnabled=false') #不加载图片, 提升速度
	chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
	chrome_options.add_argument("--ignore-certificate-errors");
	chrome_options.add_argument('lang=zh_CN.UTF-8')
	if False:
		chrome_options.binary_location = "./Chrome/Application/chrome.exe" #手动指定使用的浏览器位置

	# 创建chrome无界面对象
	driver = webdriver.Chrome(options=chrome_options)
	# driver = webdriver.Chrome()
	html = ""
	try:
		driver.get(url)
		time.sleep(5)
		html = driver.find_element_by_css_selector("html").get_attribute("outerHTML").encode("utf-8")
		pass
	except Exception as e:
		raise e
		pass
	finally:
		driver.close()
		driver.quit()
		pass
	return html

# data:image/png;base64,　iVBORw0KGgoAAAANSUhEUg
def image2base64(image_url, content_type = {}):
	data = get_data(image_url, content_type = content_type)
	# print content_type
	return base64.b64encode(data)

def image_url_to_data_url(image_url):
	content_type = {}
	image_type = "png"
	image_base64 = image2base64(image_url, content_type)
	print content_type
	if content_type.get("type") != None:
		image_type = content_type["type"]
	return data_url_format % ({"image_type": image_type, "image_base64": image_base64})

def get_lazy_load_url(image_node):
	for key in image_node.attrs:
		# print image_node[key];
		image_url = image_node[key]
		# if re.match("data-\\w", key) != None and re.match(".+\\.(gif|jpeg|png)$", image_url):
		if re.match("data-\\w", key) != None and re.match("(https?://.+|.+\\.(gif|jpeg|png)$)", image_url):
			return image_url
	return None


def find_image_url(html):
	bsObj = BeautifulSoup(html, "lxml")
	img_list = bsObj.select("img")
	# image_url_list = []
	for img in img_list:
		# data_original = img["data-original"]
		print img.attrs
		img_src = ""
		lazyload_url = get_lazy_load_url(img)
		if lazyload_url == None:
			lazyload_url = img.get("data-original") or img.get("data-src")
		if img.get("src") != None and img.get("src") != "":
			img_src = img['src']
		if lazyload_url != None:
			img_src = lazyload_url

		print img_src
		if "" == img_src:
			continue
		if img_src.startswith("data:"):
			continue
		if img_src.startswith("//"):
			img_src = protocol + ":" + img_src
		if img_src.startswith("/"):
			img_src = website + img_src
		if not img_src.startswith("http"):
			global path
			img_src = website + path[:path.rindex('/') + 1] + img_src
		# image_url_list.append(img_src)
		data_url = image_url_to_data_url(img_src)
		img["src"] = data_url
	# exit(0)
	return str(bsObj)

def find_css_link(html):
	bsObj = BeautifulSoup(html, "lxml")
	css_list = bsObj.select("link")
	css_url_list = []
	for css in css_list:
		# print css['rel']
		# print str(css)
		if css["rel"].count("stylesheet") > 0:
			# print css['href']
			css_url_list.append(css)
	return css_url_list

def style2dict(style):
	d = {}
	for line in style.split(";"):
		key_value = line.split(":")
		if len(key_value) == 2:
			d[key_value[0]] = key_value[1]
	return d

def dict2style(d):
	style = ""
	for key in d:
		style += (key + ":" + d[key] + ";")
	return style

if __name__ == '__main__':
	if len(sys.argv) < 2:
		exit(0)
	article_url = sys.argv[1]
	print get_host(article_url)

	html = get_data(article_url)
	title = page_title(html)

	html = find_image_url(html)
	# image_url_list = find_image_url(html)
	# for image_url in image_url_list:
	# 	data_url = image_url_to_data_url(image_url)
	# 	# print data_url
	# 	html = html.replace(image_url, data_url)

	# css_link_list = find_css_link(html)
	# for css_link in css_link_list:
	# 	print "+" * 80
	# 	css_url = css_link['href']
	# 	_css_url = css_url

	# 	if css_url.startswith("//"):
	# 		css_url = protocol + ":" + css_url
	# 	if css_url.startswith("/"):
	# 		css_url = website + css_url
	# 	print css_url
	# 	css_text = external_css_to_internal_css(css_url)
	# 	# print css_text
	# 	# html = html.replace(str(css_link), style_format % ({"css_text": css_text}))

	# 	print str(css_link)
	# 	pattern = re.compile(r'<link.*href=[\'\"]' + _css_url.replace("?", "\\?") + r'[\'\"].*>')
	# 	print pattern.pattern
	# 	print pattern.findall(html)
	# 	style_text = style_format % ({"css_text": css_text})
	# 	style_text = style_text.replace("\\", "\\\\")
	# 	html = re.sub(pattern, style_text, html)
	# 	print "=" * 80
	fhandle = open(title + ".html", "w")
	fhandle.write(html)
	fhandle.close()
