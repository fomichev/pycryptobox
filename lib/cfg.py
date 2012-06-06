import platform
import os
import datetime
import subprocess
import json
import tarfile
import argparse
import sys
import ConfigParser

import lang.en as lang
#import lang.ru as lang

import log

version = '0.2'
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
html = lang.text
backup_files = []

def init(args):
    global verbose
    global user
    global path
    global backup_files

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
        print e
        log.e("Could not load user config!")
        sys.exit(1)

    path['db_cipher'] = user['path']['db'] + "/cryptobox"

    path['db_hmac'] = path['db_cipher'] + ".hmac"
    path['db_conf'] = path['db_cipher'] + ".conf"
    path['db_html'] = user['path']['db'] + "/html/cryptobox.html"
    path['db_mobile_html'] = user['path']['db'] + "/html/m.cryptobox.html"
    path['db_include'] = user['path']['db'] + "/include"

    path['tmp'] = user['path']['db'] + "/tmp"
    path['backup'] = user['path']['db'] + "/cryptobox.tar"
    path['include'] = os.getcwd() + "/include"
    path['html'] = os.getcwd() + "/html"
    path['clippy'] = path['html'] + "/extern/clippy/build/clippy.swf"

    html['jquery_ui_theme'] = user['ui']['jquery_ui_theme']
    html['path_bookmarklets'] = user['ui']['path_bookmarklets']
    html['version'] = version
    html['date'] = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")
    html['default_password_length'] = str(user['security']['default_password_length'])

    backup_files = [ path['db_cipher'], path['db_hmac'], path['db_html'], path['db_conf'] ]

    return v

def backup():
    if len(backup_files) > 0:
        tar = tarfile.open(path['backup'], "w")
        for name in backup_files:
            try:
                tar.add(name)
            except:
                log.w("Couldn't add %s file to backup!" % name)

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

    get_option(c, cp, 'ui', 'jquery_ui_theme')
    get_option(c, cp, 'ui', 'path_bookmarklets')
    get_option(c, cp, 'ui', 'editor')

    get_option(c, cp, 'security', 'lock_timeout_minutes')
    get_option(c, cp, 'security', 'default_password_length')

    return c

def default_user_conf():
    c = { 'ui': {}, 'path': {}, 'security': {} }

    c['path']['db'] = os.getcwd() + "/private/"

    c['ui']['jquery_ui_theme'] = 'flick'
    c['ui']['path_bookmarklets'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/"
    if platform.system() == 'Windows':
        # editor = "c:/Program Files/Sublime Text 2/sublime_text.exe"
        # editor = "c:/Program Files/Notepad++/notepad++.exe"
        c['ui']['editor'] = "gvim"
    else:
        c['ui']['editor'] = "vim"

    c['security']['lock_timeout_minutes'] = 5
    c['security']['default_password_length'] = 16

    return c
