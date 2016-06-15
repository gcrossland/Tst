from tst import t

def mul (a, b):
  t("multiplying {} and {}", a, b)
  return a * b

def sq (a):
  return mul(a, a)
