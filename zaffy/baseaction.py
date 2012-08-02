# -*- coding: utf-8 -*-
import time
import traceback
from comparator import wrap, CmpLog
from template import assert_test
from assertionfailed import AssertionFailed
from actionexception import ActionException

class BaseAction(object):

  def __init__(self, setting):
    self.result = {}
    self.exception = None
    self.start_time = None
    self.end_time = None
    self.setting = setting
    self.cmp_log = CmpLog()

  @property
  def res(self):
    """ self.result の alias """
    return self.result

  @property
  def params(self):
    return self.setting.params

  @classmethod
  def apply_config(cls, config):
    pass

  def run_action(self, global_env, scenario):
    # 変数を jinja2 で展開する
    # const で定義する変数などアクション実行中に値が変わるものがあるので、直前じゃないとダメ
    self.setting.expand(global_env)
    self.start_time = time.time()
    try:
      self._run_dynamic_method(global_env, scenario)
    except ActionException as e:
      self.exception = e
    except Exception as e:
      self.exception = ActionException(e, traceback.format_exc())
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time

  def _run_dynamic_method(self, global_env, scenario):
    getattr(self, "do_" + self.setting._method)(self.params)

  def run_assert(self, global_env):
    self._test_assertex(global_env)
    self._test_assert(global_env)

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
        raise AssertionFailed("Exception not raised",
            [{"got": "exception not exists", "expect": "Exception"}],
            0)

    wrap_exception = wrap(self.exception.original, self.cmp_log)
    variables = dict(global_env)
    variables.update({
      "ex": wrap_exception,
      "this": wrap(self.__dict__, self.cmp_log)})
    for assert_index, assert_str in enumerate(self.setting.assertex_list):
      self.cmp_log.clear()
      if not assert_test(assert_str, variables):
        raise AssertionFailed(assert_str,
            self.cmp_log.log_list,
            assert_index)

  def _test_assert(self, global_env):
    if not self.setting.assert_list:
      return
    variables = dict(global_env)
    variables.update({
      "res": wrap(self.result, self.cmp_log),
      "this": wrap(self.__dict__, self.cmp_log)})
    for assert_index, assert_str in enumerate(self.setting.assert_list):
      self.cmp_log.clear()
      if not assert_test(assert_str, variables):
        raise AssertionFailed(assert_str,
            self.cmp_log.log_list,
            assert_index)

