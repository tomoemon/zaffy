# -*- coding: utf-8 -*-


def is_lte(left_value, right_value):
  """ test `left_value` is lte (less than equal) `right_value`

  `left_value` が `right_value` より小さいか等しいことをテストする (:ref:`references-customtests-le-label` のエイリアス)

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 100
       y: 200
       assert:
         - local.x is lte local.y
  """
  return left_value <= right_value

