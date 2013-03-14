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
    """ exists """
    return os.access(filepath, os.F_OK)

  @classmethod
  def writable(cls, filepath):
    """ writable """
    return os.access(filepath, os.W_OK)

  @classmethod
  def readable(cls, filepath):
    """ readable """
    return os.access(filepath, os.R_OK)

  @classmethod
  def executable(cls, filepath):
    """ executable """
    return os.access(filepath, os.R_OK)

  @classmethod
  def size(cls, filepath):
    """ size """
    stat_value = os.stat(filepath)
    return stat_value.st_size

  @classmethod
  def access_time(cls, filepath):
    """ access_time """
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_atime)

  @classmethod
  def update_time(cls, filepath):
    """ update_time """
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_mtime)

  @classmethod
  def create_time(cls, filepath):
    """ create_time """
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_ctime)

  @classmethod
  def read(cls, filepath, size=-1, offset=0, encoding=None):
    """ read """
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
    """ copy """
    shutil.copy(path, to)

  def do_delete(self, path):
    """ delete file """
    if os.path.isdir(path):
      shutil.rmtree(path)
    else:
      os.unlink(path)

  def do_rename(self, path, to):
    """ rename """
    shutil.move(path, to)

  def do_write(self, path, data, mode="wb"):
    """ write """
    with open(path, mode) as fp:
      fp.write(data)

