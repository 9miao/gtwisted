#coding:utf8
'''
Created on 2014年2月17日
日志的处理
@author:  lan (www.9miao.com)
'''
# from gtwisted.utils import reflect,context,output
# import sys
# import time
# from datetime import datetime
# 
# class BaseLogObserver:
#     """日志观察者的基类
#     """
#     
#     def __call__(self,eventDict):
#         """接收到日志时间后的处理方式
#         @param eventDict: 事件的内容
#         """
#         pass
# 
# context.setDefault(BaseLogObserver,
#                    {"isError": 0,
#                     "system": "-"})
# 
# def _safeFormat(fmtString, fmtDict):
#     """尝试用fmtString参数来格式化字符串fmtString,发生错误则放回错误的信息
#     """
#     try:
#         text = fmtString % fmtDict
#     except KeyboardInterrupt:
#         raise
#     except:
#         try:
#             text = ('Invalid format string or unformattable object in log message: %r, %s' % (fmtString, fmtDict))
#         except:
#             try:
#                 text = 'UNFORMATTABLE OBJECT WRITTEN TO LOG with fmt %r, MESSAGE LOST' % (fmtString,)
#             except:
#                 text = 'PATHOLOGICAL ERROR IN BOTH FORMAT STRING AND MESSAGE DETAILS, MESSAGE LOST'
#     return text
#         
# def textFromEventDict(eventDict):
#     """从日志事件中解析出事件内容
#     """
#     edm = eventDict['message']
#     if not edm:
#         if eventDict['isError'] and 'failure' in eventDict:
#             text = ((eventDict.get('why') or 'Unhandled Error')
#                     + '\n' + eventDict['failure'].getTraceback())
#         elif 'format' in eventDict:
#             text = _safeFormat(eventDict['format'], eventDict)
#         else:
#             return
#     else:
#         text = ' '.join(map(reflect.safe_str, edm))
#     return text
# 
# 
# class LogPublisher:
#     """
#     Class for singleton log message publishing.
#     """
# 
#     synchronized = ['msg']
# 
#     def __init__(self):
#         self.observers = []
# 
#     def addObserver(self, other):
#         """
#         Add a new observer.
# 
#         @type other: Provider of L{ILogObserver}
#         @param other: A callable object that will be called with each new log
#             message (a dict).
#         """
#         assert callable(other)
#         self.observers.append(other)
# 
#     def removeObserver(self, other):
#         """
#         Remove an observer.
#         """
#         self.observers.remove(other)
# 
#     def msg(self, *message, **kw):
#         """
#         Log a new message.
# 
#         The message should be a native string, i.e. bytes on Python 2 and
#         Unicode on Python 3. For compatibility with both use the native string
#         syntax, for example::
# 
#         >>> log.msg('Hello, world.')
# 
#         You MUST avoid passing in Unicode on Python 2, and the form::
# 
#         >>> log.msg('Hello ', 'world.')
# 
#         This form only works (sometimes) by accident.
#         """
#         actualEventDict = (context.get(BaseLogObserver) or {}).copy()
#         actualEventDict.update(kw)
#         actualEventDict['message'] = message
#         actualEventDict['time'] = time.time()
#         for i in range(len(self.observers) - 1, -1, -1):
#             try:
#                 self.observers[i](actualEventDict)
#             except KeyboardInterrupt:
#                 # Don't swallow keyboard interrupt!
#                 raise
#             except UnicodeEncodeError:
#                 raise
#             except:
#                 observer = self.observers[i]
#                 self.observers[i] = lambda event: None
#                 try:
#                     self._err(Exception(),
#                         "Log observer %s failed." % (observer,))
#                 except:
#                     # Sometimes err() will throw an exception,
#                     # e.g. RuntimeError due to blowing the stack; if that
#                     # happens, there's not much we can do...
#                     pass
#                 self.observers[i] = observer
# 
# 
#     def _err(self, failure, why):
#         """
#         Log a failure.
# 
#         Similar in functionality to the global {err} function, but the failure
#         gets published only to observers attached to this publisher.
# 
#         @param failure: The failure to log.
#         @type failure: L{Failure}.
# 
#         @param why: The source of this failure.  This will be logged along with
#             the C{failure} and should describe the context in which the failure
#             occurred.
#         @type why: C{str}
#         """
#         self.msg(failure=failure, why=why, isError=1)
# 
# 
#     def showwarning(self, message, category, filename, lineno, logfile=None,
#                     line=None):
#         """
#         Twisted-enabled wrapper around L{warnings.showwarning}.
# 
#         If C{logfile} is C{None}, the default behaviour is to emit the warning to
#         the log system, otherwise the original L{warnings.showwarning} Python
#         function is called.
#         """
#         if logfile is None:
#             self.msg(warning=message, category=reflect.qual(category),
#                      filename=filename, lineno=lineno,
#                      format="%(filename)s:%(lineno)s: %(category)s: %(warning)s")
# 
# 
# if not globals().get('theLogPublisher'):
#     theLogPublisher = LogPublisher()
#     addObserver = theLogPublisher.addObserver
#     removeObserver = theLogPublisher.removeObserver
#     msg = theLogPublisher.msg
#     showwarning = theLogPublisher.showwarning
# 
# def err(_stuff=None, _why=None, **kw):
#     """
#     Write a failure to the log.
# 
#     The C{_stuff} and C{_why} parameters use an underscore prefix to lessen
#     the chance of colliding with a keyword argument the application wishes
#     to pass.  It is intended that they be supplied with arguments passed
#     positionally, not by keyword.
# 
#     @param _stuff: The failure to log.  If C{_stuff} is C{None} a new
#         L{Failure} will be created from the current exception state.  If
#         C{_stuff} is an C{Exception} instance it will be wrapped in a
#         L{Failure}.
#     @type _stuff: C{NoneType}, C{Exception}, or L{Failure}.
# 
#     @param _why: The source of this failure.  This will be logged along with
#         C{_stuff} and should describe the context in which the failure
#         occurred.
#     @type _why: C{str}
#     """
#     if isinstance(_stuff, Exception):
#         msg(failure=_stuff, why=_why, isError=1, **kw)
#     else:
#         msg(repr(_stuff), why=_why, isError=1, **kw)
# 
# deferr = err
# 
# 
# class FileLogObserver:
#     """
#     Log observer that writes to a file-like object.
# 
#     @type timeFormat: C{str} or C{NoneType}
#     @ivar timeFormat: If not C{None}, the format string passed to strftime().
#     """
#     timeFormat = None
# 
#     def __init__(self, f):
#         self.write = f.write
#         self.flush = f.flush
# 
# 
#     def getTimezoneOffset(self, when):
#         """
#         Return the current local timezone offset from UTC.
# 
#         @type when: C{int}
#         @param when: POSIX (ie, UTC) timestamp for which to find the offset.
# 
#         @rtype: C{int}
#         @return: The number of seconds offset from UTC.  West is positive,
#         east is negative.
#         """
#         offset = datetime.utcfromtimestamp(when) - datetime.fromtimestamp(when)
#         return offset.days * (60 * 60 * 24) + offset.seconds
# 
# 
#     def formatTime(self, when):
#         """
#         Format the given UTC value as a string representing that time in the
#         local timezone.
# 
#         By default it's formatted as a ISO8601-like string (ISO8601 date and
#         ISO8601 time separated by a space). It can be customized using the
#         C{timeFormat} attribute, which will be used as input for the underlying
#         L{datetime.datetime.strftime} call.
# 
#         @type when: C{int}
#         @param when: POSIX (ie, UTC) timestamp for which to find the offset.
# 
#         @rtype: C{str}
#         """
#         if self.timeFormat is not None:
#             return datetime.fromtimestamp(when).strftime(self.timeFormat)
# 
#         tzOffset = -self.getTimezoneOffset(when)
#         when = datetime.utcfromtimestamp(when + tzOffset)
#         tzHour = abs(int(tzOffset / 60 / 60))
#         tzMin = abs(int(tzOffset / 60 % 60))
#         if tzOffset < 0:
#             tzSign = '-'
#         else:
#             tzSign = '+'
#         return '%d-%02d-%02d %02d:%02d:%02d%s%02d%02d' % (
#             when.year, when.month, when.day,
#             when.hour, when.minute, when.second,
#             tzSign, tzHour, tzMin)
# 
#     def emit(self, eventDict):
#         text = textFromEventDict(eventDict)
#         if text is None:
#             return
# 
#         timeStr = self.formatTime(eventDict['time'])
#         fmtDict = {'system': eventDict['system'], 'text': text.replace("\n", "\n\t")}
#         msgStr = _safeFormat("[%(system)s] %(text)s\n", fmtDict)
# 
#         output.untilConcludes(self.write, timeStr + " " + msgStr)
#         output.untilConcludes(self.flush)  # Hoorj!
# 
#     def start(self):
#         """
#         Start observing log events.
#         """
#         addObserver(self.emit)
# 
#     def stop(self):
#         """
#         Stop observing log events.
#         """
#         removeObserver(self.emit)
# 
# class StdioOnnaStick:
#     """
#     Class that pretends to be stdout/err, and turns writes into log messages.
# 
#     @ivar isError: boolean indicating whether this is stderr, in which cases
#                    log messages will be logged as errors.
# 
#     @ivar encoding: unicode encoding used to encode any unicode strings
#                     written to this object.
#     """
# 
#     closed = 0
#     softspace = 0
#     mode = 'wb'
#     name = '<stdio (log)>'
# 
#     def __init__(self, isError=0, encoding=None):
#         self.isError = isError
#         if encoding is None:
#             encoding = sys.getdefaultencoding()
#         self.encoding = encoding
#         self.buf = ''
#   
#     def close(self):
#         pass
# 
#     def fileno(self):
#         return -1
# 
#     def flush(self):
#         pass
# 
#     def read(self):
#         raise IOError("can't read from the log!")
# 
#     readline = read
#     readlines = read
#     seek = read
#     tell = read
# 
#     def write(self, data):
#         data = data.encode(self.encoding)
#         d = (self.buf + data).split('\n')
#         self.buf = d[-1]
#         messages = d[0:-1]
#         for message in messages:
#             msg(message, printed=1, isError=self.isError)
# 
#     def writelines(self, lines):
#         for line in lines:
#             line = line.encode(self.encoding)
#             msg(line, printed=1, isError=self.isError)
# 
# 
# class DefaultObserver:
#     """
#     Default observer.
# 
#     Will ignore all non-error messages and send error messages to sys.stderr.
#     Will be removed when startLogging() is called for the first time.
#     """
#     stderr = sys.stderr
# 
#     def _emit(self, eventDict):
#         if eventDict["isError"]:
#             if 'failure' in eventDict:
#                 text = ((eventDict.get('why') or 'Unhandled Error')
#                         + '\n' + eventDict['failure'].getTraceback())
#             else:
#                 text = " ".join([str(m) for m in eventDict["message"]]) + "\n"
# 
#             self.stderr.write(text)
#             self.stderr.flush()
# 
#     def start(self):
#         addObserver(self._emit)
# 
#     def stop(self):
#         removeObserver(self._emit)
# 
# if not globals().get('defaultObserver'):
#     defaultObserver = DefaultObserver()
#     defaultObserver.start()
#     
# 
# 
# def startLogging(logfile, *a, **kw):
#     """
#     Initialize logging to a specified file.
# 
#     @return: A L{FileLogObserver} if a new observer is added, None otherwise.
#     """
#     if isinstance(logfile, StdioOnnaStick):
#         return
#     flo = FileLogObserver(logfile)
#     startLoggingWithObserver(flo.emit, *a, **kw)
#     return flo
# 
# 
# def startLoggingWithObserver(observer, setStdout=1):
#     """
#     Initialize logging to a specified observer. If setStdout is true
#     (defaults to yes), also redirect sys.stdout and sys.stderr
#     to the specified file.
#     """
#     global defaultObserver
#     if defaultObserver:
#         defaultObserver.stop()
#         defaultObserver = None
#     addObserver(observer)
#     msg("Log opened.")
from twisted.python.log import *
    