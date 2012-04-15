# -*- coding: utf-8 -*-

def do_classname(obj):
  return obj.__class__.__name__

def assert_classname(obj):
  return getattr(obj, "_value", obj).__class__.__name__

do_tocmp_on_asserting = [
  ['classname', assert_classname]
]
