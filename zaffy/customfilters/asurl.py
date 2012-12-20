# -*- coding: utf-8 -*-
from urlparse import urlsplit, parse_qs, parse_qsl, SplitResult

def do_asurl(value):
  parsed = urlsplit(unicode(value))
  response = SplitResultWithQuery(parsed.scheme, parsed.netloc,
      parsed.path, parsed.query, parsed.fragment)
  return response

class SplitResultWithQuery(SplitResult):
  @property
  def param(self):
    return parse_qs(self.query, True)

  @property
  def paramlist(self):
    return parse_qsl(self.query, True)

  @property
  def hash(self):
    return self.fragment

def do_asurlquery(value):
  return parse_qs(unicode(value), True)

def do_asurlquerylist(value):
  return parse_qsl(unicode(value), True)

