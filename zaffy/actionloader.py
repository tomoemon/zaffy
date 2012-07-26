# -*- coding: utf-8 -*-
from actionsetting import ActionSetting
from moduleloader import load_module_dir
from actionparamsetting import ActionParams

class ActionLoader(object):
  def __init__(self):
    self.action_klasses = {}

  def create_action(self, raw_obj):
    if 'action' not in raw_obj or not raw_obj['action']:
      raise Exception("no action")
    action_preset = raw_obj['action'].split("<")
    if len(action_preset) == 1:
      preset_name = "default"
    else:
      preset_name = action_preset[1].strip()

    action_info = action_preset[0].split(".")
    action_name = action_info[0]

    # action: require
    # のように . 付きでメソッドを明示しない場合は
    # メソッド名はアクションと同じになる
    if len(action_info) == 2 and action_info[1]:
      method = action_info[1]
    else:
      method = action_name

    action_klass = self.get_action_klass(action_name)
    setting_obj = ActionSetting()
    del raw_obj['action']
    setting_obj.set_params(ActionParams(
      param_setting=action_klass.param_setting,
      raw_params=raw_obj,
      preset=self.get_action_klass('preset').get_applier(action_name, preset_name, False)
      ))
    setting_obj.set_method(method)
    action_obj = action_klass(setting_obj)
    return action_obj

  def load_actions(self):
    module_list = load_module_dir("actions")
    for module in module_list:
      module_name = module.__name__
      self.action_klasses[module_name] = getattr(module, module_name.title())

  def get_all_action_map(self):
    return self.action_klasses

  def get_action_klass(self, action_name):
    if action_name in self.action_klasses:
      return self.action_klasses[action_name]
    raise Exception("No such action: " + action_name)

action_loader = ActionLoader()
