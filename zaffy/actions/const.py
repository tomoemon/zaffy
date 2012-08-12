# -*- coding: utf-8 -*-
from baseaction import BaseAction

class MetaConst(type):
  def __getattribute__(cls, name):
    if name == 'get_param_setting':
      return type.__getattribute__(cls, 'get_param_setting')
    return type.__getattribute__(cls, 'const_params')[name][-1]

class Const(BaseAction):
  __metaclass__ = MetaConst

  const_params = {}

  @classmethod
  def apply_config(cls, config):
    for key, value in config.items():
      config[key] = [value]
    type.__setattr__(cls, 'const_params', config)

  def do_set(self, **kwargs):
    for key, value in kwargs.items():
      self.const_params[key] = [value]

  def do_push(self, **kwargs):
    for key, value in kwargs.items():
      self.const_params[key] = self.const_params.get(key, []) + [value]

  def do_pop(self, **kwargs):
    for key in kwargs.keys():
      self.const_params[key].pop()

