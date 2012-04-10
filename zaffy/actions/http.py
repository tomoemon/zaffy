# -*- coding: utf-8 -*-
import requests

class HttpSetting(object):
  def __init__(self):
    self._parent = None
    self._method = None
    self.url = ""
    self.url_base = ""
    self.headers = {}
    self.params = {}
    self.assert_list = []
    self.assertex_list = []

  def set_method(self, method):
    self.method = method

  def set_params(self, params):
    for key, value in params.items():
      if key in self.__dict__:
        setattr(self, key, value)

    self.assert_list = params.get("assert", self.assert_list)
    if isinstance(self.assert_list, str):
      self.assert_list = [self.assert_list]

    self.assertex_list = params.get("assertex", self.assertex_list)
    if isinstance(self.assertex_list, str):
      self.assertex_list = [self.assertex_list]

  def get_url(self):
    if self.url_base:
      return self.url_base + self.url
    return self.url

class Http(object):
  def __init__(self, setting):
    self.result = {}
    self.exception = None
    self.setting = setting

  def run(self):
    getattr(self, "do_" + self.setting.method)()

  def has_assert(self):
    return bool(self.setting.assert_list)

  def has_assertex(self):
    return bool(self.setting.assertex_list)

  def do_get(self):
    try:
      r = requests.get(self.setting.get_url(),
          headers=self.setting.headers,
          params=self.setting.params)
      self.result['status'] = r.status_code
      self.result['content'] = r.text
      self.result['headers'] = r.headers
      self.result['encoding'] = r.encoding
      self.result['cookies'] = r.cookies
    except requests.ConnectionError as e:
      self.exception = e

  def do_post(self):
    pass

