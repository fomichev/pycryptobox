import platform
import os
import datetime
import subprocess
import json
import tarfile
import argparse

import lang.en as lang
#import lang.ru as lang

version = '0.1'
try:
    cs = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    version += '-' + cs
except:
    pass

# Don't switch it! Your data will be exposed in private/tmp/
debug = False

lock_timeout_minutes = 5

prefix = "private/"
path_db = prefix + "cryptobox"
path_db_hmac = prefix + "cryptobox.hmac"
path_db_html = prefix + "html/cryptobox.html"
path_db_mobile_html = prefix + "html/m.cryptobox.html"
path_db_include = prefix + "include"
path_tmp = prefix + "tmp"
path_cfg = prefix + "cryptobox.cfg"

path_backup = prefix + "cryptobox.tar"
backup_files = [ path_db, path_db_hmac, path_db_html, path_cfg ]

path_private = os.getcwd() + "/" + prefix
path_include = os.getcwd() + "/include"
path_html = os.getcwd() + "/html"

path_clippy = path_html + "/extern/clippy/build/clippy.swf"

html = lang.text
html['jquery_ui_theme'] = 'flick'
html['path_bookmarklets'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/"
html['version'] = version
html['date'] = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")

if platform.system() == 'Windows':
    editor = "gvim"
#    editor = "c:/Program Files/Sublime Text 2/sublime_text.exe"
#    editor = "c:/Program Files/Notepad++/notepad++.exe"
else:
    editor = "vim"

def backup():
    if len(backup_files) > 0:
        tar = tarfile.open(path_backup, "w")
        for name in backup_files:
            try:
                tar.add(name)
            except:
                print "WARNING: couldn't add %s file to backup!" % name
        tar.close()
