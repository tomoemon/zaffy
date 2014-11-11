# -*- coding: utf-8 -*-
from baseaction import BaseAction
from pymemcache.client import Client


class Memcache(BaseAction):
  """ Memcache アクション
  """
  _DEFAULT_PORT=11211

  def _connect(self, host, port, func):
      client = Client((host, port))
      try:
          self.output = func(client)
      finally:
          client.close()

  def do_set(self, values, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      """ many ver exists """
      return self._connect(host, port,
              lambda c: {"succeeded": c.set_many(values, expire, noreply)})

  def do_add(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.add(key, value, expire, noreply)})

  def do_replace(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.replace(key, value, expire, noreply)})

  def do_append(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.append(key, value, expire, noreply)})

  def do_prepend(self, key, value, expire=0, noreply=True, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.prepend(key, value, expire, noreply)})

  def do_cas(self, key, value, cas, expire=0, noreply=False, host=None, port=_DEFAULT_PORT):
      return self._connect(host, port,
              lambda c: {"succeeded": c.cas(key, value, cas, expire, noreply)})

  def do_get(self, key, host=None, port=_DEFAULT_PORT):
      """
      return dict
      """
      if isinstance(key, (list, tuple)):
          return self._connect(host, port, lambda c: c.get_many(key))
      else:
          return self._connect(host, port, lambda c: {key: c.get(key)})

  def do_gets(self, keys, host=None, port=_DEFAULT_PORT):
      """
      return dict
      """
      if isinstance(keys, (list, tuple)):
          return self._connect(host, port, lambda c: c.gets_many(keys))
      else:
          return self._connect(host, port, lambda c: {keys: c.gets(keys)})

  def do_delete(self, key, noreply=True, host=None, port=_DEFAULT_PORT):
      """ many ver exists """
      if isinstance(key, (list, tuple)):
          return self._connect(host, port,
                  lambda c: {"succeeded": c.delete_many(key, noreply)})
      else:
          return self._connect(host, port,
                  lambda c: {"succeeded": c.delete(key, noreply)})

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

