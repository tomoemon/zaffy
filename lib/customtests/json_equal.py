# -*- coding: utf-8 -*-
import json
import util


def is_json_equal(left_value, right_value):
  """ test `left_value` is equal to `right_value` as json

  `left_value` と `right_value` が json として等しいことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: {"x":100,"y":200}
       y: {"y":200,"x":100}
       assert:
         - local.x is json_equal local.y
  """
  left_str = util.unicode(left_value)
  right_str = util.unicode(right_value)

  if left_str == right_str:
    return True

  try:
    left_json = json.loads(left_str)
    right_json = json.loads(right_str)
    return left_json == right_json
  except ValueError:
    return False

