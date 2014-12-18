#coding:utf8
'''
Created on 2014年5月29日

@author:  lan (www.9miao.com)
'''
import gevent
from gtwisted.core import asyncresultfactory


def AsynCaller(func,*args,**kw):
    _key,result = asyncresultfactory.AsyncResultFactory().createAsyncResult()
    def _function(_key,*args,**kw):
        aresult = asyncresultfactory.AsyncResultFactory().popAsyncResult(_key)
        aresult.set(func(*args,**kw))
    gevent.spawn(_function,_key,*args,**kw)
    return result.get()