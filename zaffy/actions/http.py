# -*- coding: utf-8 -*-
import requests

class Http(object):
  default_params = {"url":"", "url_base":"", "headers":{}, "params":{}}

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

  def _get_url(self, params):
    if params.url_base:
      return params.url_base + params.url
    return params.url

  def do_get(self):
    params = self.setting.params
    try:
      r = requests.get(self._get_url(params),
          headers=params.headers,
          params=params.params)
      self.result['status'] = r.status_code
      self.result['content'] = r.text
      self.result['headers'] = r.headers
      self.result['encoding'] = r.encoding
      self.result['cookies'] = r.cookies
    except requests.ConnectionError as e:
      self.exception = e

  def do_post(self):
    pass

