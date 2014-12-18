#coding:utf8
'''
Created on 2014年2月17日

@author:  lan (www.9miao.com)
'''
from __future__ import division, absolute_import

defaultContextDict = {}

setDefault = defaultContextDict.__setitem__

class ContextTracker:
    """
    A L{ContextTracker} provides a way to pass arbitrary key/value data up and
    down a call stack without passing them as parameters to the functions on
    that call stack.

    This can be useful when functions on the top and bottom of the call stack
    need to cooperate but the functions in between them do not allow passing the
    necessary state.  For example::

        from twisted.python.context import call, get

        def handleRequest(request):
            call({'request-id': request.id}, renderRequest, request.url)

        def renderRequest(url):
            renderHeader(url)
            renderBody(url)

        def renderHeader(url):
            return "the header"

        def renderBody(url):
            return "the body (request id=%r)" % (get("request-id"),)

    This should be used sparingly, since the lack of a clear connection between
    the two halves can result in code which is difficult to understand and
    maintain.

    @ivar contexts: A C{list} of C{dict}s tracking the context state.  Each new
        L{ContextTracker.callWithContext} pushes a new C{dict} onto this stack
        for the duration of the call, making the data available to the function
        called and restoring the previous data once it is complete..
    """
    def __init__(self):
        self.contexts = [defaultContextDict]


    def callWithContext(self, newContext, func, *args, **kw):
        """
        Call C{func(*args, **kw)} such that the contents of C{newContext} will
        be available for it to retrieve using L{getContext}.

        @param newContext: A C{dict} of data to push onto the context for the
            duration of the call to C{func}.

        @param func: A callable which will be called.

        @param *args: Any additional positional arguments to pass to C{func}.

        @param **kw: Any additional keyword arguments to pass to C{func}.

        @return: Whatever is returned by C{func}

        @raise: Whatever is raised by C{func}.
        """
        self.contexts.append(newContext)
        try:
            return func(*args,**kw)
        finally:
            self.contexts.pop()


    def getContext(self, key, default=None):
        """
        Retrieve the value for a key from the context.

        @param key: The key to look up in the context.

        @param default: The value to return if C{key} is not found in the
            context.

        @return: The value most recently remembered in the context for C{key}.
        """
        for ctx in reversed(self.contexts):
            try:
                return ctx[key]
            except KeyError:
                pass
        return default

global theContextTracker
global call
global get

theContextTracker = ContextTracker()
call = theContextTracker.callWithContext
get = theContextTracker.getContext


