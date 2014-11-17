# -*- coding: utf-8 -*-


def is_le(left_value, right_value):
  """ test `left_value` is le (less than equal) `right_value`

  `left_value` が `right_value` より小さいか等しいことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 100
       y: 200
       assert:
         - local.x is le local.y
  """
  return left_value <= right_value

