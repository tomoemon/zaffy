# -*- coding: utf-8 -*-
from jinja2 import Environment, TemplateSyntaxError
import jinja2
from pprint import pprint
from load_module import load_module_dir

env = Environment(block_start_string='<%', block_end_string='%>',
    variable_start_string='<<', variable_end_string='>>')

def add_plugin(plugin_dict, custom_plugin_dir, prefix=""):
  plugins = load_module_dir(custom_plugin_dir)
  for module in plugins:
    name_list = [name for name in dir(module) if name.startswith(prefix) and len(name) > len(prefix)]
    for name in name_list:
      obj = getattr(module, name)
      if callable(obj):
        name = name[len(prefix):]
        if name in plugin_dict:
          raise Exception(name + " is already defined")
        plugin_dict[name] = obj

add_plugin(env.tests, "customtests", "is_")
add_plugin(env.filters, "customfilters")

class AssertFormatException(Exception):
  pass

def assert_test(template_str, variable_map):
  """
  >>> assert_test('hoge == "fuga"', {"hoge": "fuga"})
  True
  >>> assert_test('hoge == "fuga"', {"hoge": "piyo"})
  False
  """
  # assert 文の中で if の制御構造を破壊されないように
  template_str = template_str.replace('<%','').replace('%>','')

  assert_str = '<% if ' + unicode(template_str) + ' %>1<% else %>0<% endif %>'
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

if __name__ == "__main__":
  import doctest
  doctest.testmod()
