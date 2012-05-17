import platform
import os
import datetime
import subprocess
import json

import argparse

from Crypto.Cipher import AES

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

pbkdf2_salt = "somesalt".encode('hex') # 64-bit
pbkdf2_iterations = 1000
aes_mode = AES.MODE_CFB
aes_iv = "0123456890123456".encode('hex') # 128-bit

lock_timeout_minutes = 5

prefix = ""
path_db = prefix + "private/cryptobox"
path_db_hmac = prefix + "private/cryptobox.hmac"
path_db_html = prefix + "private/html/cryptobox.html"
path_db_mobile_html = prefix + "private/html/m.cryptobox.html"
path_db_include = prefix + "private/include"
path_tmp = prefix + "private/tmp"

backup = [ path_db, path_db_hmac, path_db_html ]
backup_file = prefix + "private/cryptobox.tar"

path_include = os.getcwd() + "/include"
path_html = os.getcwd() + "/html"

path_clippy = path_html + "/extern/clippy/build/clippy.swf"

html = lang.text
html['jquery_ui_theme'] = 'flick'
html['path_bookmarklets'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/"
html['version'] = version
html['date'] = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")

js = {}
js['_cfg_salt'] = pbkdf2_salt
js['_cfg_lockTimeout'] = lock_timeout_minutes
js['_cfg_pbkdb2Iterations'] = pbkdf2_iterations
js['_cfg_aesMode'] = aes_mode
js['_cfg_pages'] = json.dumps(lang.types)
js['_cfg_aesIv'] = aes_iv

if platform.system() == 'Windows':
    editor = "gvim"
#    editor = "c:/Program Files/Sublime Text 2/sublime_text.exe"
#    editor = "c:/Program Files/Notepad++/notepad++.exe"
else:
    editor = "vim"
