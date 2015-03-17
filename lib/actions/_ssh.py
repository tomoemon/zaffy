# -*- coding: utf-8 -*-
import time
import paramiko as ssh
from baseaction import BaseAction


class Ssh(BaseAction):
  """ Ssh アクション

  SSH接続を通してプロセスの実行などを行なう

  .. note::

    接続先パスワードなどは :ref:`references-actions-preset-label` で定義しておくと、毎回記述する必要がなくなります。
  """
  def _connect(self, host, user, password, key_file, port, timeout):
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=user, password=password, key_filename=key_file, port=port, timeout=timeout)
    return client

  def do_put(self, host, user, local, remote, port=22, password=None, key_file=None, timeout=None):
    """ sftp でファイルを送信する

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
    :param int timeout: タイムアウト時間（秒）
    """
    client = self._connect(host, user, password, key_file, port, timeout)

    sftp = client.open_sftp()
    sftp.put(local, remote)
    sftp.close()

  def do_remove(self, host, user, remote, port=22, password=None, key_file=None, timeout=None):
    """ sftp でファイルを削除する（ディレクトリ削除は rmdir）

    .. code-block:: yaml

       - サンプルシナリオ

       - action: ssh.remove
         host: localhost
         user: testuser
         password: hogehoge
         remote: /tmp/zaffy.py

    :param string host: 接続先ホスト名、またはIPアドレス
    :param string user: 接続先ホストにおけるユーザ名
    :param string remote: 削除対象のリモートファイル
    :param int port: 接続先ポート番号
    :param string password: パスワード認証を行う場合のユーザのログインパスワード
    :param string key_file: 公開鍵認証を行う場合の公開鍵ファイル
    :param int timeout: タイムアウト時間（秒）
    """
    client = self._connect(host, user, password, key_file, port, timeout)

    sftp = client.open_sftp()
    sftp.remove(remote)
    sftp.close()

  def do_rmdir(self, host, user, remote, port=22, password=None, key_file=None, timeout=None):
    """ sftp でディレクトリを削除する（ファイル削除は remove）

    .. code-block:: yaml

       - サンプルシナリオ

       - action: ssh.rmdir
         host: localhost
         user: testuser
         password: hogehoge
         remote: /tmp/zaffy

    :param string host: 接続先ホスト名、またはIPアドレス
    :param string user: 接続先ホストにおけるユーザ名
    :param string remote: 削除対象のリモートディレクトリ
    :param int port: 接続先ポート番号
    :param string password: パスワード認証を行う場合のユーザのログインパスワード
    :param string key_file: 公開鍵認証を行う場合の公開鍵ファイル
    :param int timeout: タイムアウト時間（秒）
    """
    client = self._connect(host, user, password, key_file, port, timeout)

    sftp = client.open_sftp()
    sftp.rmdir(remote)
    sftp.close()

  def do_get(self, host, user, local, remote, port=22, password=None, key_file=None, timeout=None):
    """ sftp でファイルを取得する

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
    :param int timeout: タイムアウト時間（秒）
    """
    client = self._connect(host, user, password, key_file, port, timeout)

    sftp = client.open_sftp()
    sftp.get(remote, local)
    sftp.close()

  def do_ssh(self, host, user, cmd, port=22, password=None, key_file=None, timeout=None, decoding='utf-8'):
    """ do_run の省略呼び出し """
    method_params = locals()
    del method_params['self']
    self.do_run(**method_params)

  def do_run(self, host, user, cmd, port=22, password=None, key_file=None, timeout=None, decoding='utf-8'):
    """ ssh 接続してコマンドを実行する

    .. code-block:: yaml

     - サンプルシナリオ

     - action: ssh
       host: localhost
       user: testuser
       password: hogehoge
       cmd: ls -l
       assert:
         - out.returncode is eq 0

    :param string host: 接続先ホスト名、またはIPアドレス
    :param string user: 接続先ホストにおけるユーザ名
    :param string cmd: 実行コマンド
    :param int port: 接続先ポート番号
    :param string password: パスワード認証を行う場合のユーザのログインパスワード
    :param string key_file: 公開鍵認証を行う場合の公開鍵ファイル
    :param string decoding: 実行結果をデコードする際に用いるエンコード方式
    :param int timeout: タイムアウト時間（秒）
    :return: - **stdout** (*string*) - 実行したコマンドの標準出力
             - **stderr** (*string*) - 実行したコマンドの標準エラー
             - **returncode** (*int*) - 実行したコマンドの終了ステータス
    """
    client = self._connect(host, user, password, key_file, port, timeout)
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)

    self.output = {
        'stdout': stdout.read().decode(decoding) if decoding else stdout.read(),
        'stderr': stderr.read().decode(decoding) if decoding else stderr.read(),
        'returncode': self.__get_exit_status(stdout),
        }

  @classmethod
  def __get_exit_status(cls, output):
    for i in range(3):
      if output.channel.exit_status_ready():
        return output.channel.recv_exit_status()
      else:
        time.sleep(1)
    else:
      return -1 # error

