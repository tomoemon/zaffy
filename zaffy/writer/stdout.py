# -*- coding: utf-8 -*-
import sys
import util


class Stdout(object):
  def open(self):
    pass

  def write(self, data):
    data = util.unicode(data, errors='ignore')
    sys.stdout.write(data.encode(sys.stdout.encoding, errors='replace'))

  def close(self):
    pass

