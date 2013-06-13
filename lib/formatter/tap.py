# -*- coding: utf-8 -*-
import util
import pprint


_u = lambda x: util.unicode(x, errors='replace')


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

  def finished(self):
    return self.succeeded + self.failed + self.errored

  def debug(self, debug_obj):
    if not isinstance(debug_obj, util.basestring):
      debug_obj = pprint.pformat(debug_obj, width=80, indent=2)
    debug_str = util.unescape_unicode(debug_obj)
    self.writer.debug(_i("  # ", _u(debug_str) + "\n"))

  def start(self, scenario):
    self.current = scenario

  def _write_header(self, succeeded, style):
    self.writer.write("{0} {1}".format(succeeded, self.finished()), {"type": style})
    self.writer.write(_i(" - ", _u("{0}").format(self.current.doc.doc.strip())), {"type": style})

  def succeed(self):
    self.succeeded += 1
    self._write_header('ok', "success")

  @staticmethod
  def _stacktrace(writer, exception):
    parent = exception
    indent = "  "
    arrow = ""
    while parent and hasattr(parent, 'original'):
      writer.write(_i(indent, _u(arrow + "filename: {0}").format(parent.scenario.setting.filename)))
      writer.write(_i(indent, _u(arrow + "action_index: {0} (line: {1})").format(parent.action_index, parent.line_number)))
      parent = parent.original
      indent += " "
      arrow = '-> '

  def fail(self, exception):
    """
    @param exception ActionAssertionFailed
    """
    writer = self.writer

    self.failed += 1
    self.not_ok_list.append(self.finished())
    self._write_header('not ok', "error")
    writer.write("  ------------------------------------------------------------\n")
    self._stacktrace(writer, exception)
    writer.write(_i("  ", _u("assert_index: {0}").format(exception.assert_index)))
    writer.write(_i("  ", _u("assertion: {0}").format(exception.assertion)))
    writer.write(_i("  ", _u("compared: ")))
    for i, items in enumerate(exception.compared):
      for j, item in enumerate(items):
        writer.write(_i("    ", _u("{0}-{1}: {2}").format(i, j, item)))
    writer.write("  ------------------------------------------------------------\n")

  def error(self, exception):
    """
    @param exception ActionException
    """
    writer = self.writer

    self.errored += 1
    self.not_ok_list.append(self.finished())
    self._write_header('not ok', "error")
    writer.write("  ------------------------------------------------------------\n")
    self._stacktrace(writer, exception)
    writer.write(_i("    ", "\n" + _u(exception.root.stack_trace).rstrip()))
    writer.write("  ------------------------------------------------------------\n")

  def error_simple(self, exception):
    """
    @param exception ActionSimpleException
    """
    e = exception
    e.root.stack_trace = e.root.original.__class__.__name__ + \
        ": " + _u(e.root.original) + "\n- " + _u(e.root.template)
    self.error(e)

  def start_test(self, test_count):
    writer = self.writer

    self.test_count = test_count
    writer.write("1..{0}\n".format(test_count))

  def end_test(self, elapsed_time):
    writer = self.writer
    test_count = self.test_count

    writer.write("\n")
    if self.not_ok_list:
      writer.write("FAILED tests {0}\n".format(
        ", ".join([_u(e) for e in self.not_ok_list])), {"type": "error_result"})
      writer.write("Failed {0}/{1} tests, {2:.2f}% ok ({3:.3f} sec)\n".format(
        len(self.not_ok_list), test_count,
        float(self.succeeded) / test_count * 100,
        elapsed_time), {"type": "error_result"})
    else:
      writer.write("{0} test{1} passed ({2:.3f} sec)\n".format(
        test_count, "" if test_count == 1 else "s all", elapsed_time),
        {"type": "success_result"})

