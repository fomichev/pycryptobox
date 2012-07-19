import platform
import os
import datetime
import subprocess
import json
import tarfile
import argparse
import sys
import ConfigParser

import log

version = '0.3'
format_version = 2

try:
    cs = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    version += '-' + cs
except:
    pass

debug = False # Be aware that your data will be exposed in private/tmp/
verbose = 0

user= {}
path = {}
html = {}
defines = {}
lang = None
backup_files = []

def from_user_config(dest, user, section, name, default):
    if section in user and user[section] != None:
        if name in user[section] and user[section][name] != None:
            dest[name] = user[section][name]
            return

    dest[name] = default

def init(args):
    global verbose
    global user
    global path
    global lang
    global html
    global defines
    global backup_files

    if debug:
        log.w("DEBUGGING ENABLED! YOUR DATA MAY BE EXPOSED!")

    v = vars(args)

    if 'verbose' in v:
        verbose = v['verbose']

    try:
        if 'config' in v and v['config'] != None:
            user = read_user_conf(v['config'])
        else:
            try:
                user = read_user_conf('.cryptoboxrc')
            except:
                try:
                    user = read_user_conf('~/.cryptoboxrc')
                except:
                    user = default_user_conf()
    except Exception as e:
        log.e("Could not load user config!")
        sys.exit(1)

    path['root'] = os.getcwd()

    path['db_cipher'] = os.path.abspath(user['path']['db'] + "/cryptobox")

    path['db_hmac'] = path['db_cipher'] + ".hmac"
    path['db_conf'] = path['db_cipher'] + ".conf"
    path['db_json'] = path['db_cipher'] + ".json"
    path['db_html'] = os.path.abspath(user['path']['db'] + "/html/cryptobox.html")
    path['db_mobile_html'] = user['path']['db'] + "/html/m.cryptobox.html"
    path['db_chrome'] = user['path']['db'] + "/chrome"
    path['db_chrome_cfg'] = user['path']['db'] + "/chrome/cfg.js"

    from_user_config(path, user, 'path', 'db_bookmarklet_fill', user['path']['db'] + "/bookmarklet/fill.js")
    from_user_config(path, user, 'path', 'db_bookmarklet_form', user['path']['db'] + "/bookmarklet/form.js")

    path['db_include'] = os.path.abspath(user['path']['db'] + "/include") + '/'

    path['tmp'] = user['path']['db'] + "/tmp"
    path['backup'] = user['path']['db'] + "/cryptobox.tar"
    path['include'] = path['root'] + "/include"
    path['html'] = path['root'] + "/html"
    path['bookmarklet'] = path['root'] + "/bookmarklet"
    path['chrome'] = path['root'] + "/html/chrome"
    path['clippy'] = path['html'] + "/extern/clippy/build/clippy.swf"

    _lang = __import__('lang.' + user['ui']['lang'], globals(), locals(), [], -1)
    lang = getattr(_lang, user['ui']['lang'])

    html = lang.text
    html['jquery_ui_theme'] = user['ui']['jquery_ui_theme']
    html['path_form_bookmarklet'] = user['ui']['path_form_bookmarklet']
    html['path_fill_bookmarklet'] = user['ui']['path_fill_bookmarklet']
    html['version'] = version
    html['date'] = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")
    html['default_password_length'] = str(user['security']['default_password_length'])

    path['jquery_ui_css_images'] = os.path.abspath(path['html'] + '/extern/jquery-ui/css/' + html['jquery_ui_theme'])
    path['jquery_mobile_css_images'] = os.path.abspath(path['html'] + '/extern/jquery-mobile/')

    defines.update(path)
    defines.update(html)

    backup_files = [ path['db_cipher'], path['db_hmac'], path['db_html'], path['db_conf'], path['db_json'], path['db_html'], path['clippy'] ]

    return v

def backup():
    if len(backup_files) <= 0:
        return

    saved_cwd = os.getcwd()
    tar = tarfile.open(path['backup'], "w")
    for p in backup_files:
        abspath = os.path.abspath(p)

        try:
            os.chdir(os.path.dirname(abspath))
            tar.add(os.path.basename(abspath))
        except:
            log.w("Couldn't add %s file to backup!" % abspath)

    os.chdir(saved_cwd)

    tar.close()

def get_option(c, cp, sect, opt, integer=False):
    if cp.has_option(sect, opt):
        if integer:
            c[sect][opt] = cp.getint(sect, opt)
        else:
            c[sect][opt] = cp.get(sect, opt)

def read_user_conf(p):
    f = open(p)

    cp = ConfigParser.ConfigParser()
    cp.readfp(f)

    c = default_user_conf()
    get_option(c, cp, 'path', 'db')
    get_option(c, cp, 'path', 'db_bookmarklet_fill')
    get_option(c, cp, 'path', 'db_bookmarklet_form')

    get_option(c, cp, 'ui', 'jquery_ui_theme')
    get_option(c, cp, 'ui', 'editor')
    get_option(c, cp, 'ui', 'lang')

    get_option(c, cp, 'security', 'lock_timeout_minutes')
    get_option(c, cp, 'security', 'default_password_length')

    return c

def default_user_conf():
    c = { 'ui': {}, 'path': {}, 'security': {} }

    c['path']['db'] = os.getcwd() + "/private/"

    c['ui']['lang'] = 'en'
    c['ui']['jquery_ui_theme'] = 'flick'
    c['ui']['path_form_bookmarklet'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/form.js"
    c['ui']['path_fill_bookmarklet'] = "#"
    if platform.system() == 'Windows':
        # c['ui']['editor'] = "c:/Program Files/Sublime Text 2/sublime_text.exe"
        # c['ui']['editor'] = "c:/Program Files/Notepad++/notepad++.exe"
        c['ui']['editor'] = "gvim"
    else:
        c['ui']['editor'] = "vim"

    c['security']['lock_timeout_minutes'] = 5
    c['security']['default_password_length'] = 16

    return c
