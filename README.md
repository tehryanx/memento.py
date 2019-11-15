# memento.py

Get endpoints from archived versions of robots.txt

usage: memento.py [-h] [-w] [-s START] target

Find endpoints in archived versions of robots.txt and sitemap.xml

positional arguments:
  target                A target domain

optional arguments:
  -h, --help            show this help message and exit
  -w, --wordlistmode    Output in wordlist mode - No domains, omit entries
                        with wildcards
  -s START, --start START
                        A date to start at in the format YYYY or YYYYMM
