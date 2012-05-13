import sys
import os
import shutil

import crypto
import flatten
import cfg
import generate
import embed

debug = False

def update(password):
    try:
        os.mkdir(cfg.path_tmp + "/")
    except:
        pass

    key = crypto.derive_key(password)
    db_plaintext = crypto.dec_db(password, cfg.path_db, cfg.path_db_hmac)

    json_plaintext = flatten.flatten(db_plaintext.split("\n"), cfg.path_include + "/")
    if debug:
        open(cfg.path_tmp + "/_json_plaintext", "w").write(json_plaintext)

    aes_base64 = crypto.enc(key, json_plaintext).encode("base64")
    if debug:
        open(cfg.path_tmp + "/_aes_base64", "w").write(aes_base64)

    aes_base64_nonl = "".join(aes_base64.split("\n"))
    if debug:
        open(cfg.path_tmp + "/_aes_base64_nonl", "w").write(aes_base64_nonl)

    index_html = generate.html(cfg.path_template + "/index.html")
    open(cfg.path_tmp + "/index.html", "w").write(index_html)

    cfg_js = generate.config(aes_base64_nonl)
    open(cfg.path_tmp + "/cfg.js", "w").write(cfg_js)

    os.chdir(cfg.path_tmp)
    embed.embed("index.html", "../" + cfg.path_db_html)

    if debug == False:
        os.chdir("..")
        shutil.rmtree(cfg.path_tmp)