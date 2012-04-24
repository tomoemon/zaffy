# -*- coding: utf-8 -*-
from baseaction import BaseAction

class MetaConst(type):
  def __getattribute__(cls, name):
    if name == 'default_params':
      return type.__getattribute__(cls, 'default_params')
    return type.__getattribute__(cls, 'const_params')[name][-1]

class Const(BaseAction):
  __metaclass__ = MetaConst

  const_params = {}

  default_params = {
    "*":"",
  }

  def do_set(self):
    for key, value in self.setting.params.items():
      self.const_params[key] = [value]

  def do_push(self):
    for key, value in self.setting.params.items():
      self.const_params[key] = self.const_params.get(key, []) + [value]

  def do_pop(self):
    for key in self.setting.params.keys():
      self.const_params[key].pop()

