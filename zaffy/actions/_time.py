# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from baseaction import BaseAction


def _adddate(day=0, hour=0, min=0, sec=0, msec=0):
  return datetime.now() + timedelta(days=day, hours=hour, minutes=min, seconds=sec, milliseconds=msec)


class Time(BaseAction):
  """ Time アクション

  現在時刻の取得、日時のフォーマットを行なう

  .. code-block:: yaml

     - サンプルシナリオ

     - action: debug
       t1: <<time.now()>> #=> '2013-02-22 01:35:42.100000'
       t2: <<time.now(days=2,hours=3)>> #=> '2013-02-24 04:35:42.100000'
       t3: <<time.timestamp()>> #=> 1361464681
       t4: <<time.format('%Y-%m-%d %H:%M:%S')>> #=> '2013-02-22 01:38:01'
  """
  @classmethod
  def now(cls, day=0, hour=0, min=0, sec=0, msec=0):
    """ 現在日時を Datetime オブジェクトで返す

    引数に正の値を渡すと未来の日時、負の値を渡すと過去の日時を取得する

    :param int day: 現在日時に加える日数
    :param int hour: 現在日時に加える時間
    :param int min: 現在日時に加える分
    :param int sec: 現在日時に加える秒
    :param int msec: 現在日時にミリ秒
    :return: (*datetime*) - python datetime object
    """
    return _adddate(day, hour, min, sec, msec)

  @classmethod
  def timestamp(cls, day=0, hour=0, min=0, sec=0, msec=0):
    """ 現在日時を Unix タイムスタンプで返す

    引数に正の値を渡すと未来の日時、負の値を渡すと過去の日時を取得する

    :param int day: 現在日時に加える日数
    :param int hour: 現在日時に加える時間
    :param int min: 現在日時に加える分
    :param int sec: 現在日時に加える秒
    :param int msec: 現在日時にミリ秒
    :return: (*int*) - unix timestamp
    """
    return int(time.mktime(_adddate(day, hour, min, sec, msec).timetuple()))

  @classmethod
  def format(cls, fmt, day=0, hour=0, min=0, sec=0, msec=0):
    """ 現在日時を文字列フォーマットして返す

    フォーマット文字列
      http://docs.python.jp/2/library/time.html#time.strftime

    引数に正の値を渡すと未来の日時、負の値を渡すと過去の日時を取得する

    :param int day: 現在日時に加える日数
    :param int hour: 現在日時に加える時間
    :param int min: 現在日時に加える分
    :param int sec: 現在日時に加える秒
    :param int msec: 現在日時にミリ秒
    :return: (*int*) - unix timestamp
    """
    return _adddate(day, hour, min, sec, msec).strftime(fmt)

