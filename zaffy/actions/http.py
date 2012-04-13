# -*- coding: utf-8 -*-
import requests

class Http(object):
  default_params = {"url":"", "url_prefix":"", "url_suffix":"", "headers":{}, "params":{}}

  def _get_url(self, params):
    result = params.url
    if params.url_prefix:
      result = params.url_prefix + result
    if params.url_suffix:
      result = result + params.url_suffix
    return result

  def do_get(self):
    params = self.setting.params
    r = requests.get(self._get_url(params),
        headers=params.headers,
        params=params.params)
    self.result['status'] = r.status_code
    self.result['content'] = r.text
    self.result['headers'] = r.headers
    self.result['encoding'] = r.encoding
    self.result['cookies'] = r.cookies

  def do_post(self):
    pass

