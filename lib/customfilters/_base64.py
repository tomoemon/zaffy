# -*- coding: utf-8 -*-
import base64
import util


def do_asbase64(value, encoding='utf-8', decoding='utf-8'):
    if not isinstance(value, util.bytes):
        value = value.encode(encoding)
    return base64.b64decode(value).decode(decoding)


def do_base64(value, encoding='utf-8', decoding='utf-8'):
    if not isinstance(value, util.bytes):
        value = value.encode(encoding)
    return base64.b64encode(value).decode(decoding)

