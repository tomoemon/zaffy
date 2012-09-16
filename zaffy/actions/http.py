# -*- coding: utf-8 -*-
import requests
from baseaction import BaseAction

class Http(BaseAction):
  """ Http アクション
  port は url パラメータで http://hoge.com:8000/ のように指定する
  """
  def _create_result(self, response, no_content, binary_content, save_file):
    result = {}
    result['status'] = response.status_code
    result['headers'] = response.headers
    result['encoding'] = response.encoding
    result['cookies'] = response.cookies
    result['content'] = self._create_content(response, no_content, binary_content, save_file)
    return result

  def _create_content(self, response, no_content, binary_content, save_file):
    if not no_content:
      if save_file:
        # ファイルに保存する場合は自動的にバイナリ保存
        fp = open(save_file, "wb")
        for line in response.iter_content():
          fp.write(line)
        fp.close()
      else:
        return response.content if binary_content else response.text
    return ''

  def _http_method(self, method, url, headers, params, no_content, binary_content, save_file, ssl_verify):
    r = getattr(requests, method)(url,
          headers=headers,
          params=params,
          verify=ssl_verify)
    self.result = self._create_result(r, no_content, binary_content, save_file)

  def do_get(self, url, headers={}, params={}, no_content=False, binary_content=False, save_file=None, ssl_verify=True):
    """
    @param no_content True にすると header のみ取得する
    @param binary_content content をバイナリとして取得する
    @param save_file content をファイルに保存してメモリ上に持たない (binary_content=Trueとして扱う)
    @param ssl_verify SSL証明書のチェックをするか（自己証明書の場合はFalseじゃないと通らない）
    """
    self._http_method("get", url, headers, params, no_content, binary_content, save_file, ssl_verify)

  def do_post(self, url, headers={}, params={}, no_content=False, binary_content=False, save_file=None, ssl_verify=True):
    self._http_method("post", url, headers, params, no_content, binary_content, save_file, ssl_verify)

  def do_put(self, url, headers={}, params={}, no_content=False, binary_content=False, save_file=None, ssl_verify=True):
    self._http_method("put", url, headers, params, no_content, binary_content, save_file, ssl_verify)

  def do_delete(self, url, headers={}, params={}, no_content=False, binary_content=False, save_file=None, ssl_verify=True):
    self._http_method("delete", url, headers, params, no_content, binary_content, save_file, ssl_verify)

  def do_head(self, url, headers={}, params={}, no_content=False, binary_content=False, save_file=None, ssl_verify=True):
    self._http_method("head", url, headers, params, no_content, binary_content, save_file, ssl_verify)

  def do_patch(self, url, headers={}, params={}, no_content=False, binary_content=False, save_file=None, ssl_verify=True):
    self._http_method("patch", url, headers, params, no_content, binary_content, save_file, ssl_verify)

