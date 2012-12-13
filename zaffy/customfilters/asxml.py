# -*- coding: utf-8 -*-
from lxml import etree

def do_asxml(value):
  return etree.fromstring(str(value))

