# -*- coding: utf-8 -*-


def is_gte(left_value, right_value):
  """ test `left_value` is gte (geater than equal) `right_value`

  `left_value` が `right_value` より大きいか等しいことをテストする (:ref:`references-customtests-ge-label` のエイリアス)

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 200
       y: 100
       assert:
         - local.x is gte local.y
  """
  return left_value >= right_value

