#!/usr/bin/env python

# PBKDF2 & AES related stuff

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

import os
import binascii
import hmac, hashlib
import sys
import cfg
import json
import random

check_hmac = False

def create_cfg(path_cfg):
    salt_len = 8 # 64 bit
    iv_len = 16 # 128 bit
    aes_bs = 32 # 256 bit == key length
    pbkdf2_iterations = 1000

    salt = ''
    for i in range(0, salt_len):
        salt += chr(random.randint(0, 255))

    iv = ''
    for i in range(0, iv_len):
        iv += chr(random.randint(0, 255))

    conf = { 'pbkdf2_salt': salt.encode('base64').replace("\n", ""),
             'pbkdf2_iterations': pbkdf2_iterations,
             'pkbdf2_salt_len': salt_len,
             'aes_iv': iv.encode('base64').replace("\n", ""),
             'aes_bs': aes_bs,
             'aes_iv_len': iv_len }

    with open(path_cfg, "w") as f:
        f.write(json.dumps(conf, indent=4))

def read_cfg(path_cfg):
    with open(path_cfg, "r") as f:
        return json.loads(f.read())

def add_padding(conf, s):
    """ Because cipher should be aligned to some text length, we need to
        add padding """
    return s + (conf['aes_bs'] - len(s) % conf['aes_bs']) * chr(conf['aes_bs'] - len(s) % conf['aes_bs'])

def strip_padding(s):
    """ Reverse of add_padding """
    return s[0:-ord(s[-1])]

def enc(conf, secret, plaintext):
    """ Encode plaintext using given secret (PBKDF2) """
    plaintext = add_padding(conf, plaintext)
    cipher = AES.new(secret, AES.MODE_CBC, conf['aes_iv'].decode('base64'), segment_size=128)
    return cipher.encrypt(plaintext).encode('base64')

def dec(conf, secret, ciphertext):
    """ Encode plaintext using given secret (PBKDF2) """
    cipher = AES.new(secret, AES.MODE_CBC, conf['aes_iv'].decode('base64'), segment_size=128)
    return strip_padding(cipher.decrypt(ciphertext.decode('base64')))

def derive_key(conf, password):
    """ Derive PBKDF2 key from passphrase """
    return PBKDF2(password, conf['pbkdf2_salt'].decode('base64'), conf['pbkdf2_iterations']).read(conf['aes_bs'])

def auth(secret, plaintext):
    """ Check integrity of plaintext via HMAC-MD5 """
    return hmac.new(key=secret, msg=plaintext, digestmod=hashlib.md5).hexdigest()

def enc_plaintext(conf, password, plaintext, aes_path, hmac_path):
    key = derive_key(conf, password)

    out_hmac = open(hmac_path, "wb")
    out_hmac.write(auth(key, plaintext.encode('utf-8')))

    out_aes = open(aes_path, "wb")
    out_aes.write(enc(conf, key, plaintext.encode('utf-8')))

def enc_db(conf, password, path, aes_path, hmac_path):
    """ Used to encrypt temporary created file (cbedit) """
    print "Encode %s into %s and %s" % (path, aes_path, hmac_path)

    plaintext = open(path, "rb").read().decode('utf-8').rstrip()
    enc_plaintext(conf, password, plaintext, aes_path, hmac_path)

def dec_db(conf, password, aes_path, hmac_path):
    print "Decode %s and %s" % (aes_path, hmac_path)

    cipher = open(aes_path, "rb").read().rstrip()
    key = derive_key(conf, password)

    plaintext = dec(conf, key, cipher)

    orig_hmac = open(hmac_path, "rb").readline()
    hmac = auth(key, plaintext)

    if check_hmac:
        if (hmac != orig_hmac):
            print 'Incorrect password!'
            sys.exit(0)

    return plaintext.decode('utf-8')
