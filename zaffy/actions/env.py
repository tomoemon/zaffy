# -*- coding: utf-8 -*-
from baseaction import BaseAction
import os
from six import with_metaclass
from template import Undefined


class _MetaEnv(type):
  def __getattribute__(cls, name):
    if name.startswith('__'):
      return type.__getattribute__(cls, name)
    return os.environ.get(name, Undefined())


class Env(with_metaclass(_MetaEnv, BaseAction)):
  """ Env アクション

  環境変数を取得する

  .. code-block:: yaml

     - サンプルシナリオ

     - action: debug
       e1: <<env.PATH>> #=> 環境変数の Path を取得
       e2: <<env.HOGE>> #=> 存在しないので Undefined を取得
       e3: <<env.HOGE|d('xyz')>> #=> デフォルト値 'xyz' を取得
  """

  @classmethod
  def setup(cls, config):
    pass

