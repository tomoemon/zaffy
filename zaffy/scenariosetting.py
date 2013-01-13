# -*- coding: utf-8 -*-
import os
from os import path


class ScenarioSetting(object):
  def __init__(self, filename="", body=""):
    self.filename = path.normcase(path.abspath(filename))
    self.dir = os.path.dirname(self.filename)
    self.body = body

  def read(self):
    if self.filename and os.access(self.filename, os.R_OK):
      with open(self.filename) as fp:
        self.body = fp.read()
    return self.body

