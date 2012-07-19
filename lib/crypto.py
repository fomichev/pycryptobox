# PBKDF2, AES & HMAC related stuff

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

import os
import binascii
import hmac, hashlib
import sys
import json
import random
import ConfigParser

import log

check_hmac = True

def create_db_conf(p, format_version):
    pbkdf2_salt_len = 8 # 64 bit
    pbkdf2_iterations = 1000
    aes_iv_len = 16 # 128 bit
    aes_bs = 32 # 256 bit == key length

    pbkdf2_salt = ''
    for i in range(0, pbkdf2_salt_len):
        pbkdf2_salt += chr(random.randint(0, 255))

    aes_iv = ''
    for i in range(0, aes_iv_len):
        aes_iv += chr(random.randint(0, 255))

    c = ConfigParser.ConfigParser()

    c.add_section("cryptobox");
    c.set('cryptobox', 'format_version', format_version)

    c.add_section("pbkdf2");
    c.set('pbkdf2', 'salt', pbkdf2_salt.encode('base64').replace("\n", ""))
    c.set('pbkdf2', 'salt_len', pbkdf2_salt_len)
    c.set('pbkdf2', 'iterations', pbkdf2_iterations)

    c.add_section("aes");
    c.set('aes', 'iv', aes_iv.encode('base64').replace("\n", ""))
    c.set('aes', 'iv_len', aes_iv_len)
    c.set('aes', 'bs', aes_bs)

    with open(p, 'wb') as f:
        c.write(f)

def read_db_conf(p, format_version):
    c = ConfigParser.ConfigParser()
    c.read(p)

    if c.getint('cryptobox', 'format_version') != format_version:
        log.e("Incompatible database format!")
        sys.exis(1)

    pbkdf2_conf = {}
    pbkdf2_conf['salt'] = c.get('pbkdf2', 'salt')
    pbkdf2_conf['salt_len'] = c.getint('pbkdf2', 'salt_len')
    pbkdf2_conf['iterations'] = c.getint('pbkdf2', 'iterations')

    aes_conf = {}
    aes_conf['iv'] = c.get('aes', 'iv')
    aes_conf['iv_len'] = c.getint('aes', 'iv_len')
    aes_conf['bs'] = c.getint('aes', 'bs')

    return { 'pbkdf2': pbkdf2_conf, 'aes': aes_conf }

def add_padding(db_conf, s):
    """ Because cipher should be aligned to some text length, we need to
        add padding """
    return s + (db_conf['aes']['bs'] - len(s) % db_conf['aes']['bs']) * chr(db_conf['aes']['bs'] - len(s) % db_conf['aes']['bs'])

def strip_padding(s):
    """ Reverse of add_padding """
    return s[0:-ord(s[-1])]

def enc(db_conf, secret, plaintext):
    """ Encode plaintext using given secret (PBKDF2) """
    plaintext = add_padding(db_conf, plaintext)
    cipher = AES.new(secret, AES.MODE_CBC, db_conf['aes']['iv'].decode('base64'), segment_size=128)
    return cipher.encrypt(plaintext).encode('base64')

def dec(db_conf, secret, ciphertext):
    """ Encode plaintext using given secret (PBKDF2) """
    cipher = AES.new(secret, AES.MODE_CBC, db_conf['aes']['iv'].decode('base64'), segment_size=128)
    return strip_padding(cipher.decrypt(ciphertext.decode('base64')))

def derive_key(db_conf, password):
    """ Derive PBKDF2 key from passphrase """
    return PBKDF2(password, db_conf['pbkdf2']['salt'].decode('base64'), db_conf['pbkdf2']['iterations']).read(db_conf['aes']['bs'])

def auth(secret, plaintext):
    """ Check integrity of plaintext via HMAC-MD5 """
    return hmac.new(key=secret, msg=plaintext, digestmod=hashlib.md5).hexdigest()

def enc_plaintext(db_conf, password, plaintext, aes_path, hmac_path):
    key = derive_key(db_conf, password)

    out_hmac = open(hmac_path, "wb")
    out_hmac.write(auth(key, plaintext.encode('utf-8')))

    out_aes = open(aes_path, "wb")
    out_aes.write(enc(db_conf, key, plaintext.encode('utf-8')))

def enc_db(db_conf, password, path, aes_path, hmac_path):
    """ Used to encrypt temporary created file (cbedit) """
    log.v("Encode %s into %s and %s" % (path, aes_path, hmac_path))

    plaintext = open(path, "rb").read().decode('utf-8').rstrip()
    enc_plaintext(db_conf, password, plaintext, aes_path, hmac_path)

def dec_db(db_conf, password, aes_path, hmac_path):
    log.v("Decode %s and %s" % (aes_path, hmac_path))

    cipher = open(aes_path, "rb").read().rstrip()
    key = derive_key(db_conf, password)

    plaintext = dec(db_conf, key, cipher)

    orig_hmac = open(hmac_path, "rb").readline()
    hmac = auth(key, plaintext)

    if check_hmac:
        if (hmac != orig_hmac):
            log.e('Incorrect password!')
            sys.exit(1)

    try:
        return plaintext.decode('utf-8')
    except:
        log.e('Incorrect password!')
        sys.exit(1)
