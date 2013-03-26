# -*- coding: utf-8 -*-
from baseaction import BaseAction
from six import with_metaclass


class _MetaConst(type):
  def __getattribute__(cls, name):
    if not type.__getattribute__(cls, '_loaded'):
      # document 作成時は __doc__ などの属性にそのままアクセスさせる必要がある
      return type.__getattribute__(cls, name)
    return type.__getattribute__(cls, '_const_params')[name]


class Const(with_metaclass(_MetaConst, BaseAction)):
  """Const アクション

  上書き不可能なグローバル定数をシナリオ実行単位内で定義する。シナリオ A が、シナリオ B (Const アクションを実行する) を :ref:`references-actions-require-label` すると、シナリオ A でも定数を参照することができる (=シナリオ実行単位でグローバル)。同じキーで再度定義しようとした場合、シナリオ実行時にエラーが発生する。

  また、config ファイルで事前に共通の定数を定義しておくことも可能。詳しくは

    ``zaffy/zaffy_sample.yml``

  を参照。


  .. code-block:: yaml

     - サンプルシナリオ

     - action: const
       user: taro
       pass: taropass

     - action: http.get
       url: http://yahoo.co.jp/
       params:
         user: <<const.user>>
         pass: <<const.pass>>
  """
  _loaded = False
  _const_params = {}
  _default_params = {}

  @classmethod
  def setup(cls, config):
    type.__setattr__(cls, '_loaded', True)
    type.__setattr__(cls, '_default_params', dict(config))

  @classmethod
  def init_scenario(cls):
    # 一時対応
    type.__setattr__(cls, '_const_params', dict(type.__getattribute__(cls, '_default_params')))

  def do_const(self, **kwargs):
    """do_set の省略呼び出し"""
    self.do_set(**kwargs)

  def do_set(self, **kwargs):
    """
    :param any (any): 任意のキーで任意の値を指定する
    :return dict: 現在定義されている定数の辞書を返す
    """
    for key, value in kwargs.items():
      if key in self._const_params:
        raise Exception("cannot overridden const key '{0}', value '{1}'".format(key, value))
      self._const_params[key] = value

    self.result = self._const_params

