# -*- coding: utf-8 -*-
from jinja2 import Environment, TemplateSyntaxError
import jinja2
from assertexception import AssertFormatException

env = Environment(block_start_string='<%', block_end_string='%>',
    variable_start_string='<<', variable_end_string='>>')

def assert_test(template_str, variable_map):
  """
  >>> assert_test('hoge == "fuga"', {"hoge": "fuga"})
  True
  >>> assert_test('hoge == "fuga"', {"hoge": "piyo"})
  False
  """
  assert_str = '<% if ' + template_str + '%>true<% else %>false<% endif %>'
  try:
    if run_raw_template(assert_str, variable_map) == 'true':
      return True
    else:
      return False
  except TemplateSyntaxError:
    raise AssertFormatException(template_str)

def run_raw_template(template_str, variable_map):
  """
  >>> run_raw_template("<% if hoge == 10 %>true<% else %>false<% endif %>", {"hoge": 10})
  u'true'
  """
  template = env.from_string(template_str)
  return template.render(variable_map)

if __name__ == "__main__":
  import doctest
  doctest.testmod()
