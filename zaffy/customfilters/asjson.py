# -*- coding: utf-8 -*-
import json

def do_asjson(value):
  return json.loads(unicode(value))

do_tocmp_on_asserting = [
  ['asjson', 0]
]
