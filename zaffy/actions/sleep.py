# -*- coding: utf-8 -*-
import time as timemod
from baseaction import BaseAction


class Sleep(BaseAction):
  """ Sleep アクション
  指定した時間処理を停止する
  """

  def do_sleep(self, time):
    timemod.sleep(time / 1000.0)

