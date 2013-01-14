# -*- coding: utf-8 -*-
from baseaction import BaseAction
import os


class _MetaConst(type):
  def __getattribute__(cls, name):
    return type.__getattribute__(cls, 'get')(name, None)


class Env(BaseAction):
  """ 環境変数にアクセスするためのアクション """
  __metaclass__ = _MetaConst

  @classmethod
  def get(cls, name, default=None):
    if name in os.environ:
      return os.environ[name]
    else:
      if default:
        return default
      else:
        raise Exception("Undefined environment variable: '" + name + "'")

