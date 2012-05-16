import platform
import os
import datetime
import subprocess

from Crypto.Cipher import AES

# Don't switch it! Your data will be exposed in private/tmp/
debug = False

pbkdf2_salt = "somesalt" # 64-bit
pbkdf2_iterations = 1000
aes_mode = AES.MODE_CFB
#aes_iv = "0123456890123456" # 128-bit

lock_timeout_minutes = 5

prefix = ""
path_db = prefix + "private/cryptobox"
path_db_hmac = prefix + "private/cryptobox.hmac"
path_db_html = prefix + "private/html/cryptobox.html"
path_db_mobile_html = prefix + "private/html/m.cryptobox.html"
path_db_include = prefix + "private/include"
path_tmp = prefix + "private/tmp"

path_include = os.getcwd() + "/include"
path_html = os.getcwd() + "/html"

path_clippy = path_html + "/extern/clippy/build/clippy.swf"

html = {}
html['jquery_ui_theme'] = 'flick'
html['path_bookmarklets'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/"
html['version'] = '0.1'
html['date'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

try:
    cs = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    html['version'] += '.' + cs
except:
    pass

if platform.system() == 'Windows':
    editor = "gvim"
#    editor = "c:/Program Files/Sublime Text 2/sublime_text.exe"
#    editor = "c:/Program Files/Notepad++/notepad++.exe"
else:
    editor = "vim"
