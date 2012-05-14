import platform
from Crypto.Cipher import AES

pbkdf2_salt = "somesalt" # 64-bit
pbkdf2_iterations = 1000
aes_mode = AES.MODE_CFB
#aes_iv = "0123456890123456" # 128-bit

path_db = "private/cryptobox"
path_db_hmac = "private/cryptobox.hmac"
path_db_html = "private/cryptobox.html"
path_tmp = "tmp"
path_include = "include"
path_template = "template"

if platform.system() == 'Windows':
    editor = "gvim"
else:
    editor = "vim"
