#coding:utf8
'''
Created on 2014年2月21日\n
网络连接中的一些元素，定时器，端口监听器，连接者，通道等\n
@author:  lan (www.9miao.com)\n
'''
from gevent.server import StreamServer,DatagramServer
from gevent.pywsgi import WSGIServer
from gevent import Greenlet
import gevent

class DelayCall:
    """延迟调用对象\n
    """
    
    def __init__(self,f,*args,**kw):
        """
        @param f: function f是一个function对象\n
        @param args: f的必要参数\n
        @param kw: f的可选参数\n
        """
        self.f = f
        self.args = args
        self.kw = kw
    
    def call(self):
        """调用执行函数，并且返回结果\n
        """
        return self.f(*self.args,**self.kw)
    
class Timer(Greenlet):
    
    def __init__(self,seconds,f,*args,**kw):
        """以一个微线程的方式实现一个定时器\n
        """
        Greenlet.__init__(self)
        self.seconds = seconds
        self.delay_call = DelayCall(f,*args,**kw)
        
    def cancel(self):
        """取消定时器\n
        """
        self.kill()
        
    def _run(self):
        """通过sleep进行延迟调用注册的函数,这里的sleep与线程的sleep不同，他是基于微线程的\n
        """
        gevent.sleep(self.seconds)
        return self.delay_call.call()
        

class Transport:
    
    def __init__(self,skt,address,sessionno=0):
        """基础连接通道\n
        @param skt: socket socket实例，所有的Transport通信通过它来实现\n
        @param address: (host,port) 一个包含了host和port的元组\n
        @param sessionno: int 由服务端生成的一个唯一的ID编号\n
        """
        self.skt = skt
        self.address = address
        self.sessionno = sessionno
        
    def getAddress(self):
        """获取地址\n
        """
        return self.address
        
    def close(self):
        """关闭通道连接\n
        """
        self.skt.close()
        
    def recv(self,*args):
        """接收消息\n
        """
        return self.skt.recv(*args)
    
    def sendall(self,data):
        """发送消息\n
        """
        return self.skt.sendall(data)


class BasePortListener(Greenlet):
    """基础的端口监听器\n
    """
    def __init__(self,port,factory,server_cls,port_type=""):
        """端口监听器\n
        @param port: int 监听的端口\n
        @param factory: Factory 协议工厂，包括了ServerFactory，ClientFactory，作为监听器主要指ServerFactory\n
        (协议工厂的定义在gtwisted.core.protocols中)\n
        @param server_cls: 处理监听事件的服务器这里包含了（StreamServer,DatagramServer，WSGIServer）等\n
        """
        Greenlet.__init__(self)
        self.port = port
        self.factory = factory
        self.server_cls = server_cls
        self.port_type = port_type
        
    def getHost(self):
        """获取主机地址\n
        """
        return "0.0.0.0",self.port
    
    def getPortType(self):
        """获取端口类型\n
        """
        return self.port_type
    
    def _run(self):
        """启动监听器\n
        """
        ser = self.server_cls(self.getHost(),self.factory,backlog=100000)
        ser.serve_forever()
    

class TCPPortListener(BasePortListener):
    """TCP服务端（端口监听器）\n
    """
    
    def __init__(self,port,factory):
        """TCP服务端（端口监听器）实例化。继承于BasePortListener，这里的server_cls采用的是StreamServer\n
        (可了解gevent的StreamServer的实例)\n
        """
        BasePortListener.__init__(self, port, factory, StreamServer,port_type="TCP")
        

class UDPPortListener(BasePortListener):
    """UDP服务端（端口监听器）\n
    """
    
    def __init__(self,port,factory):
        """UDP服务端（端口监听器）实例化。DatagramServer，这里的server_cls采用的是StreamServer\n
        (可了解gevent的DatagramServer的实例)\n
        """
        BasePortListener.__init__(self, port, factory, DatagramServer,port_type="UDP")
        
    
class WSGIPortListener(BasePortListener):
    """WSGI服务端（端口监听器）\n
    """
    def __init__(self,port,factory):
        """WSGI服务端（端口监听器）实例化。WSGIServer，这里的server_cls采用的是StreamServer\n
        (可了解gevent的WSGIServer的实例)\n
        """
        BasePortListener.__init__(self, port, factory, WSGIServer,port_type="WSGI")
        
class BaseConnector(Greenlet):
    """基础连接器，用于与服务端建立连接，并注册相应的协议进行通信\n
    """
    
    def __init__(self,address,factory):
        """
        @param address: （host，port）包含了host和port的元组\n
        @param factory: 协议工厂这里主要是指ClientFactory\n
        """
        Greenlet.__init__(self)
        self.address = address
        self.factory = factory
        
    def getHost(self):
        """获取主机地址\n
        """
        return self.address
        
    def connect(self):
        """开始连接\n
        """
        self.factory.startedConnecting(self)
        
    def _run(self):
        """进行预先定义好的协议进行处理连接和通信\n
        """
        self.factory.doStart()
        
    

