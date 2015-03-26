#coding:utf8
'''
Created on 2014年2月20日\n
协议、工厂\n
@author:  lan (www.9miao.com)\n
'''
from gtwisted.core.base import Transport
from gevent import Greenlet
from gevent.socket import create_connection
from gtwisted.utils import log
import socket
import traceback

class BaseProtocol(Greenlet):
    """基础协议，一个协议就是一条单独的微线程在进行处理\n
    """
    
    def __init__(self,transport,factory):
        """每当一条连接建立是一个协议被实例化.\n
        @param transport: Transport 连接的通道实例(详见gtwisted.core.base 中对Transport的定义)\n
        @param factory: Factroy 之类值生成这个协议实例的工厂对象，可以是ClientFactory或ServerFactory\n
        """
        Greenlet.__init__(self)
        self.transport = transport
        self.factory = factory
        
    def connectionMade(self):
        """当连接建立时的处理\n
        """
        pass
        
    def connectionLost(self,reason):
        """当连接断开时的处理\n
        @param reason: Exception 端口连接的原因\n
        """
        pass
        
    def dataReceived(self, data):
        """当连接数据到达时的处理\n
        @param data: str 接收到的数据\n
        """
        pass
    
    def logPrefix(self):
        """
        """
        return str(self)
        
    def _run(self):
        """执行协议
        """
        self.connectionMade()
        try:
            while True:
                data = self.transport.recv(1024)
                if not data:
                    break
                import gevent
                gevent.spawn(self.dataReceived,data)
#                 self.dataReceived(data)
        except Exception,e:
            if not isinstance(e, socket.error):
                log.err(e,log.err(e,traceback.format_exc()))
            self.connectionLost(reason=e)
        else:
            self.connectionLost(reason=None)
        finally:
            self.transport.close()
            self.kill()
    
class ServerFactory:
    """服务端的协议工厂
    """
    
    protocol = BaseProtocol
    
    def __init__(self):
        """
        @param sessionno: int 用来记录客户端连接的动态编号\n
        """
        self.sessionno = 0
        
    def buildProtocol(self, transport):
        """
        @param transport: Transport 连接的通道实例(详见gtwisted.core.base 中对Transport的定义)\n
        """
        pass
    
    def __call__(self,socket,address):
        """每当有客户端连接产生是会被调用\n
        """
        t = Transport(socket,address,self.sessionno)
        t.start()
        self.buildProtocol(t)
        p = self.protocol(t,self)
        p.start()
        self.sessionno +=1
        
class ClientFactory:
    """客户端的协议工厂\n
    """
    
    protocol = BaseProtocol
    
    def __init__(self):
        """
        @param _protocol: Protocol 对象，一个客户端连接是只有一个协议实例产生的。\n
        """
        self._protocol = None
        
    def buildProtocol(self, transport):
        """
        @param transport: Transport 连接的通道实例(详见gtwisted.core.base 中对Transport的定义)\n
        """
        pass
    
    def startedConnecting(self,connector):
        """开始建立连接\n
        @param connector: BaseConnector (详见gtwisted.core.base 中对BaseConnector的定义)\n
        """
        address = connector.getHost()
        client = create_connection(address)
        t = Transport(client,address)
        t.start()
        self.buildProtocol(t)
        self._protocol = self.protocol(t,self)
    
    def doStart(self):
        """开始执行客户端协议\n
        """
        self._protocol.start()
        
        
        
    