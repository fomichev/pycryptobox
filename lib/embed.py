#!/usr/bin/env pyhon

# embed js and css into index.html

from bs4 import BeautifulSoup, Tag
import os
import re

def embed(index, output):
    soup = BeautifulSoup(open(index).read())

    stylesheets = ""
    for s in soup.find_all("link", rel="stylesheet"):
        stylesheets += open(s['href']).read()
        s.replace_with("")

    tag = soup.new_tag("style", media="screen", type="text/css");
    tag.string = stylesheets

    soup.head.insert(1, tag)

    scripts = ""
    for s in soup.find_all("script", type="text/javascript"):
        try:
            scripts += open(s['src']).read()
        except:
            scripts += s.string

        s.replace_with("")

    # remove comments
    scripts = re.compile(r'\s//.*$', re.MULTILINE).sub('', scripts)

    tag = soup.new_tag("script", type="text/javascript");
    tag.string = scripts

    soup.head.insert(2, tag)

    result = soup.prettify(formatter=None)
    open(output, "w").write(result)
