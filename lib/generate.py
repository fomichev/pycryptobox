"""
Generate HTML, bookmarklets, extensions, etc
"""

import sys
import os
import shutil
import json
import ConfigParser
import io
import re
import tarfile

import crypto
from preprocessor import pp

import config
import log

def db2json(db_lines, search_paths, filter_tp=None):
    """
    Merge username and password information from private database with
    appropriate JSON template
    """
    def __handle_node(search_paths, tp, v):
        for path in search_paths:
            f = path + '/' + tp
            try:
                data = pp(f, v)
            except:
                log.v("Tried " + f)
                continue

            log.v("Read " + f)

            try:
                jdata = json.loads(data)
            except Exception as e:
                raise Exception("Invalid JSON data in '" + f + "':\n" + str(e))

            jdata['type'] = tp.split('/')[0]

            if jdata['type'] == 'login':
                jdata['vars'] = v

            if len(v['tag']) == 0:
                jdata['tag'] = '__default__'
            else:
                jdata['tag'] = v['tag']

            return jdata

        if tp.split('/')[0] == 'login':
            log.w("Not found entry type '%s'" % tp)
            jdata = {}
            jdata['vars'] = v
            jdata['tag'] = '__default__'
            jdata['type'] = 'login'
            jdata['name'] = '/'.join(tp.split('/')[1:])
            jdata['address'] = 'http://' + jdata['name']
            jdata['form'] = {}

            return jdata
        else:
            raise Exception("Not found entry type '%s'" % tp)

    j = []
    j.append({ "type" : "magic", "value": "270389" })

    db = ConfigParser.ConfigParser()
    db.readfp(io.StringIO("\n".join(db_lines)))

    for section in db.sections():
        tp = section.split()[0]
        if filter_tp:
            if tp.split('/')[0] != filter_tp:
                continue

        name = " ".join(section.split()[1:])

        v = dict(db.items(section))
        v['name'] = name

        if not 'tag' in v:
            v['tag'] = '__default__'

        if 'hidden' in v and v['hidden'] == 'yes':
            continue

        for key in v.keys():
            v[key] = json.dumps(v[key])[1:-1]

        j.append(__handle_node(search_paths, tp, v))

    if config.debug:
        return json.dumps(j, indent=4)
    else:
        return json.dumps(j)

def embed_html(path, defines, css_images_root):
    """
    Preprocess HTML and embed CSS images
    """
    def __embed_css_images(text, css_images_root):
        def __getimg(path):
            data = "".join(open(path, "rb").read().encode('base64').split("\n"))
            return "data:image/png;base64," + data

        urls_re = re.compile(r'url\(([^)]*)\)*')
        urls = [url.group(1) for url in urls_re.finditer(text)]

        for url in urls:
            text = text.replace(url, __getimg(css_images_root + "/" + url))

        return text

    data = pp(path, defines, fatal=True)
    data = __embed_css_images(data, css_images_root)

    return data

def mkdir(paths):
    """
    Stupid mkdir wrapper to bypass exceptions
    """
    if type(paths) != list:
        paths = [ paths ]

    for p in paths:
        try:
            os.mkdir(p)
        except Exception as e:
            log.v("Couldn't create directory %s (%s)" % (p, e))

def encrypt_json(db_plaintext, key, db_conf, search_paths, tmp_path='', debug=False):
    """
    Create encrypted JSON database from plain text database
    """
    json_plaintext = db2json(db_plaintext.split("\n"), search_paths)
    aes_base64 = crypto.enc(db_conf, key, json_plaintext)
    aes_base64_nonl = "".join(aes_base64.split("\n"))

    if debug:
        open(tmp_path + "/1_json_plaintext", "w").write(json_plaintext)
        open(tmp_path + "/2_aes_base64", "w").write(aes_base64)

    return aes_base64_nonl

def generate_cryptobox_json(js, o):
    log.v("> cryptobox.json")
    open(o, "w").write(json.dumps(js))

def generate_html(i, o, defines):
    log.v("> cryptobox.html")
    mkdir(os.path.dirname(o))
    open(o, "w").write(embed_html(i, defines, defines['path.jquery_ui_css_images']))

    log.v(">> Copy clippy.swf")
    shutil.copyfile(defines['path.clippy'], os.path.dirname(o) + "/clippy.swf")

def generate_mhtml(i, o, defines):
    log.v("> m.cryptobox.html")
    mkdir(os.path.dirname(o))
    open(o, "w").write(embed_html(i, defines, defines['path.jquery_mobile_css_images']))

def generate_bookmarklet(i, o, defines):
    log.v("> bookmarklet/%s" % os.path.dirname(i))
    mkdir(os.path.dirname(o))
    open(o, "w").write(pp(i , defines))
    log.v(">> Save to " + o)

def generate_chrome_extension():
#    log.v("> chrome extension")
#    chrome_extension(db_plaintext, key, db_conf)
    pass

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
#    j = encrypted_json(js, db_plaintext, key, db_conf, tp="login")
#
#    path_chrome_cfg = os.path.abspath(defines['path.db_chrome_cfg'])
#    open(path_chrome_cfg, "w").write(j)
#
#    try:
#        os.mkdir(defines['path.db_chrome'])
#    except:
#        pass
#
#    for f in include:
#        shutil.copyfile(f, defines['path.db_chrome'] + '/' + os.path.basename(f))

def generate_all(db_conf, password, defines):
    """
    Generate all files (on database update)
    """
    mkdir(defines['path.tmp'])

    if config.debug:
        open(defines['path.tmp'] + "/0_defines", "w").write(str(defines))

    key = crypto.derive_key(db_conf, password)
    db_plaintext = crypto.dec_db(db_conf, password, defines['path.db_cipher'], defines['path.db_hmac'])

    js = db_conf.copy()
    js['lock_timeout_minutes'] = defines['ui.lock_timeout_minutes']
    js['page'] = dict()
    for k in defines.keys():
        if k[0:5] == 'page.':
            js['page'][k[5:]] = defines[k]
    js['cipher'] = encrypt_json(db_plaintext, key, db_conf,
                                (defines['path.include'], defines['path.db_include']),
                                tmp_path=defines['path.tmp'],
                                debug=config.debug)

    generate_cryptobox_json(js, defines['path.db_json'])
    generate_html(defines['path.html'] + "/desktop/index.html", defines['path.db_html'], defines)
    generate_mhtml(defines['path.html'] + "/mobile/index.html", defines['path.db_mobile_html'], defines)
    generate_bookmarklet(defines['path.bookmarklet'] + "/fill.js", defines['path.db_bookmarklet_fill'], defines)
    generate_bookmarklet(defines['path.bookmarklet'] + "/form.js", defines['path.db_bookmarklet_form'], defines)
    generate_chrome_extension()

    if config.debug == False:
        shutil.rmtree(defines['path.tmp'])

def backup(path, backup_files):
    if len(backup_files) <= 0:
        return

    saved_cwd = os.getcwd()
    tar = tarfile.open(path, "w")
    for p in backup_files:
        abspath = os.path.abspath(p)

        try:
            os.chdir(os.path.dirname(abspath))
            tar.add(os.path.basename(abspath))
        except:
            log.w("Couldn't add %s file to backup!" % abspath)

    os.chdir(saved_cwd)

    tar.close()
