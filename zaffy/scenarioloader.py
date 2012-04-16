# -*- coding: utf-8
import time
import yaml
from scenario import Scenario
from actionsetting import ActionSetting
from comparator import wrap, CmpLog
from template import assert_test
from assertionfailed import AssertionFailed

class ScenarioLoader(object):

  def load(self, filename):
    yaml_obj = list(self.load_yaml(filename))
    first_doc = yaml_obj[0]
    raw_actions = first_doc['actions']
    return Scenario(self.create_actions(raw_actions))

  def load_yaml(self, filename):
    print filename
    return yaml.load_all(file(filename))

  def create_action(self, raw_obj):
    if 'action' not in raw_obj:
      raise Exception("no action")
    action, method = raw_obj['action'].split(".")
    class_name = action.title()
    module = __import__("actions." + action, fromlist=[class_name])
    action_klass = getattr(module, class_name)
    ActionMethodsInjector.inject(action_klass)
    setting_obj = ActionSetting()
    setting_obj.set_params(raw_obj, action_klass.default_params)
    setting_obj.set_method(method)
    action_obj = action_klass(setting_obj)
    return action_obj

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(self.create_action(action))
    return result

class ActionMethodsInjector(object):

  @classmethod
  def inject(cls, action_klass):
    """ Action クラスに共通のメソッドを注入する """
    for name, method in cls.target_methods.items():
      setattr(action_klass, name, method)

  def __init__(self, setting):
    self.result = {}
    self.exception = None
    self.start_time = None
    self.end_time = None
    self.setting = setting
    self.cmp_log = CmpLog()

  def _run(self, global_env):
    self.start_time = time.time()
    try:
      getattr(self, "do_" + self.setting.method)()
    except Exception as e:
      self.exception = wrap(e, self.cmp_log)
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time
      self.result = wrap(self.result, self.cmp_log)

  def _assert(self):
    self._test_assertex()
    self._test_assert()

  def _test_assertex(self):
    if not self.setting.assertex_list:
      if self.exception is not None:
        raise self.exception._value
      else:
        return

    variables = {"ex": self.exception, "this": self.__dict__}
    for assert_index, assert_str in enumerate(self.setting.assertex_list):
      if not assert_test(assert_str, variables):
        raise AssertionFailed(assert_str,
            self.exception._cmp_log.log_list if self.exception is not None else [{"got": "exception not exists", "expect": "Exception"}],
            assert_index)

  def _test_assert(self):
    if not self.setting.assert_list:
      return
    variables = {"res": self.result, "this": self.__dict__}
    for assert_index, assert_str in enumerate(self.setting.assert_list):
      if not assert_test(assert_str, variables):
        raise AssertionFailed(assert_str,
            self.cmp_log.log_list,
            assert_index)

  target_methods = {
     "__init__":__init__,
     "_run": _run,
     "_assert": _assert,
     "_test_assert": _test_assert,
     "_test_assertex": _test_assertex
  }

