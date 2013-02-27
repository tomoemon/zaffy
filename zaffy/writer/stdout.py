# -*- coding: utf-8 -*-
import sys
import util


if sys.stdout.encoding:
  # redirect された場合などに None になる
  default_out_encoding = sys.stdout.encoding
else:
  # 基本的には sys.stdout.encoding と同じ
  default_out_encoding = sys.getfilesystemencoding()


class Stdout(object):
  def open(self):
    pass

  def write(self, data):
    data = util.unicode(data, errors='replace')
    # normalizing for output
    data = data.encode(default_out_encoding, 'replace').decode(default_out_encoding, 'replace')
    sys.stdout.write(data)

  def close(self):
    pass

