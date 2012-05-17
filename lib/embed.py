#!/usr/bin/env pyhon
# -*- coding: utf-8 -*-

# embed js and css into index.html

from bs4 import BeautifulSoup, Tag
import os
import re
import cfg

def getimg(path):
    data = "".join(open(path, "rb").read().encode('base64').split("\n"))
    return "data:image/png;base64," + data

def sethtmlvars(data):
    for key in cfg.html.keys():
        data = data.replace("<?" + key + "?>", cfg.html[key].decode('utf-8'))

    return data

def embed(index, output, cfg_js):
    data = open(index).read().decode('utf-8')
    data = sethtmlvars(data)

    soup = BeautifulSoup(data)

    print "Embed stylesheets"
    stylesheets = ""
    for s in soup.find_all("link", rel="stylesheet"):
        contents = open(s['href']).read()

        print "Embed images in " + s['href']
        urls_re = re.compile(r'url\(([^)]*)\)*')
        urls = [url.group(1) for url in urls_re.finditer(contents)]

        for url in urls:
            contents = contents.replace(url, getimg(os.path.dirname(s['href']) + "/" + url))

        stylesheets += contents
        s.replace_with("")

    tag = soup.new_tag("style", media="screen", type="text/css");
    tag.string = stylesheets

    soup.head.insert(1, tag)

    print "Embed scripts"
    scripts = ""
    for s in soup.find_all("script", type="text/javascript"):
        try:
            print "Embed " + s['src']
            scripts += open(s['src']).read().decode('utf-8')
        except:
            try:
                scripts += s.string
            except:
                print "! Script or tag seem to be empty"

        s.replace_with("")

    print "Remove comments from scripts"
    scripts = re.compile(r'\s//.*$', re.MULTILINE).sub('', scripts)
    scripts = sethtmlvars(scripts)

    tag = soup.new_tag("script", type="text/javascript")
    tag.string = scripts + cfg_js

    soup.head.insert(2, tag)

    result = soup.prettify(formatter=None)

    open(output, "w").write(result.encode('utf-8'))
