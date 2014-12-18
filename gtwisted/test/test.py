#coding:utf8
'''
Created on 2014年2月21日

@author:  lan (www.9miao.com)
'''
from gtwisted.core.greactor import GeventReactor
from gtwisted.core.protocols import BaseProtocol,ServerFactory
import gtwisted

print gtwisted.get_version()
reactor = GeventReactor()

class MyProtocol(BaseProtocol):
    
    def connectionMade(self):
        pass
#         print "connectionMade:",self.transport.sessionno
        
    def dataReceived(self, data):
#         print "dataReceived:",data
#         _key,aresult = AsyncResultFactory().createAsyncResult()
#         result = aresult.get()
#         print result
        print self.transport.sendall('HTTP/1.1 200 OK\n\nHello world!!')
#         self.transport.close()
        
    def connectionLost(self, reason):
        pass
#         print "connectionLost",reason
        
class MyServerFactory(ServerFactory):
    protocol = MyProtocol
    
from gtwisted.utils import log

# def setAsyncResult(result):
#     while True:
#         AsyncResultFactory().async_reuslts.values()[0].set(result)

ss = MyServerFactory()
import sys
log.startLogging(sys.stdout)
reactor.listenTCP(90, ss)
# reactor.callLater(5, setAsyncResult,"okok")
reactor.run()



