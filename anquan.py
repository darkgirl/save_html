#!/usr/bin/env python
# coding=utf-8

from bs4 import BeautifulSoup
import requests

def get_article_links(url):
	article_links = []
	html = requests.get(url)
	soup = BeautifulSoup(html, "lxml")
	nodes = soup.select("td > a")
	for node in nodes:
		print(node)

def main():
	url_format = "http://www.anquan.us/search?keywords=&&content_search_by=by_drops&&search_by_html=False&&page=%d"
	index = 1
	while index <= 54:
		get_article_links(url % index)
		exit(0)
		pass

if __name__ == '__main__':
	main()
