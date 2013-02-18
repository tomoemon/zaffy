# -*- coding: utf-8 -*-
import csv
import io
import util
""" csvフィルター
csv, _csv というモジュールはすでに存在するので separate という名前にしている
"""


def do_ascsv(value, delim=',', quote='"'):
  reader = csv.reader(io.StringIO(util.unicode(value)), delimiter=delim, quotechar=quote)
  return list(reader)

