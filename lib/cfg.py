import platform
import os
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
html['jquery_ui_theme'] = 'pepper-grinder'
#html['jquery_ui_theme'] = 'flick'
html['path_bookmarklets'] = "https://raw.github.com/fomichev/cryptobox/master/bookmarklet/"

if platform.system() == 'Windows':
    editor = "gvim"
else:
    editor = "vim"
