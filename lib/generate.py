#!/usr/bin/env python

# generate JavaScript files containing cipher setup and cipher text

import cfg

def html(index):
    res = ""
    res += open(index, "r").read()
    return res

def config(cipher):
    res = ""
    res += "_cfg_salt = \"%s\";" % (cfg.pbkdf2_salt)
    res += "_cfg_cipher = \"%s\";" % (cipher)
    res += "_cfg_lockTimeout = %s;" % (cfg.lock_timeout_minutes)
    res += "_cfg_pathBookmarklets = \"%s\";" % (cfg.path_bookmarklets)
    return res
