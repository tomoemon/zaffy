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
  def open(self):
    pass

  def write(self, data, option={}):
    data = util.unicode(data, errors='replace')
    # normalizing for output
    sys.stdout.write(util.normalize_write_string(data, default_out_encoding))

  def close(self):
    pass


class ColoredStdout(Stdout):
  def __init__(self):
    super(ColoredStdout, self).__init__()
    colorama.init()

  def _reset_style(self):
    self._set_style(Fore.RESET + Back.RESET + Style.RESET_ALL)

  def _set_style(self, style):
    sys.stdout.write(style)

  def write(self, data, option={}):
    style = option.get('style', "")
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
    else:
      start = Fore.RESET + Back.RESET + Style.RESET_ALL

    stripped = data.rstrip("\n")
    strip_count = len(data) - len(stripped)

    sys.stdout.write(start)
    super(ColoredStdout, self).write(stripped)
    sys.stdout.write(end + "\n" * strip_count)

