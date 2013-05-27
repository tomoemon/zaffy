# -*- coding: utf-8 -*-
from baseaction import ActionException, ActionAssertionFailed
import time
import sys


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
    failed = False
    for scenario in self.aggregator:
      formatter.start(scenario)
      try:
        scenario.run(global_env)
        formatter.succeed()
      except ActionAssertionFailed as e:
        formatter.fail(self._encode(e))
        failed = True
      except ActionException as e:
        formatter.error(self._encode(e))
        failed = True
    formatter.end_test(time.time() - start_time)
    return failed

  def _encode(self, exception):
    root = exception.root
    if isinstance(root.original, OSError):
      root.stack_trace = root.stack_trace.decode(sys.getfilesystemencoding())
    return exception
