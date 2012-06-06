#!/usr/bin/env python

# Concatenate all pieces into one HTML page

import sys
import os
import shutil
import json

import crypto
import flatten
import generate
import embed

import cfg
import log

def update(conf, password):
    path_tmp_index = os.path.abspath(cfg.path['tmp'] + "/index.html")
    path_tmp_mobile_index = os.path.abspath(cfg.path['tmp'] + "/m.index.html")

    path_index = os.path.abspath(cfg.path['db_html'])
    path_mobile_index = os.path.abspath(cfg.path['db_mobile_html'])

    try:
        os.mkdir(cfg.path['tmp'] + "/")
    except:
        pass

    key = crypto.derive_key(conf, password)
    db_plaintext = crypto.dec_db(conf, password, cfg.path['db'], cfg.path['db_hmac'])

    json_plaintext = flatten.flatten(db_plaintext.split("\n"), (cfg.path['include'] + "/", cfg.path['db_include'] + "/"))
    if cfg.debug:
        open(cfg.path['tmp'] + "/_json_plaintext", "w").write(json_plaintext)

    aes_base64 = crypto.enc(conf, key, json_plaintext)
    if cfg.debug:
        open(cfg.path['tmp'] + "/_aes_base64", "w").write(aes_base64)

    aes_base64_nonl = "".join(aes_base64.split("\n"))
    if cfg.debug:
        open(cfg.path['tmp'] + "/_aes_base64_nonl", "w").write(aes_base64_nonl)

    index_html = generate.html(cfg.path['html'] + "/index.html")
    open(path_tmp_index, "w").write(index_html)

    m_index_html = generate.html(cfg.path['html'] + "/m.index.html")
    open(path_tmp_mobile_index, "w").write(m_index_html)

    js = conf
    js['lock_timeout_minutes'] = cfg.lock_timeout_minutes
    js['page'] = cfg.lang.types
    js['cipher'] = aes_base64_nonl

    cfg_js = generate.config(js)
    if cfg.debug:
        open(cfg.path['tmp'] + "/cfg.js", "w").write(cfg_js)

    saved_cwd = os.getcwd()
    os.chdir(cfg.path['html'])

    try:
        os.mkdir(os.path.dirname(path_index))
    except:
        pass

    log.v("> cryptobox.html")
    embed.embed(path_tmp_index, path_index, cfg_js)
    log.v("Copy clippy.swf")
    shutil.copyfile(cfg.path['clippy'], os.path.dirname(path_index) + "/clippy.swf")

    log.v("> m.cryptobox.html")
    embed.embed(path_tmp_mobile_index, path_mobile_index, cfg_js)

    if cfg.debug == False:
        os.chdir(saved_cwd)
        shutil.rmtree(cfg.path['tmp'])
