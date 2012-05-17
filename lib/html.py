#!/usr/bin/env python

# Concatenate all pieces into one HTML page

import sys
import os
import shutil

import crypto
import flatten
import cfg
import generate
import embed

def update(password):
    path_tmp_index = os.path.abspath(cfg.path_tmp + "/index.html")
    path_tmp_mobile_index = os.path.abspath(cfg.path_tmp + "/m.index.html")

    path_index = os.path.abspath(cfg.path_db_html)
    path_mobile_index = os.path.abspath(cfg.path_db_mobile_html)

    try:
        os.mkdir(cfg.path_tmp + "/")
    except:
        pass

    key = crypto.derive_key(password)
    db_plaintext = crypto.dec_db(password, cfg.path_db, cfg.path_db_hmac)

    json_plaintext = flatten.flatten(db_plaintext.split("\n"), (cfg.path_include + "/", cfg.path_db_include + "/"))
    if cfg.debug:
        open(cfg.path_tmp + "/_json_plaintext", "w").write(json_plaintext)

    aes_base64 = crypto.enc(key, json_plaintext).encode("base64")
    if cfg.debug:
        open(cfg.path_tmp + "/_aes_base64", "w").write(aes_base64)

    aes_base64_nonl = "".join(aes_base64.split("\n"))
    if cfg.debug:
        open(cfg.path_tmp + "/_aes_base64_nonl", "w").write(aes_base64_nonl)

    index_html = generate.html(cfg.path_html + "/index.html")
    open(path_tmp_index, "w").write(index_html)

    m_index_html = generate.html(cfg.path_html + "/m.index.html")
    open(path_tmp_mobile_index, "w").write(m_index_html)


    cfg_js = generate.config(aes_base64_nonl)
    if cfg.debug:
        open(cfg.path_tmp + "/cfg.js", "w").write(cfg_js)

    saved_cwd = os.getcwd()
    os.chdir(cfg.path_html)

    print "> cryptobox.html"
    embed.embed(path_tmp_index, path_index, cfg_js)
    print "Copy clippy.swf"
    shutil.copyfile(cfg.path_clippy, os.path.dirname(path_index) + "/clippy.swf")

    print "> m.cryptobox.html"
    embed.embed(path_tmp_mobile_index, path_mobile_index, cfg_js)

    if cfg.debug == False:
        os.chdir(saved_cwd)
        shutil.rmtree(cfg.path_tmp)
