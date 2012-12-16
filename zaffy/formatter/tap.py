# -*- coding: utf-8 -*-
import pprint
import datetime

def _i(prefix, output_string, postfix="\n"):
  """ 行先頭に "ok" 等の文字が出力されないようにフォーマットする
  """
  return "\n".join([prefix + line for line in output_string.split("\n")]) + "\n"

class Tap(object):
  def __init__(self, writer):
    self.writer = writer
    self.test_count = 0
    self.succeeded = 0
    self.failed = 0
    self.errored = 0
    self.not_ok_list = []
    self.current = None

  def total_elapsed(self):
    return self.succeeded + self.failed + self.errored

  def debug(self, params):
    writer = self.writer

    var_str = pprint.pformat(params, width=80, indent=2)
    writer.write("\n")
    writer.write(_i("  # ", "DEBUG at {0}".format(datetime.datetime.now())))
    writer.write(_i("  # ", var_str))

  def start(self, scenario):
    self.current = scenario

  def succeed(self):
    writer = self.writer

    self.succeeded += 1
    writer.write("ok {0} - {1}\n".format(
      self.total_elapsed(), self.current.setting.doc))

  def fail(self, exception):
    """
    @param exception AssertionFailed
    """
    writer = self.writer

    self.failed += 1
    self.not_ok_list.append(self.total_elapsed())
    writer.write("not ok {0} - {1}\n".format(
      self.total_elapsed(), self.current.setting.doc))
    writer.write("  ------------------------------------------------------------\n")
    writer.write(_i("  ", "filename: {0}".format(self.current.setting.filename)))
    writer.write(_i("  ", "action_index: {0}".format(exception.action_index)))
    writer.write(_i("  ", "assert_index: {0}".format(exception.assert_index)))
    writer.write(_i("  ", "assertion: {0}".format(exception.assertion)))
    writer.write(_i("  ", "compared: "))
    for i, items in enumerate(exception.compared):
      for j, item in enumerate(items):
        writer.write(_i(u"    ", "{0}-{1}: {2}".format(i, j, item)))
    writer.write("  ------------------------------------------------------------\n")

  def error(self, exception):
    """
    @param exception ActionException
    """
    writer = self.writer

    self.errored += 1
    self.not_ok_list.append(self.total_elapsed())
    writer.write("not ok {0} - {1}\n".format(
      self.total_elapsed(), self.current.setting.doc))
    writer.write("  ------------------------------------------------------------\n")
    writer.write(_i("  ", "filename: {0}".format(self.current.setting.filename)))
    writer.write(_i("  ", "action_index: {0}".format(exception.action_index)))
    writer.write(_i("  ", "{0}: {1}".format(
      exception.original.__class__.__name__, str(exception.original))))
    writer.write("  ------------------------------------------------------------\n")

  def start_test(self, test_count):
    writer = self.writer

    self.test_count = test_count
    writer.write("1..{0}\n".format(test_count))

  def end_test(self, elapsed_time):
    writer = self.writer

    writer.write("\n")
    if self.not_ok_list:
      writer.write("FAILED tests {0}\n".format(
        ", ".join([str(e) for e in self.not_ok_list])))
      writer.write("Failed {0}/{1} tests, {2:.2f}% ok ({0:.2f} sec elapsed)\n".format(
        len(self.not_ok_list), self.test_count,
        float(self.succeeded) / self.test_count * 100,
        elapsed_time))
    else:
      if self.test_count == 1:
        writer.write("1 test succeeded ({0:.2f} sec elapsed)\n".format(
          self.test_count, elapsed_time))
      else:
        writer.write("{0} tests all succeeded ({0:.2f} sec elapsed)\n".format(
          self.test_count, elapsed_time))

