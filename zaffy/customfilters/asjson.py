# -*- coding: utf-8 -*-
import json

def do_asjson(value):
  return json.loads(unicode(value))

def do_tojson(value):
  return json.dumps(value)

