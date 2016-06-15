#!/usr/bin/env python2
import sys
import testeelib

if __name__ == "__main__":
  a = int(sys.argv[1])
  b = int(sys.argv[2])
  print "{} x {} is {}".format(a, b, testeelib.mul(a, b))
