# -*- coding: utf-8 -*-
from urlparse import urlparse

def do_asurl(value):
    return urlparse(str(value))
