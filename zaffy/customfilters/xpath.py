# -*- coding: utf-8 -*-
import lxml
import lxml.etree


def do_xpathlist(value, xpath, namespaces=None):
  """ 常に list 形式で返す """
  if getattr(value, 'xpath', None):
    root = value
  else:
    root = lxml.etree.fromstring(str(value))
  result = root.xpath(xpath, namespaces=namespaces)
  return result


def do_xpath(value, xpath, namespaces=None):
  """ 返り値が1件だけの場合は中身を取り出して返す """
  result = do_xpathlist(value, xpath, namespaces)
  if len(result) == 1:
    return result[0]
  return result

