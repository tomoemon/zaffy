# -*- coding: utf-8 -*-
import os
from datetime import datetime
from os import path
import shutil
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting

class File(BaseAction):
  """ File アクション
  ファイルに関する検査などを行なう
  """

  param_setting = {
      "write": ActionParamSetting(
        allow_any_params=False,
        required=['path', 'data'],
        optional={'mode':'wb'}
        ),
      "copy": ActionParamSetting(
        allow_any_params=False,
        required=['path', 'to']
        ),
      "remove": ActionParamSetting(
        allow_any_params=False,
        required=['path']
        ),
      "rename": ActionParamSetting(
        allow_any_params=False,
        required=['path', 'to']
        )
      }

  @classmethod
  def get_param_setting(cls, method_name):
    return cls.param_setting[method_name]

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

  def do_copy(self, params):
    shutil.copy(params.path, params.to)

  def do_remove(self, params):
    if path.isdir(params.path):
      shutil.rmtree(params.path)
    else:
      os.unlink(params.path)

  def do_rename(self, params):
    shutil.move(params.path, params.to)

  def do_write(self, params):
    with open(params.path, params.mode) as fp:
      fp.write(params.data)

