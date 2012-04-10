# -*- coding: utf-8 -*-

import json

def is_json_equal(left_value, right_value):
  return json.loads(left_value) == json.loads(right_value)

