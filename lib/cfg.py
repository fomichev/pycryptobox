import platform
import os
from Crypto.Cipher import AES

pbkdf2_salt = "somesalt" # 64-bit
pbkdf2_iterations = 1000
aes_mode = AES.MODE_CFB
#aes_iv = "0123456890123456" # 128-bit

prefix = ""
path_db = prefix + "private/cryptobox"
path_db_hmac = prefix + "private/cryptobox.hmac"
path_db_html = prefix + "private/cryptobox.html"
path_db_mobile_html = prefix + "private/m.cryptobox.html"
path_tmp = prefix + "private/tmp"

path_include = os.getcwd() + "/include"
path_template = os.getcwd() + "/template"

if platform.system() == 'Windows':
    editor = "gvim"
else:
    editor = "vim"
