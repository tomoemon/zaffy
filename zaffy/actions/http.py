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
      optional={
        'headers':{},
        'params':{},
        'no_content':False, # True にすると header のみ取得する
        'binary_content':False, # content をバイナリとして取得する
        'save_file':None # content をファイルに保存してメモリ上に持たない (binary_content=Trueとして扱う)
        }
      )

  def _create_result(self, params, response):
    result = {}
    result['status'] = response.status_code
    result['headers'] = response.headers
    result['encoding'] = response.encoding
    result['cookies'] = response.cookies
    result['content'] = self._create_content(params, response)
    return result

  def _create_content(self, params, response):
    if not params.no_content:
      if params.save_file:
        fp = open(params.save_file, "wb")
        for line in response.iter_lines():
          fp.write(line)
        fp.close()
      else:
        return response.content if params.binary_content else response.text
    return ''

  def do_get(self, params):
    r = requests.get(params.url,
          headers=params.headers,
          params=params.params)
    self.result = self._create_result(params, r)

  def do_post(self, params):
    r = requests.post(params.url,
          headers=params.headers,
          data=params.params)
    self.result = self._create_result(params, r)

