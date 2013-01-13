# -*- coding: utf-8 -*-
import time
import dateutil.parser
from datetime import date, datetime, timedelta


def _adddate(value, day=0, hour=0, min=0, sec=0, msec=0):
  return value + timedelta(days=day, hours=hour, minutes=min, seconds=sec, milliseconds=msec)


def _todatetime(dateobj, format=None):
  if isinstance(dateobj, datetime):
    return dateobj
  elif isinstance(dateobj, date):
    return datetime(dateobj.year, dateobj.month, dateobj.day)
  elif isinstance(dateobj, basestring):
    if format is None:
      return dateutil.parser.parse(dateobj)
    return datetime.strptime(dateobj, format)
  elif isinstance(dateobj, int) or isinstance(dateobj, float):
    return datetime.fromtimestamp(dateobj)
  raise Exception("cannot convert to datetime from unknown type: {0}".format(dateobj))


def do_dateformat(value, format, fromformat=None):
  return _todatetime(value, fromformat).strftime(format)


def do_todate(value, format=None):
  return _todatetime(value, format)


def do_dateadd(value, day=0, hour=0, min=0, sec=0, msec=0, format=None):
  value = _todatetime(value, format)
  return _adddate(value, day, hour, min, sec, msec)


def do_timestamp(value, day=0, hour=0, min=0, sec=0, msec=0, format=None):
  value = _todatetime(value, format)
  return int(time.mktime(_adddate(value, day, hour, min, sec, msec).timetuple()))
