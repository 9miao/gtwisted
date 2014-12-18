#coding:utf8
'''
Created on 2014年2月21日
这里定义了框架中所有可能出现的错误信息
@author:  lan (www.9miao.com)
'''

class ReactorAlreadyInstalledError(AssertionError):
    """
    Could not install reactor because one is already installed.\n
    """
    
class RPCDataTooLongError(AssertionError):
    """RPC调用的数据包长度过长\n
    """
    
    def __str__(self, *args, **kwargs):
        """
        """
        return "RPC data too long."
    
