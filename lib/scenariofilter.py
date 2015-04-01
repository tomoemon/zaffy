# -*- coding: utf-8 -*-


class Filter(object):
  def is_valid(self, scenario_object):
    return True


class TagFilter(object):
  def __init__(self, include):
    self.include = include

  def is_valid(self, scenario_object):
    if not self.include:
      return True

    if set(scenario_object.header.tags) & set(self.include):
      return True

    return False

