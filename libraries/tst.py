# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  Tst Library
#  © Geoff Crossland 2016
# ------------------------------------------------------------------------------
import sys

##
# When in testing mode, logs the format string s formatted according to the
# remaining arguments (or, otherwise, does nothing).
def t (s, *args, **kwargs):
  pass

##
# When in testing mode, logs the current value of a local variable (or,
# otherwise, does nothing).
def tv (varName):
  pass

frame = sys._getframe()
while frame.f_back:
  frame = frame.f_back
if frame.f_globals.get('tstEnabled', False):
  import contextlib
  import codecs
  import StringIO
  import os.path
  import os
  import traceback

  def _ensureDir (d):
    if not os.path.isdir(d):
      os.makedirs(d)

  _totalCount = 0
  _failureCount = 0
  _errorCount = 0
  _inLogFile = None
  _inLogFileLine = None
  _failure = None
  _outLogFile = None

  @contextlib.contextmanager
  def testing (name, inPathName = None, outPathName = None):
    global _totalCount
    global _failureCount
    global _errorCount
    global _inLogFile
    global _inLogFileLine
    global _failure
    global _outLogFile

    assert not _inLogFile
    assert not _inLogFileLine
    assert not _failure
    assert not _outLogFile
    try:
      try:
        if inPathName:
          if os.path.isfile(inPathName):
            _inLogFile = codecs.open(inPathName, 'r', 'utf-8')
          else:
            _inLogFile = StringIO.StringIO(u"")
          _inLogFileLine = 0
        if outPathName:
          _ensureDir(os.path.dirname(outPathName))
          _outLogFile = codecs.open(outPathName, 'w', 'utf-8')

        print "* " + name,
        _totalCount += 1
        try:
          yield
          t("")

          if inPathName:
            if _failure:
              print "- failed" + _failure
              _failureCount += 1
            else:
              print "- passed"
          else:
            assert not _failure
            print "- done"
        except:
          print "- error"
          print traceback.format_exc()
          _errorCount += 1
      finally:
        if _outLogFile:
          _outLogFile.close()
          _outLogFile = None
    finally:
      _failure = None
      if _inLogFile:
        _inLogFile.close()
        _inLogFile = None
        _inLogFileLine = None

  def report ():
    return (_totalCount, _failureCount, _errorCount)

  def _log (msg):
    global _failure
    global _inLogFileLine

    if _outLogFile:
      _outLogFile.write(msg)
      _outLogFile.write('\n')

    if _inLogFile and not _failure:
      for msgLine in msg.split('\n'):
        inLine = _inLogFile.readline()
        _inLogFileLine += 1
        if inLine.endswith('\n'):
          inLine = inLine[:-1]
        if msgLine != inLine:
          _failure = "\n  expected\n    {!r}\n  but got\n    {!r}\n  at log line {}\n\n".format(unicode(inLine), unicode(msgLine), _inLogFileLine) + "".join(traceback.format_list(traceback.extract_stack()[2:-2]))
          break

  def t (s, *args, **kwargs):
    _log(s.format(*args, **kwargs))

  def tv (varName):
    frame = sys._getframe(1)
    varVal = frame.f_locals[varName]
    _log("{} = {}".format(varName, varVal))
