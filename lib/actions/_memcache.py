# -*- coding: utf-8 -*-
from baseaction import BaseAction
from pymemcache.client import Client
import util


class Memcache(BaseAction):
  """ Memcache アクション
  """
  _DEFAULT_PORT=11211
  _DEFAULT_ENCODING="utf-8"

  def _connect(self, host, port, func):
      client = Client((host, port))
      try:
          self.output = func(client)
      finally:
          client.close()

  @classmethod
  def _encode(cls, value):
      if not isinstance(value, dict):
          return value.encode(cls._DEFAULT_ENCODING)

      result = {}
      for key, value in value.items():
          result[key] = value.encode(cls._DEFAULT_ENCODING) if isinstance(value, util.basestring) else value
      return result

  @classmethod
  def _decode(cls, value):
      if not isinstance(value, dict):
          return value.decode(cls._DEFAULT_ENCODING)

      result = {}
      for key, value in value.items():
          result[key] = value.decode(cls._DEFAULT_ENCODING) if isinstance(value, util.bytes) else value
      return result

  def do_set(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      """ many ver exists """
      return self.do_setmany({key: value}, expire, noreply, host, port)

  def do_setmany(self, data, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      """ many ver exists """
      return self._connect(host, port,
              lambda c: {"succeeded": c.set_many(self._encode(data), expire, noreply)})

  def do_add(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.add(key, self._encode(value), expire, noreply)})

  def do_replace(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.replace(key, self._encode(value), expire, noreply)})

  def do_append(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.append(key, self._encode(value), expire, noreply)})

  def do_prepend(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.prepend(key, self._encode(value), expire, noreply)})

  def do_cas(self, key, value, cas, expire=0, noreply=False, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.cas(key, self._encode(value), cas, expire, noreply)})

  def do_get(self, key, host=None, port=_DEFAULT_PORT):
      """
      return dict
      """
      if not isinstance(key, (list, tuple)):
          key = [key]
      return self._connect(host, port, lambda c: self._decode(c.get_many(key)))

  def do_gets(self, key, host=None, port=_DEFAULT_PORT):
      """
      return dict
      """
      if not isinstance(key, (list, tuple)):
          key = [key]
      return self._connect(host, port, lambda c: self._decode(c.gets_many(key)))

  def do_delete(self, key, noreply=True, host=None, port=_DEFAULT_PORT):
      """ many ver exists """
      if not isinstance(key, (list, tuple)):
          key = [key]
      return self._connect(host, port,
              lambda c: {"succeeded": c.delete_many(key, noreply)})

  def do_incr(self, key, value, noreply=False, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"value": c.incr(key, value, noreply)})

  def do_decr(self, key, value, noreply=False, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"value": c.decr(key, value, noreply)})

  def do_touch(self, key, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.touch(key, expire, noreply)})

  def do_stats(self, host=None, port=_DEFAULT_PORT, *args):
      return self._connect(host, port, lambda c: c.stats(*args))

  def do_flush_all(self, delay=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.flush_all(delay, noreply)})

