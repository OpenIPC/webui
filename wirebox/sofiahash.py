#!/usr/bin/python

import hashlib

def sofia_hash(msg):
    h = ""
    m = hashlib.md5()
    m.update(msg)
    msg_md5 = m.digest()
    for i in range(8):
        n = (ord(msg_md5[2 * i]) + ord(msg_md5[2 * i + 1])) % 0x3e
    if n > 9:
        if n > 35:
            n += 61
        else:
            n += 55
    else:
        n += 0x30
    h += chr(n)
    return h
