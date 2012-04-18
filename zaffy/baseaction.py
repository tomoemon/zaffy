# -*- coding: utf-8 -*-
import time
from comparator import wrap, CmpLog
from template import assert_test
from assertionfailed import AssertionFailed

class BaseAction(object):

  def __init__(self, setting):
    self.result = {}
    self.exception = None
    self.start_time = None
    self.end_time = None
    self.setting = setting
    self.cmp_log = CmpLog()

  def run_action(self, global_env):
    self.start_time = time.time()
    try:
      getattr(self, "do_" + self.setting.method)()
    except Exception as e:
      self.exception = e
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time

  def run_assert(self):
    self._test_assertex()
    self._test_assert()

  def _test_assertex(self):
    if not self.setting.assertex_list:
      if self.exception is not None:
        # assertexが設定されずに例外が起きた場合はそのまま上に投げる
        raise self.exception
      else:
        # assertexが設定されずに例外も起きない場合は何もしない
        return
    elif self.exception is None:

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

