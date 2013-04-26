# -*- coding: utf-8 -*-
import os
import argparse


def _parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', action='store', dest='config_file', default=None)
  parser.add_argument('--nocolor', action='store_true', dest='without_color', default=False)
  parser.add_argument('--nodebug', action='store_true', dest='without_debug', default=False)
  parser.add_argument('-t', '--tag', nargs='+', action='store', dest='tag', default=())
  parser.add_argument('scenario', nargs='*', help="scenario files")
  return parser.parse_args()

__result = _parse()
targets = __result.scenario
config_file = __result.config_file
if config_file is None and os.access('zaffy.yml', os.R_OK):
  config_file = 'zaffy.yml'

tags = __result.tag
without_color = __result.without_color
without_debug = __result.without_debug

