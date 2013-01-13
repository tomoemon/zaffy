# -*- coding: utf-8 -*-
import time
import traceback
from template import assert_test, TemplateFormatException
from assertionfailed import AssertionFailed


class ActionException(Exception):
  def __init__(self, exception, stack_trace):
    self.original = exception
    self.stack_trace = stack_trace
    self.action_index = None


class BaseAction(object):

  def __init__(self, setting):
    self.result = {}
    self.exception = None
    self.start_time = None
    self.end_time = None
    self.setting = setting

  @property
  def res(self):
    """ self.result の alias """
    return self.result

  @property
  def params(self):
    return self.setting.params

  @classmethod
  def setup(cls, config):
    pass

  @classmethod
  def teardown(cls):
    pass

  def run_action(self, global_env):
    self.start_time = time.time()
    try:
      # 変数を jinja2 で展開する
      # const で定義する変数などアクション実行中に値が変わるものがあるので、直前じゃないとダメ
      self.setting.expand(global_env)
      self._run_dynamic_method(global_env)
    except ActionException as e:
      self.exception = e
    except Exception as e:
      self.exception = ActionException(e, traceback.format_exc())
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time

  def _run_dynamic_method(self, global_env):
    self.setting._method(**self.setting.params)

  def run_assert(self, global_env):
    try:
      self._test_assertex(global_env)
      self._test_assert(global_env)
    except TemplateFormatException as e:
      raise ActionException(e, traceback.format_exc())

  def _test_assertex(self, global_env):
    if not self.setting.assertex_list:
      if self.exception is not None:
        # assertexが設定されずに例外が起きた場合はそのまま上に投げる
        raise self.exception
      else:
        # assertexが設定されずに例外も起きない場合は何もしない
        return
    else:
      # assertex が設定されたが、例外が起きていない場合
      if self.exception is None:
        raise AssertionFailed("exception expected, but not raised",
            (self.setting.assertex_list,), 0)

    variables = dict(global_env)
    variables.update({
      "ex": self.exception.original,
      "this": self.__dict__
    })
    for assert_index, assert_str in enumerate(self.setting.assertex_list):
      try:
        assert_test(assert_str, variables)
      except AssertionFailed as e:
        e.assert_index = assert_index
        raise e

  def _test_assert(self, global_env):
    if not self.setting.assert_list:
      return

    variables = dict(global_env)
    variables.update({
      "res": self.result,
      "this": self.__dict__
    })
    for assert_index, assert_str in enumerate(self.setting.assert_list):
      try:
        assert_test(assert_str, variables)
      except AssertionFailed as e:
        e.assert_index = assert_index
        raise e

