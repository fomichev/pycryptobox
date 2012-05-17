#!/usr/bin/env python

# PBKDF2 & AES related stuff

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

import os
import binascii
import hmac, hashlib
import sys
import cfg

check_hmac = False
aes_mode = AES.MODE_CBC

def add_padding(s):
    """ Because cipher should be aligned to some text length, we need to
        add padding """
    return s + (cfg.aes_bs - len(s) % cfg.aes_bs) * chr(cfg.aes_bs - len(s) % cfg.aes_bs)

def strip_padding(s):
    """ Reverse of add_padding """
    return s[0:-ord(s[-1])]

def enc(secret, plaintext):
    """ Encode plaintext using given secret (PBKDF2) """
    plaintext = add_padding(plaintext)
    cipher = AES.new(secret, aes_mode, cfg.aes_iv.decode('base64'), segment_size=128)
    return cipher.encrypt(plaintext).encode('base64')

def dec(secret, ciphertext):
    """ Encode plaintext using given secret (PBKDF2) """
    cipher = AES.new(secret, aes_mode, cfg.aes_iv.decode('base64'), segment_size=128)
    return strip_padding(cipher.decrypt(ciphertext.decode('base64')))

def derive_key(password):
    """ Derive PBKDF2 key from passphrase """
    return PBKDF2(password, cfg.pbkdf2_salt.decode('base64'), cfg.pbkdf2_iterations).read(cfg.aes_bs) # 256-bit key

def auth(secret, plaintext):
    """ Check integrity of plaintext via HMAC-MD5 """
    return hmac.new(key=secret, msg=plaintext, digestmod=hashlib.md5).hexdigest()

def enc_plaintext(password, plaintext, aes_path, hmac_path):
    key = derive_key(password)

    out_hmac = open(hmac_path, "wb")
    out_hmac.write(auth(key, plaintext.encode('utf-8')))

    out_aes = open(aes_path, "wb")
    out_aes.write(enc(key, plaintext.encode('utf-8')))

def enc_db(password, path, aes_path, hmac_path):
    """ Used to encrypt temporary created file (cbedit) """
    print "Encode %s into %s and %s" % (path, aes_path, hmac_path)

    plaintext = open(path, "rb").read().decode('utf-8').rstrip()
    enc_plaintext(password, plaintext, aes_path, hmac_path)

def dec_db(password, aes_path, hmac_path):
    print "Decode %s and %s" % (aes_path, hmac_path)

    cipher = open(aes_path, "rb").read().rstrip()
    key = derive_key(password)

    plaintext = dec(key, cipher)

    orig_hmac = open(hmac_path, "rb").readline()
    hmac = auth(key, plaintext)

    if check_hmac:
        if (hmac != orig_hmac):
            print 'Incorrect password!'
            sys.exit(0)

    return plaintext.decode('utf-8')
