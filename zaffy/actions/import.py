# -*- coding: utf-8 -*-
from baseaction import BaseAction

class Import(BaseAction):
  """ import アクション
  """
  default_params = {
    "path":""
  }

  def do_action(self):
    params = self.setting.params
    params.path = params.path.trim()
    if not params.path:
      raise Exception(params.path + " not exists")
    path_elements = [e.trim() for e in params.path.split(".")]

    if not path_elements:
      raise Exception(params.path + " is invalid path")

    empty_elem_num = 0
    for e in path_elements:
      if e: break
      empty_elem_num += 1

    if empty_elem_num == 0:
      # シナリオディレクトリのトップから探してくる
      pass
    else:
      pass
      # (empty_elem_num - 1) 個上のディレクトリまでさかのぼって探す
      # empty_elem_num == 0 の場合はカレントディレクトリ

