# embed js and css into index.html

import os
import re

import cfg
import log
from preprocessor import pp

def embed_css_images(text, images_root):
    def getimg(path):
        data = "".join(open(path, "rb").read().encode('base64').split("\n"))
        return "data:image/png;base64," + data

    urls_re = re.compile(r'url\(([^)]*)\)*')
    urls = [url.group(1) for url in urls_re.finditer(text)]

    for url in urls:
        text = text.replace(url, getimg(images_root + "/" + url))

    return text

def embed(index, output, cfg_js, images_root):
#    data = open(index).read().decode('utf-8')
    data = pp(index, cfg.defines, fatal=True)
    data = embed_css_images(data, images_root)

    open(output, "w").write(data)
