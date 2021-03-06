#!/usr/bin/env python2
import sys
import os
import os.path
import cProfile
import glob
import inspect
tstEnabled = True
import tst
from tst import t, tv

_TESTS_DIR_LEAF_NAME = u"tsts"
_TEST_FILE_SUFFIX = u".tst.py"
_TEST_FN_NAME = 'T'
_TEST_DATA_EXPR_NAME = 'D'
_LOG_FILE_SUFFIX = u".log"
_GOOD_DIR_LEAF_NAME = u"tsts.good"
_OUT_DIR_LEAF_NAME = u"tsts.out"

def main (args):
  syntax = "Syntax: runtsts [run|cmp|prof]"
  modeCmp = False
  modeProf = False
  if len(args) == 0:
    modeCmp = True
  elif len(args) == 1:
    arg = args[0]
    if arg == "run":
      pass
    elif arg == "cmp":
      modeCmp = True
    elif arg == "prof":
      modeProf = True
    else:
      sys.exit(syntax)
  else:
    sys.exit(syntax)

  rootPathName = os.getcwdu()
  testsDirPathName = os.path.join(rootPathName, _TESTS_DIR_LEAF_NAME)
  if not os.path.isdir(testsDirPathName):
    sys.exit("The tests directory is missing")

  if modeProf:
    profile = cProfile.Profile()
    startProf = profile.enable
    stopProf = profile.disable
  else:
    startProf = stopProf = lambda: None

  testsDirPrefixLen = len(os.path.join(testsDirPathName, ""))
  g = globals()
  for testPathName in sorted(glob.iglob(os.path.join(testsDirPathName, "*" + _TEST_FILE_SUFFIX))):
    testName = testPathName[testsDirPrefixLen:-len(_TEST_FILE_SUFFIX)]

    execfile(testPathName, g, g)
    testFn = g.pop(_TEST_FN_NAME, None)
    testDataExpr = g.pop(_TEST_DATA_EXPR_NAME, None)

    if testDataExpr is None:
      testDataPathNames = (os.path.join(testsDirPathName, testName),)
      qualifySubtestNameWithTestDataName = False
    else:
      testDataPathNames = sorted(glob.iglob(os.path.join(testsDirPathName, testDataExpr)))
      qualifySubtestNameWithTestDataName = True

    try:
      inspect.getcallargs(testFn, u"")
      oneArg = True
    except TypeError:
      oneArg = False

    for testDataPathName in testDataPathNames:
      subtestName = testName
      if qualifySubtestNameWithTestDataName:
        testDataName = testDataPathName[testsDirPrefixLen:].replace(os.sep, " [] ")
        subtestName += "(" + testDataName + ")"

      i = None
      o = None
      if modeCmp:
        i = os.path.join(rootPathName, _GOOD_DIR_LEAF_NAME, subtestName + _LOG_FILE_SUFFIX)
      if not modeProf:
        o = os.path.join(rootPathName, _OUT_DIR_LEAF_NAME, subtestName + _LOG_FILE_SUFFIX)
      with tst.testing(subtestName, i, o):
        startProf()
        if oneArg:
          testFn(testDataPathName)
        else:
          testFn()
        stopProf()

  print ""
  totalCount, failureCount, errorCount = tst.report()
  print "Tests: " + str(totalCount)
  print "Failures: " + str(failureCount)
  print "Errors: " + str(errorCount)
  if modeProf:
    profile.print_stats('time')
    profile.print_stats('cumtime')

if __name__ == "__main__":
  main([arg.decode(sys.getfilesystemencoding() or sys.getdefaultencoding()) for arg in sys.argv[1:]])
