# -*- coding: utf-8 -*-
import os
from os import path
import argparse

"""
root_dir を指定した上で、
"""

def _parse():
  parser = argparse.ArgumentParser(description='テストツールです')
  #parser.add_argument('-r', '--root', action='store', dest='root_dir')
  parser.add_argument('-c', '--config', action='store', dest='config_file', default=None)
  parser.add_argument('scenarios', nargs='+')
  return parser.parse_args()

class TestTarget(object):
  def __init__(self, root_dir, filename):
    self.root_dir = root_dir
    self.filename = filename

def _filter_args(args):
  scenario_root = None
  if args.root_dir:
    filename = path.normcase(path.abspath(args.root_dir))
    if not os.access(filename, os.F_OK):
      raise IOError(filename + " NOT EXISTS")
    if path.isdir(filename):
      scenario_root = filename
    else:
      raise IOError(filename + " IS NOT DIRECTORY")

  scenario_files = []
  scenario_dirs = []
  for filename in args.scenarios:
    filename = path.normcase(path.abspath(filename))
    if not os.access(filename, os.F_OK):
      raise IOError(filename + " NOT EXISTS")
    if path.isfile(filename):
      scenario_files.append(filename)
    elif path.isdir(filename):
      scenario_dirs.append(filename)
    else:
      raise Exception(filename + " UNKNOWN FILETYPE")

def _add_target(scenario_root, filename, targets):
  if filename in _added_fileset:
    return
  scenario_root = scenario_root if scenario_root else path.dirname(filename)
  targets.append(TestTarget(scenario_root, filename))

__result = _parse()
targets = __result.scenarios
config_file = __result.config_file
if config_file is None and os.access('zaffy.yml', os.R_OK):
  config_file = 'zaffy.yml'

#_added_fileset = set()
#targets = _filter_args(_parse())
#
#print [(key, item) for key, item in locals().items() if key.startswith('scenario')]
