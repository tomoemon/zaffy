# -*- coding: utf-8 -*-
import util
import yaml


class folded_unicode(util._unicode):
  pass


class literal_unicode(util._unicode):
  pass


def folded_unicode_representer(dumper, data):
  return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')


def literal_unicode_representer(dumper, data):
  return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


def tuple_representer(dumper, data):
  return dumper.represent_sequence(u'tag:yaml.org,2002:seq', data)


def unicode_representer(dumper, data):
  return dumper.represent_scalar(u'tag:yaml.org,2002:str', data)


yaml.SafeDumper.add_representer(folded_unicode, folded_unicode_representer)
yaml.SafeDumper.add_representer(literal_unicode, literal_unicode_representer)
yaml.Dumper.add_representer(folded_unicode, folded_unicode_representer)
yaml.Dumper.add_representer(literal_unicode, literal_unicode_representer)
yaml.Dumper.add_representer(tuple, tuple_representer)
yaml.Dumper.add_representer(util._unicode, unicode_representer)


def dump(obj):
  try:
    return yaml.safe_dump(obj, default_flow_style=False, allow_unicode=True)
  except yaml.representer.RepresenterError as e:
    return yaml.dump(obj, default_flow_style=False, allow_unicode=True)

