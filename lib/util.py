# -*- coding: utf-8 -*-
import sys


if sys.stdout.isatty():
  default_encoding = sys.getdefaultencoding()
else:
  import locale
  default_encoding = locale.getpreferredencoding()

filesystem_encoding = sys.getfilesystemencoding()

if sys.version[:1] == '2':
  basestring = basestring
  _unicode = unicode
  _unichr = unichr

  def normalize_write_string(value, encoding):
    # python26 だと encode して出さないと文字化けした
    return value.encode(encoding, 'replace')
else:
  basestring = str
  _unicode = str
  _unichr = chr

  def normalize_write_string(value, encoding):
    return value.encode(encoding, 'replace').decode(encoding, 'replace')


def unichr(value):
  return _unichr(value)


def unicode(value, encoding=default_encoding, errors='strict'):
  if isinstance(value, _unicode):
    return value
  # @python3 オブジェクトを文字列化する際、str に errors や encoding を指定できない
  # => TypeError: coercing to str: need bytes, bytearray or buffer-like object
  try:
    return _unicode(value, encoding=encoding, errors=errors)
  except TypeError:
    return _unicode(value)


def unicode_os_string(value, encoding=filesystem_encoding, errors='strict'):
  return unicode(value, encoding, errors)


def open_yaml(filename):
  import codecs

  """ string でも file でも同じメソッドで読みこめる """
  return codecs.open(filename, encoding='utf-8')


class ArgMatchException(Exception):
  def __init__(self, error_param, error_reason):
    self.param = error_param
    self.reason = error_reason

  def __str__(self):
    return repr(self.__dict__)


def filter_args(argspec, _params):
  """ 関数の引数に適用するためのパラメータを抽出する
  argspec ArgSpec: inspect.getargspec の結果
  params dict: 関数に適用したいパラメータ
  """
  params = dict(_params)
  args = argspec.args

  if argspec.defaults:
    no_default_key_count = len(args) - len(argspec.defaults)
    required_keys = args[:no_default_key_count]
    optional_params = dict(zip(args[no_default_key_count:], argspec.defaults))
  else:
    required_keys = args
    optional_params = {}
  allow_any_params = bool(argspec.keywords)

  exists_keys = list(params.keys())
  for required_param in required_keys:
    if required_param not in params:
      raise ArgMatchException(required_param, "required")
    exists_keys.remove(required_param)

  for optional_param_name, value in optional_params.items():
    if optional_param_name in params:
      exists_keys.remove(optional_param_name)
    else:
      params[optional_param_name] = value

  if not allow_any_params and exists_keys:
    raise ArgMatchException(exists_keys[0], "unknown")

  return params


try:
  WindowsError = WindowsError
except NameError:
  WindowsError = None

