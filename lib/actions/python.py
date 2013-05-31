# -*- coding: utf-8 -*-
from baseaction import BaseAction


class Python(BaseAction):
  """ Python アクション

  任意の python コードを実行する

  .. code-block:: yaml

    - サンプルシナリオ

    - action: local
      x: 4

    - action: python
      code: |
        import math
        z = math.factorial(local['x'])
      assert:
        - res.z is eq 24
  """
  def do_python(self, code, global_env):
    """do_run の省略呼び出し"""
    self.do_run(code, global_env)

  def do_run(self, code, global_env):
    """
    :param string code: python として実行可能なコード
    :return: (*dict*) コード上のローカル変数の値が辞書形式でセットされる
    """
    local_dict = {'local': global_env['local']}
    global_dict = dict(global_env)
    ast = compile(code, '<string>', 'exec')
    eval(ast, global_dict, local_dict)
    del local_dict['local']
    self.output.update(local_dict)

