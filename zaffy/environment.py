# -*- coding: utf-8 -*-
import sys
import os
import imp

_scenario_dir = ""

if hasattr(sys,"setdefaultencoding"):
  sys.setdefaultencoding("utf-8")

def main_is_frozen():
  return (hasattr(sys, "frozen") or # new py2exe
    hasattr(sys, "importers") # old py2exe
    or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
  if main_is_frozen():
    return os.path.abspath(os.path.dirname(sys.executable))
  return os.path.abspath(os.path.dirname(sys.argv[0]))

def get_scenario_dir():
  return _scenario_dir

def set_scenario_dir(dirname):
  global _scenario_dir
  _scenario_dir = dirname

