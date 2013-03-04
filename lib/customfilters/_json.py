# -*- coding: utf-8 -*-
import json
import util


def do_asjson(value):
  return json.loads(util.unicode(value))


def do_tojson(value):
  return json.dumps(value)

