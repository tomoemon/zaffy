# -*- coding: utf-8 -*-
import imp
import sys
import os
from os import path

def load_module(module_name, basepath):
  """ モジュールをロードして返す
  """
  f,n,d = imp.find_module(module_name,[basepath])
  return imp.load_module(module_name,f,n,d)

def load_modules(basepath):
  """ Pluginをロードしてリストにして返す
  """
  plugin_list = []
  for fdn in os.listdir(basepath):
    try:
      if not fdn.startswith('__') and fdn.endswith(".py"):
        m = load_module(fdn.replace(".py",""),basepath)
        plugin_list.append(m)
      elif os.path.isdir(fdn):
        m = load_module(fdn)
        plugin_list.append(m)
    except ImportError:
      pass
  return plugin_list

def load_module_dir(module_name):
  return load_modules(path.join(os.getcwd(), path.dirname(sys.argv[0]), module_name))

if __name__ == "__main__":
  plugindir = "plugins"  # Pluginが入っているディレクトリ
  cwd = os.getcwd()
  moduledir = os.path.join(cwd,plugindir)
  plugins = load_plugins(moduledir)   # Pluginを読み込む
  for p in plugins:
    p.foo()     # 読み込んだPluginの関数(foo)を呼び出す
