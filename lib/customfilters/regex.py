# -*- coding: utf-8 -*-
import re
import util


uni = util.unicode


def do_regex_search(value, pattern):
    return re.search(uni(pattern), uni(value))


def do_regex_match(value, pattern):
    return re.match(uni(pattern), uni(value))

