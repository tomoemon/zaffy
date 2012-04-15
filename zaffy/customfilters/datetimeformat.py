# -*- coding: utf-8 -*-
import datetime

def do_datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
  return value.strftime(format)

def do_todatetime(value, format='%Y-%m-%d %H:%M:%S'):
  return datetime.datetime.strptime(value, format)

def do_todate(value, format='%Y-%m-%d'):
  return datetime.datetime.strptime(value, format).date()

