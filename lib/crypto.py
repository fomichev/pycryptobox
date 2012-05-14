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

def add_padding(plaintext):
    padding = (16 - len(plaintext) % 16) * " "
    return plaintext + padding

def strip_padding(plaintext):
    return plaintext.rstrip()

def enc(secret, plaintext):
    plaintext = add_padding(plaintext)
    cipher = AES.new(secret, cfg.aes_mode, segment_size=128)
#    cipher = AES.new(secret, cfg.aes_mode, aes_iv, segment_size=128)
    return cipher.encrypt(plaintext)

def dec(secret, ciphertext):
    cipher = AES.new(secret, cfg.aes_mode, segment_size=128)
#    cipher = AES.new(secret, cfg.aes_mode, aes_iv, segment_size=128)
    return strip_padding(cipher.decrypt(ciphertext))

def derive_key(password):
    return PBKDF2(password, cfg.pbkdf2_salt, cfg.pbkdf2_iterations).read(32) # 256-bit key

def derive_keyhex(password):
    return PBKDF2(password, cfg.pbkdf2_salt).hexread(32) # 256-bit key

def auth(secret, plaintext):
    return hmac.new(key=secret, msg=plaintext, digestmod=hashlib.md5).hexdigest()

def enc_plaintext(password, plaintext, aes_path, hmac_path):
    key = derive_key(password)

    out_hmac = open(hmac_path, "wb")
    out_hmac.write(auth(key, plaintext.encode('utf-8')))

    out_aes = open(aes_path, "wb")
    out_aes.write(enc(key, plaintext.encode('utf-8')))

def enc_db(password, path, aes_path, hmac_path):
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
