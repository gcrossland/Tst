import os
import os.path
import sys
import subprocess
import itertools
import codecs
import difflib
import shutil



def readFile (pathName):
  if os.path.isfile(pathName):
    with codecs.open(pathName, 'r', 'utf-8') as f:
      return f.readlines()
  else:
    return []

D = "app*"

def T (data):
  env = dict(os.environ)
  env['PYTHONPATH'] = str(os.path.join(data, "libraries")) + os.pathsep + env.get('PYTHONPATH', "")
  env['PYTHONIOENCODING'] = 'utf-8'
  p = subprocess.Popen(cwd = data, env = env, args = [sys.executable, u"../../runtsts.py", "cmp"], stdin = None, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
  out, err = p.communicate()

  t("rc {}", p.returncode)
  t("out\n--------\n{}\n--------", out)
  t("err\n--------\n{}\n--------", err)
  t("diffs\n--------")
  goodDirPathName = os.path.join(data, "tsts.good")
  outDirPathName = os.path.join(data, "tsts.out")
  for leafName in sorted(set(itertools.chain(os.listdir(goodDirPathName), os.listdir(outDirPathName)))):
    g = readFile(os.path.join(goodDirPathName, leafName))
    o = readFile(os.path.join(outDirPathName, leafName))
    t("{}", "".join(difflib.unified_diff(g, o, leafName, leafName)))
  t("--------")

  shutil.rmtree(outDirPathName)
