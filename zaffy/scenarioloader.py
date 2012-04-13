# -*- coding: utf-8
from scenario import Scenario
from actionsetting import ActionSetting
from pprint import pprint

class ScenarioLoader(object):
  def __init__(self):
    pass

  def load_yaml():
    return yaml.load_all(file(sys.argv[1]))

  def create_action(raw_obj):
    if 'action' not in raw_obj:
      raise Exception("no action")
    action, method = raw_obj['action'].split(".")
    class_name = action.title()
    module = __import__("actions." + action, fromlist=[class_name])
    action_klass = getattr(module, class_name)
    inject_action_methods(action_klass)
    setting_obj = ActionSetting()
    setting_obj.set_params(raw_obj, action_klass.default_params)
    setting_obj.set_method(method)
    action_obj = action_klass(setting_obj)
    return action_obj

  def inject_action_methods(_action_klass):
    """ Action クラスに共通のメソッドを注入する """
    def __init__(self, setting):
      self.result = {}
      self.exception = None
      self.setting = setting

    def run(self):
      try:
        getattr(self, "do_" + self.setting.method)()
      except Exception as e:
        self.exception = e

    def has_assert(self):
      return bool(self.setting.assert_list)

    def has_assertex(self):
      return bool(self.setting.assertex_list)

    for name, func in locals().items():
      if not name.startswith('_') or name == '__init__':
        setattr(_action_klass, name, func)

  def create_actions(actions):
    result = []
    for action in actions:
      result.append(create_action(action))
    return result

