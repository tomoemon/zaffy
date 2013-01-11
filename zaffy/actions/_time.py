# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from baseaction import BaseAction

def _adddate(day=0, hour=0, min=0, sec=0, msec=0):
  return datetime.now() + timedelta(days=day, hours=hour, minutes=min, seconds=sec, milliseconds=msec)

class Time(BaseAction):
  """ Time アクション
  """
  @classmethod
  def now(cls, day=0, hour=0, min=0, sec=0, msec=0):
    return _adddate(day, hour, min, sec, msec)

  @classmethod
  def timestamp(cls, day=0, hour=0, min=0, sec=0, msec=0):
    return int(time.mktime(_adddate(day, hour, min, sec, msec).timetuple()))

  @classmethod
  def format(cls, format, day=0, hour=0, min=0, sec=0, msec=0):
    return _adddate(day, hour, min, sec, msec).strftime(format)

