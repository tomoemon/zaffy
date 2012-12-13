# -*- coding: utf-8 -*-

class AssertionFailed(AssertionError):
  def __init__(self, assertion_str, compared_list, assert_index=None, action_index=None):
    self.assertion = assertion_str
    self.compared = compared_list
    self.assert_index = assert_index
    self.action_index = action_index

  def __str__(self):
    return repr(self.__dict__)

