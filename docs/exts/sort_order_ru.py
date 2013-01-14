#
# -*- encoding: utf-8 -*-

"""
    sort_order_ru
    ~~~~~~~~~~~~~

    The order definition to sort (Modern) Greek words.

    Please check working correctly and fix if we need!

    :copyright: (c) 2011 by Suzumizaki-Kimitaka.
    :license: 2-clause BSD.
"""

import sort_order
import string

class SortOrderRu(sort_order.SortOrderLegacyLike):
    def etc_form(self):
        return u"Другой"

    def get_uppercases(self):
        return u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def get_default_sort_order(cfg):
    """Return vaild sort order as default in this module

    Called by the function that has same name
    in sort_order.py.
    """
    return SortOrderRu()

def setup(app):
    """Extends Sphinx as we want

    @param app sphinx.application.Sphinx object to use add builder or so.
    """
    sort_order.setup(app)
    app.add_config_value('sort_order', SortOrderRu(), 'env')
    return

