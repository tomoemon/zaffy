# -*- coding: utf-8 -*-
from actionsetting import ActionSetting
from baseaction import BaseAction
from moduleloader import load_module_dir
from actionparams import ActionParams


class InvalidActionException(Exception):
  pass


class ActionLoader(object):

  def __init__(self):
    self.action_klasses = {}

  def create_action(self, raw_obj):
    try:
      setting = ActionSetting(raw_obj)
      preset = self.get_action_klass('preset').get_applier(
        setting.action_name, setting.preset_name, setting.is_merge_preset
      )
      action_klass = self.get_action_klass(setting.action_name)
      param_obj = ActionParams(
          setting,
          action_klass,
          preset
      )
    except Exception as e:
      raise InvalidActionException(str(e))
    return action_klass(setting, param_obj)

  def load_actions(self):
    module_list, error = load_module_dir("actions")
    for module in module_list:
      # action に使いたいモジュール名がすでに使われている場合にprefixに "_" を付ける
      module_name = module.__name__.lstrip('_')
      action_klass = getattr(module, module_name.title())
      if not issubclass(action_klass, BaseAction):
        # BaseAction クラスを継承していないクラスがあったらエラー
        raise Exception(module_name.title() + " class must extend BaseAction")
      modules, errors = type.__getattribute__(action_klass, 'load_module')()
      if errors:
        error.extend(errors)
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
