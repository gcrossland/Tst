# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  Tst Library
#  © Geoff Crossland 2016
# ------------------------------------------------------------------------------
import sys



frame = sys._getframe()
while frame.f_back:
  frame = frame.f_back
if not frame.f_globals.get('tstEnabled', False):
  def t (s, *args, **kwargs):
    pass
else:
  import contextlib
  import codecs
  import StringIO
  import os.path
  import os
  import traceback

  _inLogFile = None
  _inLogFileLine = None
  _failure = None
  _outLogFile = None

  @contextlib.contextmanager
  def testing (name, inPathName = None, outPathName = None):
    assert inPathName or outPathName
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
          d = os.path.dirname(outPathName)
          if not os.path.isdir(d):
            os.makedirs(d)
          _outLogFile = codecs.open(outPathName, 'w', 'utf-8')

        print "TEST " + name,
        try:
          yield
          t("")

          if inPathName:
            if _failure:
              print "- failed" + _failure
            else:
              print "- passed"
          else:
            assert not _failure
            print "- done"
        except:
          print "- error"
          print traceback.format_exc()
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

  def t (s, *args, **kwargs):
    global _failure
    global _inLogFileLine

    msg = s.format(*args, **kwargs)

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
          _failure = "\n  expected\n    {!r}\n  but got\n    {!r}\n  at log line {}\n\n".format(unicode(inLine), unicode(msgLine), _inLogFileLine) + "".join(traceback.format_list(traceback.extract_stack()[2:-1]))
          break
