# -*- coding: utf-8 -*-
from scenarioloader import scenario_loader

class Aggregator(object):
  def __init__(self):
    self.scenario_list = []

  def add(self, scenario):
    self.scenario_list.append(scenario)

  def add_files(self, file_list):
    for target in file_list:
        scenario = scenario_loader.load_file(target)
        self.add(scenario)

  def __iter__(self):
    for scenario in self.scenario_list:
      yield scenario

  def __len__(self):
    return len(self.scenario_list)

