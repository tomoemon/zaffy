# -*- coding: utf-8 -*-
import sys
_unicode = unicode
default_encoding = sys.getdefaultencoding()

def unicode(value, encoding=default_encoding, errors='strict'):
  if isinstance(value, _unicode):
    return value
  return _unicode(str(value), encoding=encoding, errors=errors)

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

  exists_keys = params.keys()
  for required_param in required_keys:
    if required_param not in params:
      raise Exception("required: " + required_param)
    exists_keys.remove(required_param)

  for optional_param_name, value in optional_params.items():
    if optional_param_name in params:
      exists_keys.remove(optional_param_name)
    else:
      params[optional_param_name] = value

  if not allow_any_params and exists_keys:
    raise Exception("unknown param: " + exists_keys[0])

  return params

