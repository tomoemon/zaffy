# -*- coding: utf-8 -*-
import os
from datetime import datetime
import shutil
from baseaction import BaseAction


class File(BaseAction):
  """ File アクション
  ファイルに関する検査などを行なう
  """
  @classmethod
  def exists(cls, filepath):
    return os.access(filepath, os.F_OK)

  @classmethod
  def writable(cls, filepath):
    return os.access(filepath, os.W_OK)

  @classmethod
  def readable(cls, filepath):
    return os.access(filepath, os.R_OK)

  @classmethod
  def executable(cls, filepath):
    return os.access(filepath, os.R_OK)

  @classmethod
  def size(cls, filepath):
    stat_value = os.stat(filepath)
    return stat_value.st_size

  @classmethod
  def access_time(cls, filepath):
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_atime)

  @classmethod
  def update_time(cls, filepath):
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_mtime)

  @classmethod
  def create_time(cls, filepath):
    stat_value = os.stat(filepath)
    return datetime.fromtimestamp(stat_value.st_ctime)

  @classmethod
  def read(cls, filepath, size=-1, offset=0):
    with open(filepath, "rb") as fp:
      fp.seek(offset)
      return fp.read(size)

  def do_copy(self, path, to):
    shutil.copy(path, to)

  def do_remove(self, path):
    if os.path.isdir(path):
      shutil.rmtree(path)
    else:
      os.unlink(path)

  def do_rename(self, path, to):
    shutil.move(path, to)

  def do_write(self, path, data, mode="wb"):
    with open(path, mode) as fp:
      fp.write(data)

