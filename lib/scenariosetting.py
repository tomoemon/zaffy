# -*- coding: utf-8 -*-
import os
from os import path
import util


class ScenarioSetting(object):
  def __init__(self, filename="", body=""):
    self.filename = path.normcase(path.abspath(filename)) if filename else ""
    self.dir = os.path.dirname(self.filename)
    self.body = body

  def read(self):
    if self.filename:
      with util.open_yaml(self.filename) as fp:
        self.body = fp.read()
    return self.body

