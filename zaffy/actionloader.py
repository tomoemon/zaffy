# -*- coding: utf-8 -*-
from actionsetting import ActionSetting
from moduleloader import load_module_dir
from actionparamsetting import ActionParams
import re

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
    setting_obj = ActionSetting()
    del raw_obj['action']
    setting_obj.set_params(ActionParams(
      param_setting=action_klass.param_setting,
      raw_params=raw_obj,
      preset=self.get_action_klass('preset').get_applier(action_name, preset_name, False)
      ))
    setting_obj.set_method(method_name)
    action_obj = action_klass(setting_obj)
    return action_obj

  def parse_action_id(self, raw_action_id):
    match = self.ACTION_REGEX.match(raw_action_id)
    if match is None:
      raise Exception("Invalid action: '" + raw_action_id + "'")
    return match.groupdict()

  def load_actions(self):
    module_list = load_module_dir("actions")
    for module in module_list:
      module_name = module.__name__
      action_klass = getattr(module, module_name.title())
      if not hasattr(action_klass, "param_setting"):
        raise Exception("actions." + module_name.title()
            + " class should have static property 'param_setting'")
      self.action_klasses[module_name] = action_klass

  def get_all_action_map(self):
    return self.action_klasses

  def get_action_klass(self, action_name):
    if action_name in self.action_klasses:
      return self.action_klasses[action_name]
    raise Exception("No such action: " + action_name)

action_loader = ActionLoader()
