# -*- coding: utf-8 -*-
from baseaction import ActionException
from assertionfailed import AssertionFailed
import time

class ScenarioRunner(object):
  def __init__(self, aggregator, formatter):
    """ init ScenarioRunner
    @param aggregator Aggregator
    @param formatter Formatter
    """
    self.aggregator = aggregator
    self.formatter = formatter

  def run(self, global_env):
    start_time = time.time()
    formatter = self.formatter
    formatter.start_test(len(self.aggregator))
    for scenario in self.aggregator:
      formatter.start(scenario)
      try:
        scenario.run(global_env)
        formatter.succeed()
      except ActionException as e:
        formatter.error(e)
      except AssertionFailed as e:
        formatter.fail(e)
    formatter.end_test(time.time() - start_time)

