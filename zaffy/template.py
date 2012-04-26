# -*- coding: utf-8 -*-
from jinja2 import Environment, TemplateSyntaxError
from moduleloader import load_module_dir
from comparator import wrap_func, wrap_test_func
import types

env = Environment(block_start_string='<%', block_end_string='%>',
    variable_start_string='<<', variable_end_string='>>')

def add_plugin(plugin_dict, custom_plugin_dir, prefix=""):
  plugins = load_module_dir(custom_plugin_dir)
  other_info_list = []
  for module in plugins:
    name_list = [name for name in dir(module) if name.startswith(prefix) and len(name) > len(prefix)]
    overridable = getattr(module, prefix + "override", [])
    for name in name_list:
      info = {}
      obj = getattr(module, name)
      if callable(obj):
        plugin_name = name[len(prefix):]
        if plugin_name in plugin_dict and name not in overridable:
          raise Exception(name + " is already defined")
        plugin_dict[plugin_name] = obj
      else:
        info[name] = obj
    other_info_list.append(info)
  return other_info_list

info_list = add_plugin(env.tests, "customtests", "is_")
normal_tests = dict(env.tests)
assert_tests = dict(env.tests)
for info in info_list:
  func_list = info.get("is_tocmp_on_asserting", [])
  for values in func_list:
    name = values[0]
    func = normal_tests[name]
    index = values[1]
    assert_tests[name] = wrap_test_func(func, index)

info_list = add_plugin(env.filters, "customfilters", "do_")
normal_filters = dict(env.filters)
assert_filters = dict(env.filters)
for info in info_list:
  func_list = info.get("do_tocmp_on_asserting", [])
  for values in func_list:
    name = values[0]
    if isinstance(values[1], types.FunctionType):
      func = values[1]
      index = 0
    else:
      func = normal_filters[name]
      index = values[1]
    assert_filters[name] = wrap_func(func, index)

class AssertFormatException(Exception):
  pass

def assert_test(template_str, variable_map):
  """
  >>> assert_test('hoge == "fuga"', {"hoge": "fuga"})
  True
  >>> assert_test('hoge == "fuga"', {"hoge": "piyo"})
  False
  """
  global env
  env.filters = assert_filters
  env.tests = assert_tests
  template_str = unicode(template_str)
  # assert 文の中で if の制御構造を破壊されないように
  template_str = template_str.replace('<%','').replace('%>','')

  assert_str = '<% if ' + template_str + ' %>1<% else %>0<% endif %>'
  try:
    result = run_raw_template(assert_str, variable_map)
    if result == '1':
      return True
    else:
      return False
  except TemplateSyntaxError:
    raise AssertFormatException(template_str)

def run_raw_template(template_str, variable_map):
  """
  >>> run_raw_template("<% if hoge.x == 10 %>true<% else %>false<% endif %>", {"hoge": {"x":10}})
  u'true'
  """
  template = env.from_string(template_str)
  return template.render(variable_map)

def expand(template_str, variable_map):
  global env
  env.filters = normal_filters
  env.tests = normal_tests
  return run_raw_template(template_str, variable_map)

if __name__ == "__main__":
  import doctest
  doctest.testmod()
