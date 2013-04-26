# -*- coding: utf-8 -*-
import os
import argparse


def _parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', action='store', dest='config_file', default=None)
  parser.add_argument('--nocolor', action='store_true', dest='without_color', default=False)
  parser.add_argument('--nodebug', action='store_true', dest='without_debug', default=False)
  parser.add_argument('-t', '--tag', nargs='+', action='store', dest='tag', default=())
  parser.add_argument('-i', action='store_true', dest='interactive', help='interactive mode')
  parser.add_argument('scenario', nargs='*', help="scenario files")
  return parser

__parser = _parser()
__result = __parser.parse_args()
print_help = __parser.print_help

targets = __result.scenario
config_file = __result.config_file
if config_file is None and os.access('zaffy.yml', os.R_OK):
  config_file = 'zaffy.yml'

interactive = __result.interactive
tags = __result.tag
without_color = __result.without_color
without_debug = __result.without_debug

