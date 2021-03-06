# -*- coding: utf-8 -*-
import template
import ast
import inspect
import util


class ActionParams(object):

  def __init__(self, setting, action_klass, preset):

    try:
      method = type.__getattribute__(action_klass, 'do_' + setting.method_name)
    except AttributeError as e:
      raise Exception("'{0}' action has no '{1}' method".format(setting.action_name, setting.method_name))
    self._argspec = inspect.getargspec(method)
    self._preset = preset
    self._raw_params = setting.params

    self.params = None
    self.debug = False
    self.enable = True
    self.filter_list = None
    self.assert_list = None
    self.assertex_list = None

  def expand(self, global_env):
    params = self._preset.apply(self._raw_params)

    for key, value in params.items():
      self._expand_params(params, key, value, global_env)

    #
    # debug 設定の取得
    #
    self.debug = params.pop('_debug', False)

    #
    # enable 設定の取得
    #
    self.enable = params.pop('_enable', True)

    #
    # filter 設定の取得
    #
    resfilter = params.pop('resfilter', [])
    self.filter_list =  params.pop('outfilter', []) if not resfilter else resfilter
    if isinstance(self.filter_list, dict):
      self.filter_list = [self.filter_list]

    #
    # assert 設定の取得
    #
    self.assert_list = params.pop('assert', [])
    if isinstance(self.assert_list, util.basestring):
      self.assert_list = [self.assert_list]
    self.assertex_list = params.pop('assertex', [])
    if isinstance(self.assertex_list, util.basestring):
      self.assertex_list = [self.assertex_list]

    #
    # input 設定の取得
    #
    # instance method は "self" が付いてるので除く
    argspec = self._argspec
    argspec.args.pop(0)

    if "scenario" in argspec.args:
      params["scenario"] = global_env['scenario']
    if "global_env" in argspec.args:
      params["global_env"] = global_env

    self.params = util.filter_args(argspec, params)

    return self.params

  def _expand_params(self, parent, key, value, global_env):
    # 文字列の場合はテンプレートとして扱い、
    # 辞書、リストの場合はさらにその中の要素を展開する。
    # ここで指定していない数値等の型はそのまま
    if isinstance(value, util.basestring):
      # key に + が付いている場合は変数をそのまま代入する
      if isinstance(key, util.basestring) and key.startswith('+'):
        original_key = key.lstrip('+')
        result = template.expand_param({original_key: value}, global_env)
        parent[original_key] = result[original_key]
        del parent[key]
      else:
        parent[key] = template.expand(value, global_env)
    elif isinstance(value, dict):
      # see: scenarioloader.py
      # 辞書オブジェクトに勝手に __line__ が入ることによって挙動が変わることがあるので
      # 削除しておく
      if '__line__' in value:
        del value['__line__']
      for k, v in value.items():
        self._expand_params(value, k, v, global_env)
    elif isinstance(value, list):
      for k, v in enumerate(value):
        self._expand_params(value, k, v, global_env)

