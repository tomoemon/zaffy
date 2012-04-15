# -*- coding: utf-8 -*-

class CmpLog(object):
  def __init__(self):
    self.log_list = []

  def add(self, got, expect):
    self.log_list.append({
      "got": got,
      "expect": expect
      })

class Comparator(object):
  def __init__(self, val, cmp_log):
    self._value = val
    self._cmp_log = cmp_log

  def __cmp__(self, other):
    if isinstance(other, Comparator):
      other_value = other.value
    else:
      other_value = other

    self._cmp_log.add(self._value, other_value)
    return cmp(self._value, other_value)

  def __call__(self, *args):
    return wrap(self._value(*args), self._cmp_log)

  def __getattr__(self, name):
    return wrap(getattr(self._value, name), self._cmp_log)

  def __getitem__(self, key):
    return wrap(self._value[key], self._cmp_log)

  def __iter__(self):
    return wrap(iter(self._value), self._cmp_log)

  def __reversed__(self):
    return wrap(reversed(self._value), self._cmp_log)

  def __getslice__(self, i, j):
    return wrap(self._value[i:j], self._cmp_log)

  def __contains__(self, item):
    # bool オブジェクトを返さないと python のエラーになってしまう
    self._cmp_log.add(item, self._value)
    return item in self._value

  def __hash__(self):
    # int オブジェクトを返さないと python のエラーになってしまう
    return hash(self._value)

  def __str__(self):
    # str オブジェクトを返さないと python のエラーになってしまう
    return str(self._value)

  def __unicode__(self):
    return unicode(self._value)

  def __repr__(self):
    return repr(self._value)

  def __len__(self):
    return len(self._value)

def wrap(obj, cmp_log):
  if isinstance(obj, Comparator):
    return obj
  return Comparator(obj, cmp_log)

def wrap_func(function, value_index):
  def _wrap(*args, **kw):
    res = function(*args, **kw)
    if isinstance(args[value_index], Comparator):
      return wrap(res, args[value_index]._cmp_log)
    return res
  return _wrap

def wrap_test_func(function, arg_size):
  """ customizetests を Comparator 対応する """
  def _wrap(*args, **kw):
    res = function(*args, **kw)
    if isinstance(args[0], Comparator):
      args[0]._cmp_log.add(*args[:arg_size])
    return res
  return _wrap

def wrap_object(obj, cmp_log):
  """ 全階層のオブジェクトを Comparator にする """
  newobj = obj
  if isinstance(obj, list):
    newobj = []
    for item in obj:
      newobj.append(wrap_object(item, cmp_log))
  elif isinstance(obj, tuple):
    temp = []
    for item in obj:
      temp.append(wrap_object(item, cmp_log))
    newobj = tuple(temp)
  elif isinstance(obj, set):
    temp = []
    for item in obj:
      temp.append(wrap_object(item, cmp_log))
    newobj = set(temp)
  elif isinstance(obj, dict):
    newobj = {}
    for key, value in obj.items():
      newobj[key] = wrap_object(value, cmp_log)
  elif '__dict__' in dir(obj):
    newobj = obj.__dict__.copy()
    for attr, value in newobj.items():
      newobj[attr] = wrap_object(value, cmp_log)
  return wrap(newobj, cmp_log)

