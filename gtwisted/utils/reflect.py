#coding:utf8
'''
Created on 2014年2月17日

@author:  lan (www.9miao.com)
'''
from io import StringIO
import traceback

def _determineClass(x):
    try:
        return x.__class__
    except:
        return type(x)
    
def _determineClassName(x):
    c = _determineClass(x)
    try:
        return c.__name__
    except:
        try:
            return str(c)
        except:
            return '<BROKEN CLASS AT 0x%x>' % id(c)
        
def qual(clazz):
    """
    Return full import path of a class.
    """
    return clazz.__module__ + '.' + clazz.__name__

def _safeFormat(formatter, o):
    """
    Helper function for L{safe_repr} and L{safe_str}.
    """
    try:
        return formatter(o)
    except:
        io = StringIO()
        traceback.print_exc(file=io)
        className = _determineClassName(o)
        tbValue = io.getvalue()
        return "<%s instance at 0x%x with %s error:\n %s>" % (
            className, id(o), formatter.__name__, tbValue)
        
def safe_repr(o):
    """
    Returns a string representation of an object, or a string containing a
    traceback, if that object's __repr__ raised an exception.

    @param o: Any object.

    @rtype: C{str}
    """
    return _safeFormat(repr, o)



def safe_str(o):
    """
    Returns a string representation of an object, or a string containing a
    traceback, if that object's __str__ raised an exception.

    @param o: Any object.

    @rtype: C{str}
    """
    return _safeFormat(str, o)
