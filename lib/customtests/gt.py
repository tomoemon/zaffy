# -*- coding: utf-8 -*-


def is_gt(left_value, right_value):
  """ test `left_value` is gt (greater than) `right_value`

  `left_value` が `right_value` より大きいことをテストする

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 200
       y: 100
       assert:
         - local.x is gt local.y
  """
  return left_value > right_value

