#coding:utf8
'''
Created on 2014年2月17日

@author:  lan (www.9miao.com)
'''
import errno


def untilConcludes(f, *a, **kw):
    """
    Call C{f} with the given arguments, handling C{EINTR} by retrying.

    @param f: A function to call.

    @param *a: Positional arguments to pass to C{f}.

    @param **kw: Keyword arguments to pass to C{f}.

    @return: Whatever C{f} returns.

    @raise: Whatever C{f} raises, except for C{IOError} or C{OSError} with
        C{errno} set to C{EINTR}.
    """
    while True:
        try:
            return f(*a, **kw)
        except (IOError, OSError) as e:
            if e.args[0] == errno.EINTR:
                continue
            raise
        