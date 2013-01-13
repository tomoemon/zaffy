# -*- coding: utf-8 -*-
from baseaction import BaseAction


class Python(BaseAction):
  """ Pythonアクション
  指定されたコードを実行する
  """
  def do_python(self, code, global_env):
    self.do_run(code, global_env)

  def do_run(self, code, global_env):
    local_dict = {'local': global_env['local']}
    global_dict = dict(global_env)
    ast = compile(code, '<string>', 'exec')
    eval(ast, global_dict, local_dict)
    del local_dict['local']
    self.result.update(local_dict)

