# -*- coding: utf-8 -*-


def is_ge(left_value, right_value):
  """ test `left_value` is ge (greater than equal) `right_value`

  `left_value` が `right_value` より大きいか等しいことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 200
       y: 100
       assert:
         - local.x is ge local.y
  """
  return left_value >= right_value

