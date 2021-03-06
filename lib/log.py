"""
Custom small logging system
"""

import config

def d(s):
    """
    Debug printout (intended only for development!)
    """
    if config.debug:
        print s

def v(s):
    """
    Verbose printout
    """
    if config.verbose:
        print s

def w(s):
    """
    Warning printout
    """
    print "WARNING! " + s

def e(s):
    """
    Error printout
    """
    print "ERROR! " + s

def p(s):
    """
    Wrapper around print (to be consistent with other routines in this module
    """
    print s

def yn(s):
    """
    Get YES or NO answer from user
    """
    ans = ''

    while not ans in ['Y', 'y', 'N', 'n']:
        ans = raw_input(s + " [y|n]: ")

    return ans
