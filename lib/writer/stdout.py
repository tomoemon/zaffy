# -*- coding: utf-8 -*-
import sys
import util
import colorama
from colorama import Fore, Back, Style


if sys.stdout.encoding:
  # redirect された場合などに None になる
  default_out_encoding = sys.stdout.encoding
else:
  # 基本的には sys.stdout.encoding と同じ
  default_out_encoding = sys.getfilesystemencoding()


class Stdout(object):
  def __init__(self, nodebug=False):
    self.nodebug = nodebug

  def open(self):
    pass

  def debug(self, data, option={}):
    if not self.nodebug:
      option['type'] = 'debug'
      self.write(data, option)

  def write(self, data, option={}):
    data = util.unicode(data, errors='replace')
    # normalizing for output
    sys.stdout.write(util.normalize_write_string(data, default_out_encoding))

  def close(self):
    pass


class ColoredStdout(Stdout):
  def __init__(self, nodebug=False):
    super(ColoredStdout, self).__init__(nodebug)
    colorama.init()

  def write(self, data, option={}):
    style = option.get('type', "")
    start = ""
    end = Fore.RESET + Back.RESET + Style.RESET_ALL
    if style == 'error':
      start = Fore.RED + Style.BRIGHT
    elif style == 'error_result':
      start = Fore.WHITE + Back.RED + Style.BRIGHT
    elif style == 'success':
      start = Fore.GREEN + Style.BRIGHT
    elif style == 'success_result':
      start = Fore.WHITE + Back.GREEN + Style.BRIGHT
    elif style == 'debug':
      start = Fore.BLACK + Back.RESET + Style.BRIGHT
    else:
      start = Fore.RESET + Back.RESET + Style.RESET_ALL

    stripped = data.rstrip("\n")
    strip_count = len(data) - len(stripped)

    sys.stdout.write(start)
    super(ColoredStdout, self).write(stripped)
    sys.stdout.write(end + "\n" * strip_count)

