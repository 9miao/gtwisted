#coding:utf8
'''
Created on 2014年2月21日

@author:  lan (www.9miao.com)
'''
from __future__ import division, absolute_import
from gtwisted.core import error

def installReactor(reactor):
    """装载reactor
    @param reactor: Rector 对象
    """
    import gtwisted.core
    import sys
    if 'twisted.internet.reactor' in sys.modules:
        raise error.ReactorAlreadyInstalledError("reactor already installed")
    gtwisted.core.reactor = reactor
    sys.modules['gtwisted.core.reactor'] = reactor