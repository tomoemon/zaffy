# -*- coding: utf-8 -*-


def is_lt(left_value, right_value):
  """ test `left_value` is le (less than) `right_value`

  `left_value` が `right_value` より小さいことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 100
       y: 200
       assert:
         - local.x is lt local.y
  """
  return left_value < right_value

