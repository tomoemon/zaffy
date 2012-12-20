# -*- coding: utf-8 -*-
try:
  import configparser
except ImportError:
  import ConfigParser as configparser

import io

def do_asini(value):
  dummy_section = "__{0}__".format(id(value))
  value = "[{0}]\n".format(dummy_section) + value
  config = configparser.SafeConfigParser()
  config.readfp(io.StringIO(unicode(value)))

  if len(config.sections()) == 1:
    result = dict(config.items(dummy_section))
  else:
    config.remove_section(dummy_section)
    result = {section: dict(config.items(section)) for section in config.sections()}
  return result

if __name__ == '__main__':
  d = u"""[hoge]
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
