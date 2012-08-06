# -*- coding: utf-8 -*-
import os
from os import path
from subprocess import Popen, PIPE
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting

class Shell(BaseAction):
  """ Shell アクション
  プロセスの実行などを行なう
  """

  param_setting = ActionParamSetting(
      allow_any_params=False,
      required=['cmd'],
      optional={'stdin': None, 'curdir': None}
      )

  @classmethod
  def get_param_setting(cls, method_name):
    return cls.param_setting

  def do_shell(self, params):
    self.do_run(params)

  def do_run(self, params):
    before_curdir = path.abspath(os.curdir)

    if params.curdir:
      os.chdir(params.curdir)

    stdin_pipe = PIPE if params.stdin else None
    stdout_pipe = PIPE
    stderr_pipe = PIPE
    proc = Popen(params.cmd,
        stdin=stdin_pipe, stdout=stdout_pipe, stderr=stderr_pipe)
    (stdoutdata, stderrdata) = proc.communicate(params.stdin)

    self.result = {
        'stdout': stdoutdata,
        'stderr': stderrdata,
        'returncode': proc.returncode
        }

    os.chdir(before_curdir)
