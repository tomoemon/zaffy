# -*- coding: utf-8 -*-
from actionsetting import ActionSetting
from baseaction import BaseAction
from moduleloader import load_module_dir
from actionparams import ActionParams
import re
import inspect


class ActionLoader(object):
  ACTION_REGEX = re.compile(r'(?P<actionName>\w+)(?:\.(?P<methodName>\w+))?(?:\s*\<\s*(?P<presetName>\w+))?')

  def __init__(self):
    self.action_klasses = {}

  def create_action(self, raw_obj):
    if 'action' not in raw_obj or not raw_obj['action']:
      raise Exception("No action")

    match_dict = self.parse_action_id(raw_obj['action'])
    action_name = match_dict['actionName']
    method_name = match_dict['methodName']
    preset_name = match_dict['presetName']

    # action: http.get
    # の場合は http アクションの get メソッドを呼ぶ
    # action: require
    # のように . 付きでメソッドを明示しない場合は
    # メソッド名はアクションと同じになる
    if not method_name:
      method_name = action_name

    action_klass = self.get_action_klass(action_name)
    del raw_obj['action']
    setting_obj = ActionSetting()
    action_obj = action_klass(setting_obj)
    method_obj = getattr(action_obj, "do_" + method_name)
    setting_obj.set_params(ActionParams(
      argspec=inspect.getargspec(method_obj),
      raw_params=raw_obj,
      preset=self.get_action_klass('preset').get_applier(action_name, preset_name, False)
    ))
    setting_obj.set_method(method_obj)
    return action_obj

  def parse_action_id(self, raw_action_id):
    match = self.ACTION_REGEX.match(raw_action_id)
    if match is None:
      raise Exception("Invalid action: '" + raw_action_id + "'")
    return match.groupdict()

  def load_actions(self):
    module_list, error = load_module_dir("actions")
    for module in module_list:
      # action に使いたいモジュール名がすでに使われている場合にprefixに "_" を付ける
      module_name = module.__name__.lstrip('_')
      action_klass = getattr(module, module_name.title())
      if not issubclass(action_klass, BaseAction):
        # BaseAction クラスを継承していないクラスがあったらエラー
        raise Exception(module_name.title() + " class must extend BaseAction")
      self.action_klasses[module_name] = action_klass

    if error:
      raise error

  def get_all_action_map(self):
    return self.action_klasses

  def get_action_klass(self, action_name):
    if action_name in self.action_klasses:
      return self.action_klasses[action_name]
    raise Exception("No such action: " + action_name)

action_loader = ActionLoader()
