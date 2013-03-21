# -*- coding: utf-8 -*-
import ssh
from baseaction import BaseAction


class Ssh(BaseAction):
  """ Ssh アクション

  SSH接続を通してプロセスの実行などを行なう

  .. note::

    接続先パスワードなどは :ref:`references-actions-preset-label` で定義しておくと、毎回記述する必要がなくなります。
  """
  def do_ssh(self, host, user, cmd, port=22, password=None, key_file=None):
    """ do_run の省略呼び出し """
    method_params = locals()
    del method_params['self']
    self.do_run(**method_params)

  def do_put(self, host, user, local, remote, port=22, password=None, key_file=None):
    """ scp でファイルを送信する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: ssh.put
         host: localhost
         user: testuser
         password: hogehoge
         local: zaffy.py
         remote: /tmp/zaffy.py

    :param string host: 接続先ホスト名、またはIPアドレス
    :param string user: 接続先ホストにおけるユーザ名
    :param string local: ローカルの送信ファイル
    :param string remote: リモートのファイル保存先
    :param int port: 接続先ポート番号
    :param string password: パスワード認証を行う場合のユーザのログインパスワード
    :param string key_file: 公開鍵認証を行う場合の公開鍵ファイル
    """
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=user, password=password, key_filename=key_file, port=port)

    sftp = client.open_sftp()
    sftp.put(local, remote)
    sftp.close()

  def do_get(self, host, user, local, remote, port=22, password=None, key_file=None):
    """ scp でファイルを取得する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: ssh.get
         host: localhost
         user: testuser
         password: hogehoge
         remote: /tmp/zaffy.py
         local: zaffy2.py

    :param string host: 接続先ホスト名、またはIPアドレス
    :param string user: 接続先ホストにおけるユーザ名
    :param string local: ローカルのファイル保存先
    :param string remote: リモートのファイル取得先
    :param int port: 接続先ポート番号
    :param string password: パスワード認証を行う場合のユーザのログインパスワード
    :param string key_file: 公開鍵認証を行う場合の公開鍵ファイル
    """
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=user, password=password, key_filename=key_file, port=port)

    sftp = client.open_sftp()
    sftp.get(remote, local)
    sftp.close()

  def do_run(self, host, user, cmd, port=22, password=None, key_file=None):
    """ ssh 接続してコマンドを実行する

    .. code-block:: yaml

     - サンプルシナリオ

     - action: ssh
       host: localhost
       user: testuser
       password: hogehoge
       cmd: ls -l
       assert:
         - res.returncode is eq 0

    :param string host: 接続先ホスト名、またはIPアドレス
    :param string user: 接続先ホストにおけるユーザ名
    :param string cmd: 実行コマンド
    :param int port: 接続先ポート番号
    :param string password: パスワード認証を行う場合のユーザのログインパスワード
    :param string key_file: 公開鍵認証を行う場合の公開鍵ファイル
    :return: - **stdout** (*string*) - 実行したコマンドの標準出力
             - **stderr** (*string*) - 実行したコマンドの標準エラー
             - **returncode** (*int*) - 実行したコマンドの終了ステータス
    """
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=user, password=password, key_filename=key_file, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)

    self.result = {
        'stdout': stdout.read(),
        'stderr': stderr.read(),
        'returncode': stdout.channel.recv_exit_status(),
        }

