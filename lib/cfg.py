import platform
import os
import datetime
import subprocess
import json
import tarfile
import argparse
import sys

import lang.en as lang
#import lang.ru as lang

version = '0.2'
try:
    cs = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    version += '-' + cs
except:
    pass

debug = False # Don't switch it! Your data will be exposed in private/tmp/
verbose = 0
lock_timeout_minutes = 5
prefix = "private/"

path = {}
path['db'] = prefix + "cryptobox"
path['db_hmac'] = prefix + "cryptobox.hmac"
path['db_html'] = prefix + "html/cryptobox.html"
path['db_mobile_html'] = prefix + "html/m.cryptobox.html"
path['db_include'] = prefix + "include"
path['tmp'] = prefix + "tmp"
path['cfg'] = prefix + "cryptobox.cfg"
path['backup'] = prefix + "cryptobox.tar"
path['private'] = os.getcwd() + "/" + prefix
path['include'] = os.getcwd() + "/include"
path['html'] = os.getcwd() + "/html"
path['clippy'] = path['html'] + "/extern/clippy/build/clippy.swf"

html = lang.text
html['jquery_ui_theme'] = 'flick'
html['path_bookmarklets'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/"
html['version'] = version
html['date'] = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")

backup_files = [ path['db'], path['db_hmac'], path['db_html'], path['cfg'] ]

if platform.system() == 'Windows':
    editor = "gvim"
#    editor = "c:/Program Files/Sublime Text 2/sublime_text.exe"
#    editor = "c:/Program Files/Notepad++/notepad++.exe"
else:
    editor = "vim"

def init(args):
    global verbose

    v = vars(args)

    if 'verbose' in v:
        verbose = v['verbose']

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
