# -*- coding: utf-8 -*-
import requests

class Http(object):
  __slots__ = ["result"]

  def __init__(self):
    self.result = {}

  def do_get(self, url, headers, params):
    r = requests.get(url, headers=headers, params=params)
    self.result['status'] = r.status_code
    self.result['content'] = r.text
    self.result['headers'] = r.headers
    self.result['encoding'] = r.encoding
    self.result['cookies'] = r.cookies

