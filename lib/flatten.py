#!/usr/bin/env python

# merge username and password information from private database with
# appropriate JSON template

import json
import cgi
import re
import io
import ConfigParser

import cfg
import log

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

def flatten_node(search_paths, tp, v):
    for path in search_paths:
        try:
            data = open(path + tp, "r").read().decode('utf-8')
        except:
            log.d("Tried " + path + tp)
            continue

        log.v("Read " + path + tp)
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

        if len(v['tag']) == 0:
            jdata['tag'] = '__default__'
        else:
            jdata['tag'] = v['tag']

        return jdata

    raise Exception("Not found entry type '%s'" % tp)

def flatten(lines, search_paths):
    j = []
    j.append({ "type" : "magic", "value": "270389" })

    conf = ConfigParser.ConfigParser()
    conf.readfp(io.StringIO("\n".join(lines)))

    for section in conf.sections():
        tp = section.split()[0]
        name = " ".join(section.split()[1:])

        v = dict(conf.items(section))
        v['name'] = name
        v['username'] = name

        if not 'tag' in v:
            v['tag'] = '__default__'

        j.append(flatten_node(search_paths, tp, v))

    if cfg.debug:
        return json.dumps(j, indent=4)
    else:
        return json.dumps(j)
