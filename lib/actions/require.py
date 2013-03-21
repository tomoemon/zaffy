# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting
import os
import util


class Require(BaseAction):
  """ Require アクション

  外部のシナリオファイルを読み込み、実行する

  config ファイル

  * **root_path** (*string*): 読み込みファイルを絶対パスで指定した際の基準ディレクトリ

  """
  _root_path = ""

  @classmethod
  def setup(cls, config):
    if 'root_path' in config:
      cls._root_path = os.path.abspath(config['root_path'])

  def __getitem__(self, index):
    return self.result['actions'][index]

  def do_require(self, path, global_env, scenario):
    """ パラメータなしの呼び出し

    * A.yml

    .. code-block:: yaml

      - サンプルシナリオ

      - action: require
        path: B.yml

      - action: debug
        result: <<last.res.status>>

    * B.yml

    .. code-block:: yaml

      - サンプルシナリオ

      - action: sleep
        time: 1000

      - action: http.get
        url: http://yahoo.co.jp

    :param string path: 読み込みシナリオファイル。相対パスの場合は現在のシナリオファイルからの相対パス。絶対パスの場合は ``root_path`` を基準ディレクトリとして使用する。
    :return: - **any** (*dict*) - 読み込んだシナリオの最後のアクションの result
    """
    new_scenario = self._load(path, global_env, scenario, None)
    self.result = new_scenario.actions[-1].result

  def do_call(self, path, global_env, scenario, params=None):
    """ パラメータ付き呼び出し

    * A.yml

    .. code-block:: yaml

      - サンプルシナリオ

      - action: require.call
        path: B.yml
        params:
          x: 100
          y: 200

      - action: debug
        result: <<last.res.sum>>

    * B.yml

    .. code-block:: yaml

      - サンプルシナリオ

      - action: local
        sum: <<local.x + local.y>>

    :param string path: 読み込みシナリオファイル。相対パスの場合は現在のシナリオファイルからの相対パス。絶対パスの場合は ``root_path`` を基準ディレクトリとして使用する。
    :param any params: 読み込みシナリオに渡すパラメータ。渡されたパラメータは読み込みシナリオのローカル変数として参照可能。辞書を渡した場合はサンプルのように ``local.x`` 形式で参照可能、リストを渡した場合は ``local.0`` や ``local[0]`` のようにアクセスする。
    :return: - **any** (*dict*) - 読み込んだシナリオの最後のアクションの result
    """
    new_scenario = self._load(path, global_env, scenario, params)
    self.result = new_scenario.actions[-1].result

  def do_repeat(self, path, global_env, scenario, params):
    """ パラメータ付き繰り返し呼び出し

    * A.yml

    .. code-block:: yaml

      - サンプルシナリオ

      # B.yml を2回呼び出す
      - action: require.call
        path: B.yml
        params:
          - x: 100
            y: 200
          - x: 50
            y: 20

    * B.yml

    .. code-block:: yaml

      - サンプルシナリオ

      - action: local
        sum: <<local.x + local.y>>

      - action: debug
        result: <<local.sum>> # 1度目は 300, 2度目は 70 を表示

    :param string path: 読み込みシナリオファイル。相対パスの場合は現在のシナリオファイルからの相対パス。絶対パスの場合は ``root_path`` を基準ディレクトリとして使用する。
    :param list params: 読み込みシナリオに渡すパラメータ。リストの要素数が、繰り返し呼び出しを行なう回数になる。
    :return: - **any** (*dict*) - 読み込んだシナリオの最後のアクションの result
    """
    for param in params:
      self.do_call(path, global_env, scenario, param)

  @staticmethod
  def _replace_root(src_path, new_root):
    split = os.path.split
    head = tail = src_path
    while tail:
      head, tail = split(head)
    return os.path.join(new_root, src_path[len(head):])

  @staticmethod
  def _to_dict(params):
    if isinstance(params, dict):
      return params
    elif isinstance(params, list):
      return dict(enumerate(params))
    elif isinstance(params, (util.basestring, int, bool)):
      return {0: params}
    return {}

  def _load(self, path, global_env, scenario, params):
    path = path.strip()
    if not path:
      raise Exception(path + " not exists")

    if os.path.isabs(path):
      if self._root_path:
        path = self._replace_root(path, self._root_path)
    else:
        path = os.path.join(scenario.dir, path)

    new_scenario = scenario_loader.load(ScenarioSetting(path), scenario)
    new_scenario.localvar = self._to_dict(params)
    new_scenario.run(global_env)
    return new_scenario

