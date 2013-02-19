# -*- coding: utf-8 -*-
import time as _time
from baseaction import BaseAction


class Sleep(BaseAction):
  """ Sleep アクション

  指定した時間、処理を停止する
  """

  def do_sleep(self, time):
    """ sleep """
    _time.sleep(time / 1000.0)

