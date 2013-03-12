# -*- coding: utf-8 -*-
import os
import argparse
import util


def _parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', action='store', dest='config_file', default=None)
  parser.add_argument('--nocolor', action='store_false', dest='enable_color', default=True)
  parser.add_argument('scenarios', nargs='*', help="test files")
  return parser.parse_args()

__result = _parse()
targets = __result.scenarios
config_file = __result.config_file
if config_file is None and os.access('zaffy.yml', os.R_OK):
  config_file = 'zaffy.yml'

enable_color = __result.enable_color

