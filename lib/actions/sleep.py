# -*- coding: utf-8 -*-
import time as _time
from baseaction import BaseAction


class Sleep(BaseAction):
  """ Sleep アクション

  指定した時間、処理を停止する

  .. code-block:: yaml

     - サンプルシナリオ

     - action: debug
       t1: start

     - action: sleep
       time: 3000 # => 3秒間停止する

     - action: debug
       t2: end
  """

  def do_sleep(self, time):
    """ 指定した時間、処理を停止する

    :param int time: 停止する秒数(ミリ秒)
    :return: None
    """
    _time.sleep(time / 1000.0)

