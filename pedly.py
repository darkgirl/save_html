#!/usr/bin/env python
#coding=utf-8

import  traceback
from bs4 import BeautifulSoup
import save_html
import save_pdf

url_format = "https://bbs.pediy.com/search-原创-1-%d.htm"
referer = "https://bbs.pediy.com/"

def get_article_link(html):
	article_link_list = []
	soup = BeautifulSoup(html, "lxml")
	subject_list = soup.select(".subject")
	for subject in subject_list:
		a_list = subject.select("a")
		if a_list[2].contents[0] != "工具下载".decode("utf-8"):
			link = referer + a_list[0]["href"]
			print link
			article_link_list.append(link)
	return article_link_list

def main():
	index = 49
	while index < 1219:
		url = url_format % (index)
		try:
			html = save_html.get_data(url)
			article_link_list = get_article_link(html)
			fhandle = open("pediy.txt", "a")
			fhandle.write("[%5d]\n" % index);
			fhandle.write("\n".join(article_link_list))
			fhandle.write("\n")
			fhandle.close()

			for article_link in article_link_list:
				try:
					save_pdf.exclude_tags_default.append(".avatar_info")
					save_pdf.save_pdf(article_link, ["div .card"], directory="./pedly/")
				except Exception as e:
					traceback.print_exc()
					# raise e
					print  article_link


					fhandle = open("pediy_err.log", "a")
					fhandle.write("[start]\n")
					fhandle.write(article_link + "\n")
					fhandle.write(traceback.format_exc())
					fhandle.write("[end]\n")
					fhandle.close()
			index += 1
			pass
		except Exception as e:
			print e.message
			print  index

			traceback.print_exc()

			fhandle = open("pediy.log", "a")
			fhandle.write("[start]\n")
			fhandle.write(url + "\n")
			fhandle.write(traceback.format_exc())
			fhandle.write("[end]\n")
			fhandle.close()
			pass

if __name__ == '__main__':
	main()