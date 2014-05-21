# -*- coding: utf-8 -*-
from baseaction import BaseAction


class _PresetApplier(object):
  DEFAULT_NAME = 'default'

  def __init__(self, action_name, preset_name, is_merge):
    self.action_name = action_name
    self.preset_name = preset_name if preset_name else self.DEFAULT_NAME
    self.is_merge = is_merge

  def apply(self, action_params):
    presets = Preset.get_action_presets(self.action_name)
    if presets is None:
      return action_params
    elif self.preset_name == self.DEFAULT_NAME:
      if self.DEFAULT_NAME not in presets:
        return action_params
    elif self.preset_name not in presets:
      raise Exception("preset '" + self.action_name + "." + self.preset_name + "' is not defined")

    preset_params = dict(presets[self.preset_name])
    self.apply_params(preset_params, action_params, self.is_merge)
    return preset_params

  @staticmethod
  def apply_params(before, after, is_merge):
    for key, value in after.items():
      if key not in before or type(before[key]) is not type(value) or not is_merge:
        # preset に存在しないキー、または型が違う、または上書きモードの場合は上書き
        before[key] = value
      else:
        if isinstance(value, list):
          before[key].extend(value)
        elif isinstance(value, dict):
          before[key].update(value)
        else:
          # 数値・文字列の場合は上書き
          before[key] = value


class Preset(BaseAction):
  """ Preset アクション

  任意のアクションに対する実行時のパラメータプリセットを定義する。アクションに対して多数のパラメータを繰り返し適用する場合、事前にプリセットを定義しておくことでシナリオをシンプルにできる。:ref:`references-actions-const-label` アクションと同様にシナリオ実行単位でグローバルに参照可能。

  定義の上書き
    すでに定義済みのプリセット名と同じ名前で定義した場合、後から定義したパラメータセットで完全に上書きされる。異なるアクション間で同名のプリセット名を持つことは可能。

  評価のタイミング
    preset アクションで定義したパラメータセットは、preset アクションが実行されたタイミングで評価される。パラメータセットの中で :ref:`references-actions-const-label` 定数や :ref:`references-actions-local-label` 変数の使用、または関数呼び出しを記述していた場合、その時点での値でパラメータセットが確定する。評価を遅延させたい場合は

    ``<<"<<const.param1>>">>``

    のように preset アクション実行時は後から展開可能な文字列として定義する。

  .. note::
    YAML 形式がもともと備えているエイリアス・アンカーといった機能をシナリオ内で使うことも可能
    http://jp.rubyist.net/magazine/?0009-YAML#l10

  .. code-block:: yaml

     - サンプルシナリオ

     - action: preset
       http:
         default:
           url: http://yahoo.co.jp/

     # default preset の適用
     #   アクションに対して何も渡していないが default プリセットがあるので
     #   url: http://yahoo.co.jp/ に対して http get する
     - action: http

     - action: preset
       http:
         assert404:
           assert:
             - out.status is 404

     # named preset の適用
     #   assert を定義していないが status が 404 であることをテストしている
     - action: http.get < assert404
       url: http://yahoo.co.jp/hogehoge
  """
  _presets = {}
  _default_presets = {}

  @classmethod
  def setup(cls, config):
    cls._default_presets = config

  @classmethod
  def init_scenario(cls):
    # 一時対応
    cls._presets = dict(cls._default_presets)

  @classmethod
  def get_action_presets(cls, action_name):
    return cls._presets.get(action_name, None)

  @classmethod
  def get_applier(cls, action_name, preset_name, is_merge):
    return _PresetApplier(action_name, preset_name, is_merge)

  @classmethod
  def reset(cls):
    cls._presets = {}

  def do_preset(self, **params):
    """ preset を定義する

    :param any (any): 1階層目には存在するアクション名、2階層目にプリセット名、3階層目以降に定義するパラメータセットを辞書形式で指定する
    :return: None
    """
    for target_action, presets in params.items():
      self._presets[target_action] = presets

