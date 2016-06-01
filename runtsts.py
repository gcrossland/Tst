#!/usr/bin/env python2
import sys
import os
import os.path
import glob
import inspect
tstEnabled = True
from tst import t, testing



_TESTS_DIR_LEAF_NAME = u"tsts"
_TEST_FILE_SUFFIX = u".tst.py"
_TEST_FN_NAME = 'T'
_TEST_DATA_EXPR_NAME = 'D'
_LOG_FILE_SUFFIX = u".log"
_GOOD_DIR_LEAF_NAME = u"tsts.good"
_OUT_DIR_LEAF_NAME = u"tsts.out"

def main (args):
  cmp = len(args) != 0 and args[0] == "cmp"

  rootPathName = os.getcwdu()
  testsDirPrefixLen = len(os.path.join(rootPathName, _TESTS_DIR_LEAF_NAME, ""))
  g = globals()
  for testPathName in sorted(glob.iglob(os.path.join(rootPathName, _TESTS_DIR_LEAF_NAME, "*" + _TEST_FILE_SUFFIX))):
    testName = testPathName[testsDirPrefixLen:-len(_TEST_FILE_SUFFIX)]

    execfile(testPathName, g, g)
    testFn = g.pop(_TEST_FN_NAME, None)
    testDataExpr = g.pop(_TEST_DATA_EXPR_NAME, None)

    if testDataExpr is None:
      testDataPathNames = (os.path.join(rootPathName, _TESTS_DIR_LEAF_NAME, testName),)
      qualifySubtestNameWithTestDataName = False
    else:
      testDataPathNames = sorted(glob.iglob(os.path.join(rootPathName, _TESTS_DIR_LEAF_NAME, testDataExpr)))
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
      if cmp:
        i = os.path.join(rootPathName, _GOOD_DIR_LEAF_NAME, subtestName + _LOG_FILE_SUFFIX)
      o = os.path.join(rootPathName, _OUT_DIR_LEAF_NAME, subtestName + _LOG_FILE_SUFFIX)
      with testing(subtestName, i, o):
        if oneArg:
          testFn(testDataPathName)
        else:
          testFn()



if __name__ == "__main__":
  envEncoding = sys.stdin.encoding or sys.getdefaultencoding()
  main([arg.decode(envEncoding) for arg in sys.argv[1:]])