# -*- coding: utf-8 -*-
import os
from os import path
from subprocess import Popen, PIPE
from baseaction import BaseAction


class Shell(BaseAction):
  """ Shell アクション

  シェルを通してプロセスの実行などを行なう
  """
  def do_shell(self, cmd, stdin=None, curdir=None):
    """ do_run の省略呼び出し """
    self.do_run(cmd, stdin, curdir)

  def do_run(self, cmd, stdin=None, curdir=None):
    """ run """
    before_curdir = path.abspath(os.curdir)

    if curdir:
      os.chdir(curdir)

    stdin_pipe = PIPE if stdin else None
    stdout_pipe = PIPE
    stderr_pipe = PIPE
    proc = Popen(cmd,
        stdin=stdin_pipe, stdout=stdout_pipe, stderr=stderr_pipe)
    (stdoutdata, stderrdata) = proc.communicate(stdin)

    self.result = {
        'stdout': stdoutdata,
        'stderr': stderrdata,
        'returncode': proc.returncode
    }

    os.chdir(before_curdir)
