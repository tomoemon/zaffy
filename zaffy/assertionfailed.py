# -*- coding: utf-8 -*-

class AssertionFailed(Exception):
  def __init__(self, assertion_str, cmp_log_list, assert_index):
    self.assertion_str = assertion_str
    self.cmp_log_list = cmp_log_list
    self.assert_index = assert_index
    self.action_index = None

  def __str__(self):
    return repr(self.__dict__)

