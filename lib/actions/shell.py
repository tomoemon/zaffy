# -*- coding: utf-8 -*-
import os
from os import path
from subprocess import Popen, PIPE
from baseaction import BaseAction
import util


class Shell(BaseAction):
  """ Shell アクション

  シェルを通してプロセスの実行などを行なう
  """
  def do_shell(self, cmd, stdin=None, curdir=None, shell=True, error_on_failed=False):
    """ do_run の省略呼び出し """
    self.do_run(cmd, stdin, curdir, shell, error_on_failed)

  def do_run(self, cmd, stdin=None, curdir=None, shell=True, error_on_failed=False):
    """ コマンドの実行

    .. code-block:: yaml

     - サンプルシナリオ

     - action: shell
       cmd: ls -l /tmp

     - action: debug
       result: <<last.res.stdout>>

    :param string cmd: 実行するコマンド
    :param string curdir: 実行時のカレントディレクトリ。指定しない場合は zaffy 実行時のカレントディレクトリ
    :param bool shell: シェルを介して実行する (default:True)
    :param bool error_on_failed: コマンドの失敗時(return code != 0) にテストを error 扱いにする (default:False)
    :return: - **stdout** (*string*) - 実行したコマンドの標準出力
             - **stderr** (*string*) - 実行したコマンドの標準エラー
             - **returncode** (*int*) - 実行したコマンドの終了ステータス
    """
    before_curdir = path.abspath(os.curdir)

    if curdir:
      os.chdir(curdir)

    stdin_pipe = PIPE
    stdout_pipe = PIPE
    stderr_pipe = PIPE
    proc = Popen(cmd,
        stdin=stdin_pipe, stdout=stdout_pipe, stderr=stderr_pipe, shell=shell)
    (stdoutdata, stderrdata) = proc.communicate(stdin)

    stdoutdata = util.unicode_os_string(stdoutdata)
    stderrdata = util.unicode_os_string(stderrdata)

    if error_on_failed and proc.returncode != 0:
      raise Exception(stderrdata.strip() + ' (code=' + util.unicode(proc.returncode) + ')')

    self.result = {
        'stdout': stdoutdata,
        'stderr': stderrdata,
        'returncode': proc.returncode
    }

    os.chdir(before_curdir)

