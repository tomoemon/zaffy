# -*- coding: utf-8 -*-
import ssh
from baseaction import BaseAction


class Ssh(BaseAction):
  """ Ssh アクション
  SSH接続を通してプロセスの実行などを行なう
  """
  def do_ssh(self, host, user, cmd, port=22, password=None, key_file=None):
    method_params = locals()
    del method_params['self']
    self.do_run(**method_params)

  def do_put(self, host, user, local, remote, port=22, password=None, key_file=None):
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=user, password=password, key_filename=key_file, port=port)

    sftp = client.open_sftp()
    sftp.put(local, remote)
    sftp.close()

  def do_get(self, host, user, local, remote, port=22, password=None, key_file=None):
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=user, password=password, key_filename=key_file, port=port)

    sftp = client.open_sftp()
    sftp.get(remote, local)
    sftp.close()

  def do_run(self, host, user, cmd, port=22, password=None, key_file=None):
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

