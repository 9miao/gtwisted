#coding:utf8
'''
Created on 2014年2月22日

@author:  lan (www.9miao.com)
'''
from gtwisted.core import reactor
from gtwisted.core.rpc import PBClientProtocl,PBClientFactory
from gtwisted.utils import log
import sys


class MyPBClientProtocl(PBClientProtocl):
    
    def remote_getResult(self,a,b):
        
        return a+b
    
    def remote_printok(self):
        print "Hello World!"
        
class MyPBClientFactory(PBClientFactory):
    
    protocol = MyPBClientProtocl
    
client = MyPBClientFactory()

def printok():
    print "ok"
    reactor.callLater(1, printok)
    
def callRemote():
    dd = client.getRootObject()
    result = dd.callRemoteForResult('getResult1',8,9)
    print result
    
def callRemote2():
    dd = client.getRootObject()
    result = dd.callRemoteForResult('getResult',8,9)
    print 'result',result

reactor.connectTCP('localhost', 1000, client)
# reactor.callLater(3, callRemote)
reactor.callLater(5, callRemote2)
# reactor.callLater(1, printok)
log.startLogging(sys.stdout)
reactor.run()


