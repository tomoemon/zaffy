# -*- coding: utf-8 -*-
try:
  # python2
  from urlparse import urlsplit, parse_qs, parse_qsl, SplitResult
except ImportError:
  # python3
  from urllib.parse import urlsplit, parse_qs, parse_qsl, SplitResult
import util


def do_asurl(value):
  parsed = urlsplit(util.unicode(value))
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
  return parse_qs(util.unicode(value), True)


def do_asurlquerylist(value):
  return parse_qsl(util.unicode(value), True)

