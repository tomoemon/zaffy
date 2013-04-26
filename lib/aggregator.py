# -*- coding: utf-8 -*-
import sys
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting


class Aggregator(object):
  def __init__(self):
    self.scenario_list = []
    self.filter = []

  def add_filter(self, filter):
    self.filter.append(filter)

  def add(self, scenario):
    self.scenario_list.append(scenario)

  def add_files(self, file_list):
    filter = self.filter
    for target in file_list:
      scenario = scenario_loader.load(ScenarioSetting(filename=target))
      if self.is_valid(scenario):
        self.add(scenario)

  def is_valid(self, scenario):
    for f in self.filter:
      if not f.is_valid(scenario):
        return False
    return True

  def __iter__(self):
    for scenario in self.scenario_list:
      yield scenario

  def __len__(self):
    return len(self.scenario_list)

