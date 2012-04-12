# -*- coding: utf-8 -*-
import datetime

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
  return value.strftime(format)

def todatetime(value, format='%Y-%m-%d %H:%M:%S'):
  return datetime.datetime.strptime(value, format)

def todate(value, format='%Y-%m-%d'):
  return datetime.datetime.strptime(value, format).date()

