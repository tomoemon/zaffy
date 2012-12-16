# -*- coding: utf-8 -*-
import sys

class Stdout(object):
  def open(self):
    pass

  def write(self, data):
    sys.stdout.write(unicode(data))

  def close(self):
    pass

