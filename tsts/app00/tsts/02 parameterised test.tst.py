import os.path



D = "02/?.txt"

def checkContent (name):
  t("content is {!r}", file(name).readline())

def T (data):
  t("test data is {}", os.path.basename(data))
  checkContent(data)
  t("done!")
