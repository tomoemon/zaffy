# -*- coding: utf-8 -*-
from urlparse import parse_qs

def do_asquerystring(value):
  return parse_qs(str(value), True, True)
