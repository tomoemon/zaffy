# -*- coding: utf-8 -*-
from baseaction import ActionException, ActionAssertionFailed, ActionSimpleException
import time
import util
import chardet
import six


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
      except ActionSimpleException as e:
        formatter.error_simple(e)
        failed = True
      except ActionException as e:
        formatter.error(self._encode(e))
        failed = True
    formatter.end_test(time.time() - start_time)
    return failed

  def _encode(self, exception):
    root = exception.root
    if isinstance(root.original, EnvironmentError):
      root.stack_trace = util.unicode_os_string(root.stack_trace)
    elif not isinstance(root.stack_trace, six.text_type):
      encoding = chardet.detect(root.stack_trace)
      if encoding['confidence'] > 0.95:
        root.stack_trace = util.unicode(root.stack_trace, encoding['encoding'])
    return exception

