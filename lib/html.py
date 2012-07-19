# Concatenate all pieces into one HTML page

import sys
import os
import shutil
import json

import crypto
from db2json import db2json
import embed
from preprocessor import pp

import cfg
import log

def encrypted_json(suffix, js, db_plaintext, key, db_conf, tp=None):
    json_plaintext = db2json(db_plaintext.split("\n"), (cfg.path['include'] + "/", cfg.path['db_include']), tp)
    if cfg.debug:
        open(cfg.path['tmp'] + "/1_json_plaintext_" + suffix, "w").write(json_plaintext)

    aes_base64 = crypto.enc(db_conf, key, json_plaintext)
    if cfg.debug:
        open(cfg.path['tmp'] + "/2_aes_base64_" + suffix, "w").write(aes_base64)

    aes_base64_nonl = "".join(aes_base64.split("\n"))
    if cfg.debug:
        open(cfg.path['tmp'] + "/3_aes_base64_nonl_" + suffix, "w").write(aes_base64_nonl)

    js['cipher'] = aes_base64_nonl

    cfg_js = 'cfg = ' + json.dumps(js) + ';'
    open(cfg.path['db_json'], "w").write(json.dumps(js))

    return cfg_js

def bookmarket_form(db_plaintext, key, db_conf):
    return pp('../bookmarklet/form.js', cfg.defines)

def bookmarket_fill(db_plaintext, key, db_conf):
    return pp('../bookmarklet/fill.js' , cfg.defines)

#def chrome_extension(db_plaintext, key, db_conf):
#    include = (
#            "../html/chrome/icon.png",
#            "../html/chrome/manifest.json",
#            "../html/chrome/popup.html",
#            "../html/chrome/popup.js",
#            "../html/chrome/content.js",
#            "../html/chrome/background.js",
#
#            "../html/js/crypto.js",
#            "../html/js/login.js",
#            "../html/js/lock.js",
#            "../html/js/fill.js",
#            "../html/extern/jquery/jquery-1.7.2.min.js",
#
#            "../html/extern/CryptoJS/components/core-min.js",
#            "../html/extern/CryptoJS/components/enc-base64-min.js",
#            "../html/extern/CryptoJS/components/cipher-core-min.js",
#            "../html/extern/CryptoJS/components/aes-min.js",
#            "../html/extern/CryptoJS/components/sha1-min.js",
#            "../html/extern/CryptoJS/components/hmac-min.js",
#            "../html/extern/CryptoJS/components/pbkdf2-min.js",
#            )
#
#    js = db_conf.copy()
#    j = encrypted_json("bookmarklet", js, db_plaintext, key, db_conf, tp="login")
#
#    path_chrome_cfg = os.path.abspath(cfg.path['db_chrome_cfg'])
#    open(path_chrome_cfg, "w").write(j)
#
#    try:
#        os.mkdir(cfg.path['db_chrome'])
#    except:
#        pass
#
#    for f in include:
#        shutil.copyfile(f, cfg.path['db_chrome'] + '/' + os.path.basename(f))

def generate_html(index):
    return open(index, "r").read()

def update(db_conf, password):
    path_tmp_index = os.path.abspath(cfg.path['tmp'] + "/index.html")
    path_tmp_mobile_index = os.path.abspath(cfg.path['tmp'] + "/m.index.html")

    path_index = os.path.abspath(cfg.path['db_html'])
    path_mobile_index = os.path.abspath(cfg.path['db_mobile_html'])
    path_bookmarklet_fill = os.path.abspath(cfg.path['db_bookmarklet_fill'])
    path_bookmarklet_form = os.path.abspath(cfg.path['db_bookmarklet_form'])

    try:
        os.mkdir(cfg.path['tmp'] + "/")
    except:
        pass

    key = crypto.derive_key(db_conf, password)
    db_plaintext = crypto.dec_db(db_conf, password, cfg.path['db_cipher'], cfg.path['db_hmac'])

    index_html = generate_html(cfg.path['html'] + "/desktop/index.html")
    open(path_tmp_index, "w").write(index_html)

    m_index_html = generate_html(cfg.path['html'] + "/mobile/index.html")
    open(path_tmp_mobile_index, "w").write(m_index_html)

    js = db_conf.copy()
    js['lock_timeout_minutes'] = cfg.user['security']['lock_timeout_minutes']
    js['page'] = cfg.lang.types

    cfg_js = encrypted_json("html", js, db_plaintext, key, db_conf)

    saved_cwd = os.getcwd()
    os.chdir(cfg.path['html'])

    try:
        os.mkdir(os.path.dirname(path_index))
    except:
        pass

    try:
        os.mkdir(os.path.dirname(path_mobile_index))
    except:
        pass

    try:
        os.mkdir(os.path.dirname(path_bookmarklet_fill))
    except:
        pass

    try:
        os.mkdir(os.path.dirname(path_bookmarklet_form))
    except:
        pass

    log.v("> cryptobox.html")
    embed.embed(path_tmp_index, path_index, cfg_js, cfg.path['jquery_ui_css_images'])
    log.v("Copy clippy.swf")
    shutil.copyfile(cfg.path['clippy'], os.path.dirname(path_index) + "/clippy.swf")

    log.v("> m.cryptobox.html")
    embed.embed(path_tmp_mobile_index, path_mobile_index, cfg_js, cfg.path['jquery_mobile_css_images'])

    log.v("> bookmarklet/fill.js")
    open(path_bookmarklet_fill, "w").write(bookmarket_fill(db_plaintext, key, db_conf))
    log.v("Save to " + path_bookmarklet_fill)

    log.v("> bookmarklet/form.js")


    open(path_bookmarklet_form, "w").write(bookmarket_form(db_plaintext, key, db_conf))
    log.v("Save to " + path_bookmarklet_form)

#    log.v("> chrome extension")
#    chrome_extension(db_plaintext, key, db_conf)

    if cfg.debug == False:
        os.chdir(saved_cwd)
        shutil.rmtree(cfg.path['tmp'])
