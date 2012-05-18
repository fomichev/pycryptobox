#!/usr/bin/env python

# generate JavaScript files containing cipher setup and cipher text

import json
from Crypto.Cipher import AES

import cfg

def html(index):
    return open(index, "r").read()

def config(js):
    return 'cfg = ' + json.dumps(js) + ';'
