from Crypto.Cipher import AES

pbkdf2_salt = "somesalt" # 64-bit
pbkdf2_iterations = 1000
aes_mode = AES.MODE_CFB

#aes_iv = "0123456890123456" # 128-bit

path_db = "private/db"
path_db_hmac = "private/db.hmac"

editor = "vim"
