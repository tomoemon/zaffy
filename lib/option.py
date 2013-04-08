# -*- coding: utf-8 -*-
import os
import argparse


def _parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', action='store', dest='config_file', default=None)
  parser.add_argument('--nocolor', action='store_true', dest='without_color', default=False)
  parser.add_argument('--nodebug', action='store_true', dest='without_debug', default=False)
  parser.add_argument('scenarios', nargs='*', help="test files")
  return parser.parse_args()

__result = _parse()
targets = __result.scenarios
config_file = __result.config_file
if config_file is None and os.access('zaffy.yml', os.R_OK):
  config_file = 'zaffy.yml'

without_color = __result.without_color
without_debug = __result.without_debug

