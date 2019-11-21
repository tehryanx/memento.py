#!/usr/bin/env python3

import re
import argparse
import json
import requests
import sys

parser = argparse.ArgumentParser(description='Find endpoints in archived versions of robots.txt')
#group = parser.add_mutually_exclusive_group()
parser.add_argument("target", help="A target domain")
parser.add_argument("-w", "--wordlistmode", help="Output in wordlist mode - No domains, omit entries with wildcards", action="store_true")
parser.add_argument("-s", "--start", help="A date to start at in the format YYYY or YYYYMM", default=2010)
args = parser.parse_args()

target_url = args.target if "//" not in args.target else args.target.split('//')[1]
target_url = target_url if target_url[-1] != '/' else target_url[0:-1]

endpoint = "http://web.archive.org/cdx/search/cdx?url="+target_url+"/robots.txt&collapse=digest&collapse=timestamp:6&output=json&filter=statuscode:200&from=" + str(args.start)

response = requests.get(endpoint)
parsed_response = json.loads(response.text)[1:-1]

mementos = []

for item in parsed_response:
	mementos.append("https://web.archive.org/web/" + item[1] + "/" + item[2])

sys.stderr.write("Found " + str(len(mementos)) + " mementos for " + target_url + "\n")

endpoints = []
for memento in mementos:
	contents = requests.get(memento).text
	endpoints += re.findall( r'[^agent][Aa]llow.?:.?(.*?)\n', contents)

endpoints = list(dict.fromkeys(endpoints))
for item in endpoints:

	if len(item) > 0 and item[0] != "/":
		item = "/" + item
	if args.wordlistmode:
		if "*" not in item:
			print(item)
	else:
		print("https://" + target_url + item)
