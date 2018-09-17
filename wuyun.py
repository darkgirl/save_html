#!/usr/bin/env python
# coding=utf-8

import  traceback
from bs4 import BeautifulSoup
import requests

import save_pdf

url_referer = "https://wooyun.js.org/"

def get_article_links(url):
	article_links = []
	html = requests.get(url).text
	soup = BeautifulSoup(html, "lxml")
	nodes = soup.select(".link > a")
	for node in nodes:
		link = node["href"]
		print(link)
		article_links.append(url_referer + link.encode("utf-8"))
	return article_links

filename = "log/400.txt"
def main():
	try:
		# article_links = get_article_links(url_referer)
		fd = open(filename, "r")
		article_links = fd.read().split("\n")
		fd.close()
		for article_link in article_links:
			try:
				print article_link
				# print chardet.detect(article_link)
				save_pdf.save_pdf_by_url(article_link, ["body"], directory="./anquan/")
				# exit(0)
				article_links.remove(article_link)

				fd = open(filename, "w")
				fd.write("\n".join(article_links))
				fd.close()
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
		# print
		raise e
		pass

	fd = open(filename, "w")
	fd.write("\n".join(article_links))
	fd.close()


if __name__ == '__main__':
	main()
