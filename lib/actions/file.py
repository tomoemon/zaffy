# -*- coding: utf-8 -*-
import os
from datetime import datetime
import shutil
from baseaction import BaseAction


class File(BaseAction):
  """ File アクション

  ファイル操作やファイルに関する情報の取得を行なう
  """
  @classmethod
  def exists(cls, filepath):
    """ ファイルの存在チェック

    :param string filepath: 対象のファイル
    :return: (*bool*) - 存在する場合 True、なければ False
    """
    return os.access(filepath, os.F_OK)

  @classmethod
  def writable(cls, filepath):
    """ ファイルの書き込み権限チェック

    :param string filepath: 対象のファイル
    :return: (*bool*) - 権限があれば True、なければ False
    """
    return os.access(filepath, os.W_OK)

  @classmethod
  def readable(cls, filepath):
    """ ファイルの読み込み権限チェック

    :param string filepath: 対象のファイル
    :return: (*bool*) - 権限があれば True、なければ False
    """
    return os.access(filepath, os.R_OK)

  @classmethod
  def executable(cls, filepath):
    """ ファイルの実行権限チェック

    :param string filepath: 対象のファイル
    :return: (*bool*) - 権限があれば True、なければ False
    """
    return os.access(filepath, os.R_OK)

  @classmethod
  def size(cls, filepath):
    """ ファイルサイズ取得

    :param string filepath: 対象のファイル
    :return: (*int*) - ファイルのバイト数
    """
    stat_value = os.stat(filepath)
    return stat_value.st_size

  @classmethod
  def access_time(cls, filepath):
    """ ファイルの最終アクセス日時を取得

    :param string filepath: 対象のファイル
    :return: (*datetime*) - ファイルの最終アクセス日時
    """
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_atime)

  @classmethod
  def update_time(cls, filepath):
    """ ファイルの最終更新日時を取得

    :param string filepath: 対象のファイル
    :return: (*datetime*) - ファイルの最終更新日時
    """
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_mtime)

  @classmethod
  def create_time(cls, filepath):
    """ ファイルの作成日時を取得

    :param string filepath: 対象のファイル
    :return: (*datetime*) - ファイルの作成日時
    """
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_ctime)

  @classmethod
  def read(cls, filepath, size=-1, offset=0, encoding=None):
    """ ファイルの読み込み

    :param string filepath: 対象のファイル
    :param int size: 取得するバイト数
    :param int offset: 取得するバイトオフセット
    :param string encoding: 対象ファイルの文字エンコーディング
    :return: (*string|byte*) - 取得したバイト列、もしくは文字列 (encoding 指定時)
    """
    import codecs
    if encoding:
      with codecs.open(filepath, encoding=encoding) as fp:
        fp.seek(offset)
        return fp.read(size)
    else:
      with open(filepath, "rb") as fp:
        fp.seek(offset)
        return fp.read(size)

  def do_copy(self, path, to):
    """ ファイルをコピーする

    :param string path: コピー元パス
    :param string to: コピー先パス
    :return: (*None*)
    """
    shutil.copy(path, to)

  def do_delete(self, path):
    """ ファイルまたはディレクトリを削除する

    :param string path: 削除対象パス
    :return: (*None*)
    """
    if os.path.isdir(path):
      shutil.rmtree(path)
    else:
      os.unlink(path)

  def do_rename(self, path, to):
    """ ファイルをリネーム（移動）する

    :param string path: リネーム元パス
    :param string to: リネーム先パス
    :return: (*None*)
    """
    shutil.move(path, to)

  def do_write(self, path, data, mode="wb"):
    """ ファイルの書き込み

    :param string path: 対象のファイル
    :param string|byte data: 対象データ
    :param string mode: 書き込みモード
    :return: (*None*)
    """
    with open(path, mode) as fp:
      fp.write(data)

