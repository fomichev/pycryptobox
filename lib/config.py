"""
This module is responsible for handling config
"""

import ConfigParser
import datetime
import os
import platform
import sys

import log

version = '0.4'
format_version = 2

debug = False # Be aware that your data will be exposed in private/tmp/
verbose = False

# add git hash to the version if available
try:
    cs = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    version += '-' + cs
except:
    pass

def config_value(d, c, variable, default='', t=str):
    section, name = variable.split('.')

    try:
        value = c.get(section, name)
    except:
        value = default

    if t == str:
        d[variable] = value
    else:
        d[variable] = int(value)

def read_user_config(c):
    def read_lang(l):
        _lang = __import__('lang.' + l, globals(), locals(), [], -1)
        lang = getattr(_lang, l)

        return lang.defines

    if platform.system() == 'Windows':
        #default_editor = "notepad.exe"
        default_editor = "gvim"
    else:
        default_editor = "vim"

    d = dict()

    config_value(d, c, 'ui.jquery_ui_theme', 'flick')
    config_value(d, c, 'ui.default_password_length', '16')
    config_value(d, c, 'ui.lock_timeout_minutes', '5')
    config_value(d, c, 'ui.editor', default_editor)
    config_value(d, c, 'ui.lang', 'en')

    config_value(d, c, 'cryptobox.version', version)
    config_value(d, c, 'cryptobox.date_format', "%H:%M %d.%m.%Y")
    config_value(d, c, 'cryptobox.date', datetime.datetime.now().strftime(d['cryptobox.date_format']))

    # TODO: ABSPATH
    config_value(d, c, 'path.root', os.getcwd())
    config_value(d, c, 'path.db', os.getcwd() + "/private")

    config_value(d, c, 'path.db_cipher', d['path.db'] + '/cryptobox')
    config_value(d, c, 'path.db_conf', d['path.db_cipher'] + '.conf')
    config_value(d, c, 'path.db_json', os.path.abspath(d['path.db_cipher'] + '.json'))
    config_value(d, c, 'path.db_hmac', d['path.db_cipher'] + '.hmac') ############################################### TEMP
    config_value(d, c, 'path.db_html', d['path.db'] + '/html/cryptobox.html')
    config_value(d, c, 'path.db_mobile_html', d['path.db'] + '/html/m.cryptobox.html')
    config_value(d, c, 'path.db_chrome', d['path.db'] + '/chrome')
    config_value(d, c, 'path.db_chrome_cfg', d['path.db'] + '/chrome/cfg.js')
    config_value(d, c, 'path.db_include', d['path.db'] + '/include')
    config_value(d, c, 'path.tmp', d['path.db'] + '/tmp')
    config_value(d, c, 'path.include', d['path.root'] + '/include')
    config_value(d, c, 'path.html', d['path.root'] + '/html')
    config_value(d, c, 'path.bookmarklet', d['path.root'] + '/bookmarklet')
    config_value(d, c, 'path.chrome', d['path.root'] + '/chrome')
    config_value(d, c, 'path.clippy', d['path.html'] + '/extern/clippy/build/clippy.swf')
    config_value(d, c, 'path.jquery_ui_css_images', os.path.abspath(d['path.html'] + '/extern/jquery-ui/css/' + d['ui.jquery_ui_theme']))
    config_value(d, c, 'path.jquery_mobile_css_images', os.path.abspath(d['path.html'] + '/extern/jquery-mobile/'))

    config_value(d, c, 'path.db_bookmarklet_form', d['path.db'] + '/bookmarklet/form.js')
    config_value(d, c, 'path.db_bookmarklet_fill', d['path.db'] + '/bookmarklet/fill.js')

    config_value(d, c, 'backup.path', d['path.db'] + '/cryptobox.tar')
    config_value(d, c, 'backup.files', [
        d['path.db_cipher'],
        d['path.db_hmac'],
        d['path.db_html'],
        d['path.db_conf'],
        d['path.db_json'],
        d['path.db_html'],
        d['path.clippy'] ])

    return dict(d.items() + read_lang(d['ui.lang']).items())

#def read_db_config(c):
#    d = dict()
#
#    config_value(d, c, 'pbkdf2.salt_len')
#    config_value(d, c, 'pbkdf2.salt')
#    config_value(d, c, 'pbkdf2.iterations')
#
#    config_value(d, c, 'aes.iv_len')
#    config_value(d, c, 'aes.iv')
#    config_value(d, c, 'aes.bs')
#
#    config_value(d, c, 'cryptobox.format_version')
#    config_value(d, c, 'cryptobox.hmac')
#
#    return d
#
#def save_db_config(path, d):
#    pass

def read(args):
    """
    Read configuration (possibly pointed by args)
    """

    if debug:
        log.w("DEBUGGING ENABLED! YOUR DATA MAY BE EXPOSED!")

    v = vars(args)

    global verbose
    if 'verbose' in v:
        verbose = v['verbose']

    user_config_parser = ConfigParser.ConfigParser()
    try:
        if 'config' in v and v['config'] != None:
            f = open(v['config'])
            user_config_parser.readfp(f)
        else:
            try:
                f = open('.cryptoboxrc')
                user_config_parser.readfp(f)
            except:
                try:
                    f = open('~/.cryptoboxrc')
                    user_config_parser.readfp(f)
                except:
                    pass
    except Exception as e:
        log.e("Could not load user config!")
        log.e(str(e))
        sys.exit(1)

    return read_user_config(user_config_parser)
