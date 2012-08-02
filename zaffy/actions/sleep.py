# -*- coding: utf-8 -*-
import time
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting

class Sleep(BaseAction):
  """ Sleep アクション
  指定した時間処理を停止する
  """

  param_setting = ActionParamSetting(
      allow_any_params=False,
      required=['time']
      )

  def do_sleep(self, params):
    time.sleep(params.time / 1000.0)

