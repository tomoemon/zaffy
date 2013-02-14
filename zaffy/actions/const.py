# -*- coding: utf-8 -*-
from baseaction import BaseAction


class _MetaConst(type):
  def __getattribute__(cls, name):
    return type.__getattribute__(cls, 'const_params')[name]


class Const(BaseAction):
  __metaclass__ = _MetaConst

  const_params = {}
  default_params = {}

  @classmethod
  def setup(cls, config):
    type.__setattr__(cls, 'default_params', dict(config))

  @classmethod
  def init_scenario(cls):
    """ 一時対応 """
    type.__setattr__(cls, 'const_params', dict(type.__getattribute__(cls, 'default_params')))

  def do_const(self, **kwargs):
    self.do_set(**kwargs)

  def do_set(self, **kwargs):
    for key, value in kwargs.items():
      if key in self.const_params:
        print 3, id(self.const_params)
        raise Exception("cannot overridden const key '{0}', value '{1}'".format(key, value))
      self.const_params[key] = value

    self.result = self.const_params

