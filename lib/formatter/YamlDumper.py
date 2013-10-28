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


yaml.SafeDumper.add_representer(folded_unicode, folded_unicode_representer)
yaml.SafeDumper.add_representer(literal_unicode, literal_unicode_representer)


def dump(obj):
  return yaml.safe_dump(obj, default_flow_style=False)

