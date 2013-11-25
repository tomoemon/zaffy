# -*- coding: utf-8 -*-
import lxml
from lxml import etree, html


class _XmlNamespace(object):
  def __init__(self, xmlobj, namespaces=None):
    self.xml = xmlobj
    self.namespaces = namespaces

  def xpath(self, xpath, namespaces=None):
    ns = self.namespaces
    if namespaces:
      ns = namespaces
    return self.xml.xpath(xpath, namespaces=ns)


def do_ashtml(value):
  return _XmlNamespace(html.fromstring(str(value)))


def do_asxml(value, namespaces=None):
  return _XmlNamespace(etree.fromstring(str(value)), namespaces)


def do_xpathlist(value, xpath, namespaces=None):
  """ 常に list 形式で返す """
  if isinstance(value, _XmlNamespace):
    xml = value
  else:
    xml = do_asxml(value, namespaces)
  result = xml.xpath(xpath, namespaces)
  return result


def do_xpath(value, xpath, namespaces=None):
  """ 返り値が1件だけの場合は中身を取り出して返す """
  result = do_xpathlist(value, xpath, namespaces)
  try:
    if len(result) == 1:
      return result[0]
  except TypeError:
    # xml.xpath responds sequence of element or number (eg. count() is used)
    pass
  return result

