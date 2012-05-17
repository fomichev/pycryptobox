#!/usr/bin/env python

# generate JavaScript files containing cipher setup and cipher text

from Crypto.Cipher import AES

import cfg

def html(index):
    res = ""
    res += open(index, "r").read()
    return res

def config(cipher):
    res = ""

    for v in cfg.js.keys():
        if type(cfg.js[v]) == type(int()):
            if v == '_cfg_aesMode':
                if cfg.js[v] == AES.MODE_CFB:
                    res += "_cfg_aesMode = new Crypto.mode.CFB;"
                else:
                    raise Exception("Unknown AES mode")
            else:
                res += "%s = %s;" % (v, cfg.js[v])
        elif type(cfg.js[v] == type(str())):
            if v == '_cfg_pages':
                res += "%s = %s;" % (v, cfg.js[v])
            else:
                res += "%s = '%s';" % (v, cfg.js[v])
        else:
            raise Exception("Unknown type of JavaScript variable")

    res += "_cfg_cipher = \"%s\";" % (cipher)
    return res
