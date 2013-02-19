# -*- coding: utf-8 -*-
from baseaction import BaseAction
import os
from six import with_metaclass


class _MetaEnv(type):
  def __getattribute__(cls, name):
    if not type.__getattribute__(cls, '_loaded'):
      # document 作成時は __doc__ などの属性にそのままアクセスさせる必要がある
      return type.__getattribute__(cls, name)
    return os.environ[name]


class Env(with_metaclass(_MetaEnv, BaseAction)):
  """ 環境変数にアクセスするためのアクション """
  _loaded = False

  @classmethod
  def setup(cls, config):
    type.__setattr__(cls, '_loaded', True)

