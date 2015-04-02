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

    # preset_params は変更禁止
    preset_params = presets[self.preset_name]
    return self.apply_params(preset_params, action_params, self.is_merge)

  @staticmethod
  def apply_params(before, after, is_merge):
    after = dict(after)
    for key, value in before.items():
      if key not in after:
        # action 作成時にセットされていないキーの場合は preset の値をそのまま使う
        after[key] = value
      elif is_merge:
        if type(value) is not type(after[key]):
          raise Exception("merging preset parameter failed: types of '{0}' are different".format(key))
        elif isinstance(value, list):
          after[key] = value + after[key]
        elif isinstance(value, dict):
          after[key].update(value)
    return after


class Preset(BaseAction):
  """ Preset アクション

  http や ssh 等の任意のアクションに対するパラメータプリセットを定義する。認証等のためにアクション作成時に多数のパラメータを繰り返し適用しなければならない場合、事前にプリセットを定義しておくことでシナリオをシンプルにできる。:ref:`references-actions-const-label` アクションと同様にシナリオ実行単位でグローバルに参照可能。

  プリセットの作成
    プリセットを作成するには「対象アクション」「プリセット名」「パラメータセット」を下記のように指定する必要がある。プリセット名を ``default`` にした場合、対象アクションを実行する際に暗黙的に該当のプリセットパラメータが適用される。

    .. code-block:: yaml

       - action: preset
         http:                         # 対象アクション
           assert200:                  # プリセット名
             url: http://yahoo.co.jp/  # パラメータセット: 対象アクションで使用可能なパラメータを任意の数セットする
             assert:                   # assert もセットできる
               - out.status is eq 200

  プリセットの使用
    上記のプリセットが作成された後、アクションを作成する際にアクション名の後ろに ``<`` とプリセット名を記述することでプリセットパラメータを使用することができる。下記の例では google.com にアクセスした上で、ステータスコードが 200 であることを検証する。プリセットのパラメータと同一のキーをアクション作成時にセットした場合は、アクション側のパラメータで上書きされる。ただし、``<<`` を使ってプリセットを適用した場合でかつパラメータがリストか辞書の場合は、マージされる。

    .. code-block:: yaml

       - action: http.get < assert200
         url: http://google.com/

  プリセットの上書き
    すでに作成済みのプリセット名と同じ名前でプリセットを作成した場合、後から作成したパラメータセットで完全に上書きされる。異なるアクションを対象にした同名のプリセットを持つことは可能。

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
       local:
         set_list:
           x:
             - 100

     # default preset の適用
     #   アクションに対して何も渡していないが default プリセットがあるので
     #   url: http://yahoo.co.jp/ に対して http get する
     - action: http

     - action: preset
       http:
         assert404:
           assert:
             - out.status is 404

     # named preset の適用（同一キーのパラメータは上書き）
     #   assert を定義していないが status が 404 であることをテストしている
     - action: http.get < assert404
       url: http://yahoo.co.jp/hogehoge

     # named preset の適用（同一キーのパラメータはできるだけマージする）
     #   action 定義の x と preset の x がマージされる
     - action: http.get << set_list
       x:
         - 200
       assert:
         - out.x is eq [100,200]
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

