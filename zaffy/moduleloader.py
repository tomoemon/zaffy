# -*- coding: utf-8 -*-
import imp
import os
from os import path
import environment

class LoadError(Exception):
  def __init__(self, error_list):
    self.error_list = error_list

def load_module(module_name, basepath):
  """ モジュールをロードして返す
  imp.load_module は reload() と同じなので注意!!
  """
  f, n, d = imp.find_module(module_name, [basepath])
  return imp.load_module(module_name, f, n, d)


def load_modules(basepath):
  """ Pluginをロードしてリストにして返す
  """
  plugin_list = []
  error_list = []
  for filename in os.listdir(basepath):
    if filename.startswith('.'):
      continue

    try:
      if not filename.startswith('__') and filename.endswith(".py"):
        m = load_module(filename.replace(".py", ""), basepath)
        plugin_list.append(m)
      elif os.path.isdir(filename):
        m = load_module(filename, basepath)
        plugin_list.append(m)
    except ImportError as e:
      error_list.append((filename, e))
  error = LoadError(error_list) if error_list else None
  return plugin_list, error


def load_module_dir(module_name):
  return load_modules(path.join(environment.get_main_dir(), module_name))

if __name__ == "__main__":
  plugindir = "plugins"  # Pluginが入っているディレクトリ
  cwd = os.getcwd()
  moduledir = os.path.join(cwd,plugindir)
  plugins = load_module_dir(moduledir)   # Pluginを読み込む
  for p in plugins:
    p.foo()     # 読み込んだPluginの関数(foo)を呼び出す
