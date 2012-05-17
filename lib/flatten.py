#!/usr/bin/env python

# merge username and password information from private database with
# appropriate JSON template

import json
import cgi
import re

import cfg

re_subst = re.compile(r'\$\{([^\}]*)\?([^}]*)\}')

def clear_unset(obj):
    if type(obj) == type(dict()):
        for k in obj.keys():
            if type(obj[k]) == type(dict()):
                clear_unset(obj[k])
            elif type(obj[k]) == type(list()):
                clear_unset(obj[k])
            else:
                r = re_subst.search(obj[k])
                while r:
                    obj[k] = obj[k].replace(r.group(0), "")
                    r = re_subst.search(obj[k])

    elif type(obj) == type(list()):
        for i in obj:
            clear_unset(i, v);

def set_vars(obj, v):
    if type(obj) == type(dict()):
        for k in obj.keys():
            if type(obj[k]) == type(dict()):
                set_vars(obj[k], v)
            elif type(obj[k]) == type(list()):
                set_vars(obj[k], v)
            else:
                for vk in v.keys():
                    r = re_subst.search(obj[k])
                    if r and r.group(1) == vk:
                        obj[k] = obj[k].replace(r.group(0), r.group(2))

                    obj[k] = obj[k].replace("$" + vk, v[vk])
    elif type(obj) == type(list()):
        for i in obj:
            set_vars(i, v);

def flatten_node(search_paths, tp, v, tag):
    for path in search_paths:
        try:
            data = open(path + tp, "r").read().decode('utf-8')
        except:
            if cfg.debug:
                print "Tried " + path + tp
            continue

        print "Read " + path + tp
#        data = cgi.escape(data)
        try:
            jdata = json.loads(data)
        except Exception as e:
            raise Exception("Invalid JSON data in '" + path + tp + "':\n" + str(e))

        jdata['type'] = tp.split('/')[0]

        set_vars(jdata, v)
        clear_unset(jdata)
        if jdata['type'] == 'login':
            jdata['vars'] = v

        if len(tag) == 0:
            jdata['tag'] = '__default__'
        else:
            jdata['tag'] = tag

        return jdata

    raise Exception("Not found entry type '%s'" % tp)

def here_doc(val):
    try:
        if val[0] == '<' and val[1] == '<':
            return val[2:]
    except:
        return ""

    return ""

def flatten(lines, search_paths):
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
                logins.append(flatten_node(search_paths, tp, v, tag))
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
            keyval[1] = "=".join(keyval[1:]).strip()

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
        logins.append(flatten_node(search_paths, tp, v, tag))
        tp = None

    padding = "                " # somehow JS decrypt eats fist 16 symbols

    if cfg.debug:
        return padding + json.dumps(logins, indent=4)
    else:
        return padding + json.dumps(logins)
