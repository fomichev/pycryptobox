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


def flatten_node(prefix, tp, v):
    print "Read " + prefix + tp

    data = open(prefix + tp, "r").read()
    data = cgi.escape(data)

    jdata = json.loads(data)
    set_vars(jdata, v)
    jdata['vars'] = v

    return jdata

def flatten(lines, prefix):
    logins = []
    tp = None
    v = {}
    for line in lines:
        line = line.strip()

        if len(line) <= 1:
            continue

        if line[0] == '#':
            continue

        if line[0] == '@':
            # handle groups?!
            continue

        if line[len(line) - 1] == ':':
            if tp:
                logins.append(flatten_node(prefix, tp, v))
                v = {}

            tp = line[:-1]

        keyval = line.split('=')
        if len(keyval) == 2:
            v[keyval[0]] = keyval[1]

    if tp:
        logins.append(flatten_node(prefix, tp, v))

    padding = "                " # somehow JS decrypt eats fist 16 symbols
    return padding + json.dumps(logins, sort_keys=True, indent=4)
