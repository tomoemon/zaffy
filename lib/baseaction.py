# -*- coding: utf-8 -*-
import time
import traceback
import template
from assertionfailed import AssertionFailed
import util


class ActionException(Exception):
  def __init__(self, exception, stack_trace, line_number):
    self.original = exception
    self.stack_trace = stack_trace
    self.action_index = None
    self.scenario = None
    self.line_number = line_number

  @property
  def root(self):
    instance = self
    while isinstance(instance.original, ActionException):
      instance = instance.original
    return instance

  def __getattr__(self, key):
    return getattr(self.original, key)


class ActionAssertionFailed(ActionException):
  def __init__(self, exception, stack_trace, line_number):
    super(ActionAssertionFailed, self).__init__(exception, stack_trace, line_number)


class BaseAction(object):

  def __init__(self, setting, params_obj):
    self.result = {}
    self.exception = None
    self.start_time = None
    self.end_time = None
    self.params = None
    self._params = params_obj
    self._setting = setting

  @property
  def res(self):
    """ self.result の alias """
    return self.result

  @property
  def line_number(self):
    return self._setting.line_number

  @classmethod
  def setup(cls, config):
    pass

  @classmethod
  def load_module(cls):
    # modules, errors
    return ((), None)

  @classmethod
  def teardown(cls):
    pass

  def run_action(self, global_env):
    self.start_time = time.time()
    try:
      # 変数を jinja2 で展開する
      # local 変数などアクション実行中に値が変わるものがあるので直前にやる必要がある
      self.params = self._params.expand(global_env)
      self._run()
      self._filter(global_env)
    except ActionAssertionFailed as e:
      self.exception = ActionAssertionFailed(e, traceback.format_exc(), self.line_number)
    except Exception as e:
      # 別シナリオを require して実行中に例外が起きた場合は ActionException が飛んでくる
      # このシナリオにおける line_number を記録する（あとで表示する）必要があるので、
      # 再度 wrap する
      self.exception = ActionException(e, traceback.format_exc(), self.line_number)
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time

    self._assert(global_env)

  def _run(self):
    method = getattr(self, "do_" + self._setting.method_name)
    method(**self.params)

  def _filter(self, global_env):
    variables = dict(global_env)
    variables.update({
      "res": self.result,
      "this": self.__dict__
    })
    for filter_dict in self._params.filter_list:
      self.result.update(template.expand_param(filter_dict, variables))

  def debug_print(self, printer):
    debug = self._params.debug

    if not debug:
      return

    if debug == True:
      debug = ["params", "res"]

    if isinstance(debug, util.basestring):
      debug_dict = {debug: debug}
    elif isinstance(debug, list):
      debug_dict = dict([(k, k) for k in debug])
    elif isinstance(debug, dict):
      debug_dict = debug
    else:
      debug_dict = {util.unicode(debug): util.unicode(debug)}

    variables = {}
    variables.update({
      "params": self.params,
      "res": self.result,
      "this": self.__dict__
    })
    try:
      result = template.expand_param(debug_dict, variables)
      printer.write(result)
    except Exception as e:
      printer.write({"error": util.unicode(e)})

  def _assert(self, global_env):
    try:
      self._test_assertex(global_env)
      self._test_assert(global_env)
    except AssertionFailed as e:
      raise ActionAssertionFailed(e, traceback.format_exc(), self.line_number)
    except ActionException as e:
      raise
    except Exception as e:
      raise ActionException(e, traceback.format_exc(), self.line_number)

  def _test_assertex(self, global_env):
    if not self._params.assertex_list:
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
            (self._params.assertex_list,), 0)

    variables = dict(global_env)
    variables.update({
      "ex": self.exception.original,
      "this": self.__dict__
    })
    for assert_index, assert_str in enumerate(self._params.assertex_list):
      try:
        template.assert_test(assert_str, variables)
      except AssertionFailed as e:
        e.assert_index = assert_index
        raise

  def _test_assert(self, global_env):
    if not self._params.assert_list:
      return

    variables = dict(global_env)
    variables.update({
      "res": self.result,
      "this": self.__dict__
    })
    for assert_index, assert_str in enumerate(self._params.assert_list):
      try:
        template.assert_test(assert_str, variables)
      except AssertionFailed as e:
        e.assert_index = assert_index
        raise

