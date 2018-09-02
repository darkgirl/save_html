#!/usr/bin/env python
# coding=utf-8


from optparse import OptionParser
import sys
import save_pdf

def main():
	usage = "usage: %prog <url> [options] args"
	parser = OptionParser(usage)
	parser.add_option("-i", "--include_tags", dest="include_tags",
		help="which tags need to be retained")
	parser.add_option("-e", "--enclude_tags", dest="exclude_tags",
		help="which tags need to be removed")
	parser.add_option("-d", "--dictionary", dest="dictionary",
		help="where to save")
	parser.add_option("-r", "--render", dest="render", action="store_true",
		help="whether the page needs to be rendered")
	(values, args) = parser.parse_args(sys.argv[1:])
	if len(args) != 1:
		parser.print_help()
		exit(0)
	print values
	print args
	url = args[0]
	options = eval(str(values))
	if None != options.get("include_tags"):
		save_pdf.config["include_tags"].extend(options["include_tags"].split(","))
	if None != options.get("exclude_tags"):
		save_pdf.config["exclude_tags"].extend(options["exclude_tags"].split(","))
	if None != options.get("dictionary"):
		save_pdf.config["dictionary"] = options["dictionary"]
	if None != options.get("render"):
		save_pdf.config["render"] = options["render"]
	print save_pdf.config
	save_pdf.save_pdf_config(url, save_pdf.config)

if __name__ == "__main__":
    main()