#!/usr/bin/env python

# merge username and password information from private database with
# appropriate JSON template

import json
import cgi

def get_vars(s):
    v = {}

    first = True
    for var in s.split():
        keyval = var.split('=')

        if len(keyval) != 2:
            if first:
                first = False
                continue
            else:
                print "SOMETHING IS WRONG WITH DB"
                return {}

        v[keyval[0]] = keyval[1]

    return v

def set_vars(obj, v):
    if type(obj) == type(dict()):
        for k in obj.keys():
            if type(obj[k]) == type(dict()):
                set_vars(obj[k], v)
            elif type(obj[k]) == type(list()):
                set_vars(obj[k], v)
            else:
                for vk in v.keys():
                    obj[k] = obj[k].replace("${" + vk + "}", v[vk])
                    obj[k] = obj[k].replace("$" + vk, v[vk])

    elif type(obj) == type(list()):
        for i in obj:
            set_vars(i, v);

def flatten(lines, prefix):
    logins = []
    for line in lines:
        line = line.strip()

        if len(line) <= 1:
            continue

        if line[0] == '#':
            continue

        if line[0] == '@':
            # handle groups?!
            continue

        tp = line.split()[0]

        data = open(prefix + tp, "r").read()
        data = cgi.escape(data)

        jdata = json.loads(data)
        v = get_vars(line)
        set_vars(jdata, v)

        jdata['vars'] = v

        logins.append(jdata)

        padding = "                " # somehow JS decrypt eats fist 16 symbols

    return padding + json.dumps(logins, sort_keys=True, indent=4)
