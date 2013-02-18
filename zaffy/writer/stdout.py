# -*- coding: utf-8 -*-
import sys
import util


class Stdout(object):
  def open(self):
    pass

  def write(self, data):
    data = util.unicode(data, errors='replace')
    # normalizing for output
    data = data.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
    sys.stdout.write(data)

  def close(self):
    pass

