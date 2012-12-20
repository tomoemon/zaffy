# -*- coding: utf-8 -*-
from cgi import parse_qs

def do_asquery(value):
    return parse_qs(str(value), True, True)
