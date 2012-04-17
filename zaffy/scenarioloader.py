# -*- coding: utf-8
import time
import yaml
from scenario import Scenario
from actionsetting import ActionSetting
from comparator import wrap, CmpLog
from template import assert_test
from assertionfailed import AssertionFailed

action_klass_memo = {}

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
    action_name, method = raw_obj['action'].split(".")
    action_klass = self.get_action_klass(action_name)
    setting_obj = ActionSetting()
    setting_obj.set_params(raw_obj, action_klass.default_params)
    setting_obj.set_method(method)
    action_obj = action_klass(setting_obj)
    return action_obj

  def get_action_klass(self, action_name):
    global action_klass_memo
    class_name = action_name.title()
    if class_name in action_klass_memo:
      action_klass = action_klass_memo[class_name]
    else:
      module = __import__("actions." + action_name, fromlist=[class_name])
      action_klass = getattr(module, class_name)
      ActionMethodsInjector.inject(action_klass)
      action_klass_memo[class_name] = action_klass
    return action_klass

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
      self.exception = e
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time

  def _assert(self):
    self._test_assertex()
    self._test_assert()

  def _test_assertex(self):
    if not self.setting.assertex_list:
      if self.exception is not None:
        raise self.exception
      else:
        return

    wrap_exception = wrap(self.exception, self.cmp_log)
    variables = {"ex": wrap_exception, "this": wrap(self.__dict__, self.cmp_log)}
    for assert_index, assert_str in enumerate(self.setting.assertex_list):
      self.cmp_log.clear()
      if not assert_test(assert_str, variables):
        raise AssertionFailed(assert_str,
            self.cmp_log.log_list if self.exception is not None else [{"got": "exception not exists", "expect": "Exception"}],
            assert_index)

  def _test_assert(self):
    if not self.setting.assert_list:
      return
    variables = {"res": wrap(self.result, self.cmp_log), "this": wrap(self.__dict__, self.cmp_log)}
    for assert_index, assert_str in enumerate(self.setting.assert_list):
      self.cmp_log.clear()
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

