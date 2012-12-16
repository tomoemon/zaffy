# -*- coding: utf-8 -*-
import os

class ScenarioSetting(object):
  def __init__(self, doc="", filename=""):
    self.doc = doc
    self.filename = filename
    self.dir = os.path.dirname(self.filename)
    self.from_scenario = None

