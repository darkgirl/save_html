#!/usr/bin/env python
# coding=utf-8

import  traceback
from bs4 import BeautifulSoup
import requests

import save_pdf

def get_article_links(url):
	article_links = []
	html = requests.get(url).text
	soup = BeautifulSoup(html, "lxml")
	nodes = soup.select("td > a[href^=\"static\"]")
	for node in nodes:
		link = node["href"]
		print(link)
		article_links.append("http://www.anquan.us/" + link)
	return article_links

def main():
	url_format = "http://www.anquan.us/search?keywords=&&content_search_by=by_drops&&search_by_html=False&&page=%d"
	index = 4
	while index <= 54:
		url = url_format % index
		try:
			article_links = get_article_links(url)
			fd = open("log/anquan.txt", "a")
			fd.write("[%d]\n" % index)
			fd.write("\n".join(article_links))
			fd.close()
			for article_link in article_links:
				try:
					save_pdf.save_pdf(article_link, ["article"], directory="./anquan/")
					# exit(0)
					pass
				except Exception as e:
					# raise e

					fhandle = open("log/anquan_err.log", "a")
					fhandle.write("[start]\n")
					fhandle.write(article_link + "\n")
					fhandle.write(traceback.format_exc())
					fhandle.write("[end]\n")
					fhandle.close()
					# exit(0)
					pass
			pass
		except Exception as e:
			# raise e


			fhandle = open("log/anquan.log", "a")
			fhandle.write("[start]\n")
			fhandle.write(url + "\n")
			fhandle.write(traceback.format_exc())
			fhandle.write("[end]\n")
			fhandle.close()
			pass
		index += 1

if __name__ == '__main__':
	main()
