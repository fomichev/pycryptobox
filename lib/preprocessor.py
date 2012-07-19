# Custom c-style preprocessor

import os
from cStringIO import StringIO
import re

from extern.Preprocessor import Preprocessor

def pp(filename, defines = {}, remove_lf=True, fatal=False):
    p = Preprocessor()
    p.context.update(defines)
    p.setLineEndings('lf')
    p.setMarker('#')
    p.out = StringIO()
    p.do_filter('substitution')
    if fatal:
        p.do_filter('substitution')
    else:
        p.do_filter('attemptSubstitution')

    if type(filename) == list:
        for f in filename:
            p.do_include(f)
    else:
        p.do_include(filename)

    if remove_lf:
        return os.linesep.join([s for s in p.out.getvalue().splitlines() if s])
    else:
        return p.out.getvalue()
