#coding:utf8
'''
Created on 2014年2月21日

@author:  lan (www.9miao.com)
'''
# from twisted.core.greactor import GeventReactor
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory,Protocol

reactor = reactor

class MyProtocol(Protocol):
    
    def connectionMade(self):
        pass
#         print "connectionMade:",self.transport.sessionno
        
    def dataReceived(self, data):
#         print "dataReceived:",data
        self.transport.write('HTTP/1.1 200 OK\n\nHello World!!')
        self.transport.loseConnection()
        
    def connectionLost(self, reason):
        pass
#         print "connectionLost",reason
        
class MyServerFactory(ServerFactory):
    protocol = MyProtocol
    
from gtwisted.utils import log

ss = MyServerFactory()
import sys
log.startLogging(sys.stdout)
reactor.listenTCP(80, ss)
reactor.callLater(5, log.msg,"asdfasdf")
reactor.run()