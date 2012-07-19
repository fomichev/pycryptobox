# merge username and password information from private database with
# appropriate JSON template

import json
import cgi
import re
import io
import ConfigParser

import cfg
import log
from preprocessor import pp

def __handle_node(search_paths, tp, v):
    for path in search_paths:
        try:
#            data = open(path + tp, "r").read().decode('utf-8')
            data = pp(path + tp, v)
        except:
            log.v("Tried " + path + tp)
            continue

        log.v("Read " + path + tp)

        try:
            jdata = json.loads(data)
        except Exception as e:
            raise Exception("Invalid JSON data in '" + path + tp + "':\n" + str(e))

        jdata['type'] = tp.split('/')[0]

        if jdata['type'] == 'login':
            jdata['vars'] = v

        if len(v['tag']) == 0:
            jdata['tag'] = '__default__'
        else:
            jdata['tag'] = v['tag']

        return jdata

    if tp.split('/')[0] == 'login':
        log.w("Not found entry type '%s'" % tp)
        jdata = {}
        jdata['vars'] = v
        jdata['tag'] = '__default__'
        jdata['type'] = 'login'
        jdata['name'] = '/'.join(tp.split('/')[1:])
        jdata['address'] = 'http://' + jdata['name']
        jdata['form'] = {}

        return jdata
    else:
        raise Exception("Not found entry type '%s'" % tp)

def db2json(db_lines, search_paths, filter_tp=None):
    j = []
    j.append({ "type" : "magic", "value": "270389" })

    db = ConfigParser.ConfigParser()
    db.readfp(io.StringIO("\n".join(db_lines)))

    for section in db.sections():
        tp = section.split()[0]
        if filter_tp:
            if tp.split('/')[0] != filter_tp:
                continue

        name = " ".join(section.split()[1:])

        v = dict(db.items(section))
        v['name'] = name

        if not 'tag' in v:
            v['tag'] = '__default__'

        if 'hidden' in v and v['hidden'] == 'yes':
            continue

        j.append(__handle_node(search_paths, tp, v))

    if cfg.debug:
        return json.dumps(j, indent=4)
    else:
        return json.dumps(j)
