# -*- coding: utf-8 -*-


def is_eq(left_value, right_value):
  """ test `left_value` is eq (equal to) `right_value`

  `left_value` が `right_value` と等しいことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 100
       y: 100
       assert:
         - local.x is eq local.y
  """
  return left_value == right_value

