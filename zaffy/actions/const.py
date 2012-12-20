# -*- coding: utf-8 -*-
from baseaction import BaseAction

class MetaConst(type):
  def __getattribute__(cls, name):
    return type.__getattribute__(cls, 'const_params')[name]

class Const(BaseAction):
  __metaclass__ = MetaConst

  const_params = {}

  @classmethod
  def apply_config(cls, config):
    type.__setattr__(cls, 'const_params', config)

  def do_set(self, **kwargs):
    for key, value in kwargs.items():
      if key in self.const_params:
        raise Exception("'const.{0}' already exists.\n  old: {1}\n  new: {2}".format(
          key, self.const_params[key], value))
      self.const_params[key] = value

