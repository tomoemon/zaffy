# -*- coding: utf-8 -*-


def is_ne(left_value, right_value):
  """ test `left_value` is ne (not equal to) `right_value`

  `left_value` が `right_value` と等しくないことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 100
       y: 200
       assert:
         - local.x is ne local.y
         - local.x is not eq local.y
  """
  return left_value != right_value

