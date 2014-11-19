# -*- coding: utf-8 -*-
import jinja2
from moduleloader import load_module_dir
from assertionfailed import AssertionFailed
import util

_env = jinja2.Environment(block_start_string='<%', block_end_string='%>',
                  variable_start_string='<<', variable_end_string='>>')

# referred by actions/env.py
Undefined = jinja2.Undefined

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
  failed = []

  def __init__(self, testfunc):
    self.testfunc = testfunc

  def __call__(self, *args):
    result = self.testfunc(*args)
    if not result:
      self.failed.append(args)
    return result


class TemplateFormatException(Exception):
  def __init__(self, original, template):
    super(TemplateFormatException, self).__init__(util.unicode(original))
    self.template = template


def assert_test(assertion, variable_map):
  """
  >>> assert_test('hoge == "fuga"', {"hoge": "fuga"})
  True
  >>> assert_test('hoge == "fuga"', {"hoge": "piyo"})
  False
  """
  CustomTest.failed = []

  try:
    result = _env.compile_expression(assertion)(**variable_map)
    if result != True:
      raise AssertionFailed(assertion, CustomTest.failed)
  except jinja2.TemplateSyntaxError as e:
    raise TemplateFormatException(e, assertion)
  except jinja2.UndefinedError as e:
    raise TemplateFormatException(e, assertion)


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
  except jinja2.TemplateSyntaxError as e:
    raise TemplateFormatException(e, template_str)
  except jinja2.UndefinedError as e:
    raise TemplateFormatException(e, template_str)


def expand_param(filter_dict, variable_map):
  result = {}
  for key, expression in filter_dict.items():
    try:
      result[key] = _env.compile_expression(expression)(**variable_map)
    except jinja2.TemplateSyntaxError as e:
      raise TemplateFormatException(e, "{0}: {1}".format(key, expression))
    except jinja2.UndefinedError as e:
      raise TemplateFormatException(e, "{0}: {1}".format(key, expression))
  return result

if __name__ == "__main__":
  import doctest
  doctest.testmod()
