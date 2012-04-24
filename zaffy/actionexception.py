# -*- coding: utf-8 -*-

class ActionException(Exception):
  def __init__(self, exception, stack_trace):
    self.original = exception
    self.stack_trace = stack_trace

