#!/usr/bin/env python

# generate JavaScript files containing cipher setup and cipher text

import cfg

def html(index):
    res = ""
    res += open(index, "r").read()
    return res

def config(data):
    res = ""
    res += "_cfg_salt = \"%s\";" % (cfg.pbkdf2_salt)
    res += "_cfg_cipher = \"%s\";" % (data)
    return res
