# -*- coding: utf-8 -*-


def is_in(left_value, right_value):
  """ test `left_value` is in `right_value`
  `left_value` が `right_value` に含まれることをテストする

  :param object left_value: 任意の値
  :param list|dict|... right_value: ``__contains__`` メソッドを持つ、list, dict 等のコレクション型

  .. code-block:: yaml

     - サンプルシナリオ

     - action: local
       x: 200
       y: [100, 200, 300]
       z:
         a: 20
         b: 30
       assert:
         - local.x is in local.y
         - "a" is in local.z
  """
  return left_value in right_value

