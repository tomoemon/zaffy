# -*- coding: utf-8 -*-
import datetime
import pprint
import re
import util

_UNICODE_REGEXP = re.compile(r"\\u([0-9a-f]{4})")


class DebugPrinter(object):

  def __init__(self, formatter, scenario):
    self.formatter = formatter
    self.scenario = scenario

  def smart_write(self, params):
    """ 与えられた文字列値を python の基本データ型のリテラルとして解釈した後に print する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: debug.print
         v1: "1 + 2 + 3" #=> 6 と表示
         v2: "[1, 2] + [3, 4]" #=> [1, 2, 3, 4] と表示
    """
    dump = {}
    for key, value in params.items():
      if isinstance(value, util.basestring):
        try:
          # debug中で任意のコードが実行されないように、
          # ビルトイン関数を無効にしてリテラルと一部の式だけ解釈できるようにする
          dump[key] = eval(value, {'__builtins__':{}}, {})
        except Exception:
          dump[key] = util.unicode(value)
      else:
        dump[key] = value
    self.write(dump)

  def write(self, params):
    params['__file__'] = self.scenario.setting.filename
    params['__index__'] = self.scenario.action_index
    self.formatter.debug("\nDEBUG - {0}".format(datetime.datetime.now()))
    self.formatter.debug(self._pp(params))

  @classmethod
  def _pp(cls, obj):
    # 日本語を pprint で表示しようとすると、
    # 以下のように文字コードで表示されてしまうため置換する
    # 'row1': u'\u6570\u5b66\u30ac\u30fc\u30eb'
    pstr = pprint.pformat(obj, width=80, indent=2)
    return _UNICODE_REGEXP.sub(lambda x: util.unichr(int("0x" + x.group(1), 16)), pstr)

