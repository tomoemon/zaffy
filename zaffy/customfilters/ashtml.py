# -*- coding: utf-8 -*-
from lxml import html

def do_ashtml(value):
  return html.fromstring(str(value))

