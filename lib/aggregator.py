# -*- coding: utf-8 -*-
import sys
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting


class Aggregator(object):
  def __init__(self):
    self.scenario_list = []

  def add(self, scenario):
    self.scenario_list.append(scenario)

  def add_files(self, file_list):
    for target in file_list:
      try:
        scenario = scenario_loader.load(ScenarioSetting(filename=target))
      except Exception as e:
        sys.stderr.write("Loading scenario failed: " + target + "\n\n")
        raise
      self.add(scenario)

  def __iter__(self):
    for scenario in self.scenario_list:
      yield scenario

  def __len__(self):
    return len(self.scenario_list)

