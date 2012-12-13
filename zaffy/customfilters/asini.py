# -*- coding: utf-8 -*-
try:
  import configparser
except ImportError:
  import ConfigParser as configparser

import io

def do_asini(value):
  dummy_section = "__{0}__".format(id(value))
  value = "[{0}]\n".format(dummy_section) + value
  config = configparser.SafeConfigParser(allow_no_value=True)
  config.readfp(io.BytesIO(value))

  if len(config.sections()) == 1:
    result = {key: value for key, value in config.items(dummy_section)}
  else:
    config.remove_section(dummy_section)
    result = {}
    for section in config.sections():
      result[section] = {key: value for key, value in config.items(section)}
  return result

if __name__ == '__main__':
  d = """[hoge]
fuga=piyo
x= 10
y=
"""
  print do_asini(d)

  d = """
fuga=piyo
x= 10
y=
"""
  print do_asini(d)
