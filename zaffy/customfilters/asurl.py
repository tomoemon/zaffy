# -*- coding: utf-8 -*-
from urlparse import urlparse, parse_qs, ParseResult

def do_asurl(value):
  parsed = urlparse(str(value))
  response = ParseResultWithQuery(parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)
  return response

class ParseResultWithQuery(ParseResult):
  @property
  def queries(self):
    return parse_qs(self.query)
