#coding:utf8
'''
Created on 2014年2月22日

@author:  lan (www.9miao.com)
'''
import sys
from gtwisted.core import reactor
from gtwisted.core.rpc import PBServerProtocl,PBServerFactory
from gtwisted.utils import log


class MyPBServerProtocl(PBServerProtocl):
    
    def remote_getResult(self,a,b):
        print a,b
        dd = self.getRootObject()
        ss = dd.callRemoteForResult('getResult',9,9)
        print 'clinet result',ss
        print "11111111111"
        return a+b
        
class MyPBServerFactory(PBServerFactory):
    
    protocol = MyPBServerProtocl
    
reactor.listenTCP(1000, MyPBServerFactory())
log.startLogging(sys.stdout)
reactor.run()
