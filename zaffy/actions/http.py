# -*- coding: utf-8 -*-
import requests
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting

class Http(BaseAction):
  """ Http アクション
  port は url パラメータで http://hoge.com:8000/ のように指定する
  """

  param_setting = ActionParamSetting(
      allow_any_params=False,
      required=['url'],
      optional={'headers':{}, 'params':{}}
      )

  def _to_result(self, response):
    result = {}
    result['status'] = response.status_code
    result['content'] = response.text
    result['headers'] = response.headers
    result['encoding'] = response.encoding
    result['cookies'] = response.cookies
    return result

  def do_get(self, params):
    r = requests.get(params.url,
          headers=params.headers,
          params=params.params)
    self.result = self._to_result(r)

  def do_post(self, params):
    r = requests.post(params.url,
          headers=params.headers,
          data=params.params)
    self.result = self._to_result(r)

