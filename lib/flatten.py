#!/usr/bin/env python

# merge username and password information from private database with
# appropriate JSON template

import json
import cgi

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


def flatten_node(prefix, tp, v, tag):
    print "Read " + prefix + tp

    data = open(prefix + tp, "r").read().decode('utf-8')
    data = cgi.escape(data)

    jdata = json.loads(data)
    set_vars(jdata, v)
    if not 'vars' in  jdata:
        jdata['vars'] = v

    if len(tag) == 0:
        jdata['tag'] = '__default__'
    else:
        jdata['tag'] = tag

    return jdata

def here_doc(val):
    try:
        if val[0] == '<' and val[1] == '<':
            return val[2:]
    except:
        return ""

    return ""

def flatten(lines, prefix):
    logins = []
    logins.append({ "type" : "magic", "value": "270389" })
    lines.reverse()

    tp = None
    tag = ''
    v = {}
    while lines:
        line = lines.pop().strip()

        if len(line) == 0:
            continue

        if line[0] == '#':
            continue

        if line[len(line) - 1] == ':':
            if tp:
                logins.append(flatten_node(prefix, tp, v, tag))
                v = {}

            tp = line[:-1]
            try:
                tag = tp.split('@')[1].strip()
                tp = tp.split('@')[0].strip()
            except:
                tag = ''

            continue

        keyval = line.split('=')
        if len(keyval) == 2:
            keyval[0] = keyval[0].strip()
            keyval[1] = keyval[1].strip()

            hdoc = here_doc(keyval[1])
            if hdoc != "":
                value = ""

                while lines:
                    hline = lines.pop()
                    if hline.strip() == hdoc:
                        break
                    value += hline + "\n"

                v[keyval[0]] = value
            else:
                v[keyval[0]] = keyval[1]

    if tp:
        logins.append(flatten_node(prefix, tp, v, tag))
        tp = None

    padding = "                " # somehow JS decrypt eats fist 16 symbols
    return padding + json.dumps(logins, sort_keys=True, indent=4)
