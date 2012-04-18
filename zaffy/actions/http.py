# -*- coding: utf-8 -*-
import requests
from baseaction import BaseAction

class Http(BaseAction):
  """ Http アクション
  port は url パラメータで http://hoge.com:8000/ のように指定する
  """
  default_params = {
    "url":"",
    "url_prefix":"",
    "url_suffix":"",
    "headers":{},
    "params":{}
  }

  def _get_url(self, params):
    result = params.url
    if params.url_prefix:
      result = params.url_prefix + result
    if params.url_suffix:
      result = result + params.url_suffix
    return result

  def _to_result(self, response):
    result = {}
    result['status'] = response.status_code
    result['content'] = response.text
    result['headers'] = response.headers
    result['encoding'] = response.encoding
    result['cookies'] = response.cookies
    return result

  def do_get(self):
    params = self.setting.params
    r = requests.get(self._get_url(params),
        headers=params.headers,
        params=params.params)
    self.result = self._to_result(r)

  def do_post(self):
    params = self.setting.params
    r = requests.post(self._get_url(params),
        headers=params.headers,
        data=params.params)
    self.result = self._to_result(r)

