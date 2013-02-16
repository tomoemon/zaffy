# -*- coding: utf-8 -*-
from jinja2 import Environment, TemplateSyntaxError, UndefinedError
from moduleloader import load_module_dir
from assertionfailed import AssertionFailed
import util

_env = Environment(block_start_string='<%', block_end_string='%>',
                  variable_start_string='<<', variable_end_string='>>')


def load_plugin(plugin_dict, custom_plugin_dir, prefix=""):
  plugins, load_error = load_module_dir(custom_plugin_dir)
  for module in plugins:
    name_list = [name for name in dir(module) if name.startswith(prefix) and len(name) > len(prefix)]
    overridable = getattr(module, prefix + "override", [])
    for name in name_list:
      obj = getattr(module, name)
      if callable(obj):
        plugin_name = name[len(prefix):]
        if plugin_name in plugin_dict and name not in overridable:
          raise Exception(name + " is already defined")
        plugin_dict[plugin_name] = obj
  return load_error


def load_customtests():
  load_error = load_plugin(_env.tests, "customtests", "is_")
  for name, testfunc in _env.tests.items():
    _env.tests[name] = CustomTest(testfunc)
  if load_error:
    raise load_error


def load_customfilters():
  load_error = load_plugin(_env.filters, "customfilters", "do_")
  if load_error:
    raise load_error


class CustomTest(object):
  test_index = 0
  failed = {}

  def __init__(self, testfunc):
    self.testfunc = testfunc

  def __call__(self, *args):
    result = self.testfunc(*args)
    if not result:
      self.failed.setdefault(self.test_index, []).append(args)
    return result

  @classmethod
  def start_test(cls, test_index):
    cls.test_index = test_index
    return ""

  @classmethod
  def reset(cls):
    cls.test_index = 0
    cls.failed = {}


class TemplateFormatException(Exception):
  pass


class AssertFormatException(TemplateFormatException):
  pass


def assert_all(assertions, variable_map):
  CustomTest.reset()

  assert_list = []
  param_set_list = []
  for index, assertion in enumerate(assertions):
    if isinstance(assertion, dict):
      for key, value in assertion.items():
        param_set_list.append((key, value))
    else:
      assert_list.append((index, assertion))

  template_list = []
  template_list.append(
      # TODO: escape value
      "".join(["<% set {0} = {1} %>".format(key, value) for key, value in param_set_list])
  )
  template_list.extend(
      ["<<__CustomTest__.start_test({2})>><% if {0} %><% else %>{1}<% endif %>".format(assertion, index, index) for index, assertion in assert_list]
  )

  variable_map["__CustomTest__"] = CustomTest

  try:
    template = "\n".join(template_list)
    result = run_raw_template(template, variable_map)
    result_lines = result.split("\n")[1:]
    for assert_result in result_lines:
      if assert_result:
        assert_index = int(assert_result)
        raise AssertionFailed(assertions[assert_index], CustomTest.failed.get(assert_index, {}), assert_index)
  except TemplateSyntaxError as e:
    assert_str = "\n".join(["  " + str(a) for a in assertions])
    raise AssertFormatException(util.unicode(e) + "\n" + assert_str)
  except UndefinedError as e:
    assert_str = "\n".join(["  " + str(a) for a in assertions])
    raise AssertFormatException(util.unicode(e) + "\n" + assert_str)


def run_raw_template(template_str, variable_map):
  """
  >>> run_raw_template("<% if hoge.x == 10 %>true<% else %>false<% endif %>", {"hoge": {"x":10}})
  u'true'
  """
  template = _env.from_string(template_str)
  return template.render(variable_map)


def expand(template_str, variable_map):
  try:
    return run_raw_template(template_str, variable_map)
  except TemplateSyntaxError as e:
    raise TemplateFormatException(util.unicode(e) + "\n" + template_str)
  except UndefinedError as e:
    raise TemplateFormatException(util.unicode(e) + "\n" + template_str)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
