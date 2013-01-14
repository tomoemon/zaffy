#
# -*- encoding: utf-8 -*-

"""The order definition to sort Esperanto words.

The language `esperanto` has 6 diacritical marked
alphabet. C^, G^, H^, J^, S^ and U with breve.

These characters ordered AFTER non marked chars,
such as C, G, H, J, S and U.

    :copyright: (c) 2011 by Suzumizaki-Kimitaka.
    :license: 2-clause BSD.
"""

import sort_order
import string

class SortOrderEo(sort_order.SortOrderBase):
    """The sort order for Esperanto

    We don't have to register yomigana for Esperanto,
    like sort_order_ja.py does.

    Q, W, X and Y are not used as Esperanto words, but
    some acronym may be used without translating for
    Esperanto.
    """
    eo_uppercases = u"ĈĜĤĴŜŬ"
    diacriticalmark_target = u"CGHJSU"
    eo_alluppercases = string.ascii_uppercase + eo_uppercases

    def get_string_to_sort(self, entry_name):
        s = entry_name.upper()
        s = ''.join((self.insert_space_or_hat(x) for x in s))
        if s[:1] not in self.eo_alluppercases:
            return u"\uffff" + s
        return s

    def get_group_name(self, entry_name):
        """Return the group name of the given entry"""
        s = self.get_string_to_sort(entry_name)
        if s[0] in self.eo_alluppercases:
            if s[1] == u" ":
                return s[0]
            idx = self.diacriticalmark_target.find(s[0])
            return self.eo_uppercases[idx]
        return u"Malalfabetoj"

    def insert_space_or_hat(self, c):
        """Return sortable string as Esperanto word.

        The parameter c sholud be a character, means len(c) == 1.
        Return value is string which length is 2.
        This function returns U^ for Ŭ, used internal only.
        """
        idx = self.eo_uppercases.find(c)
        return c+u" " if idx==-1 else self.diacriticalmark_target[idx]+u"^"

def get_default_sort_order(cfg):
    """Return vaild sort order as default in this module

    Called by the function that has same name
    in sort_order.py.
    """
    return SortOrderEo()

def setup(app):
    """Extends Sphinx as we want

    @param app sphinx.application.Sphinx object to use add builder or so.
    """
    sort_order.setup(app)
    app.add_config_value('sort_order', SortOrderEo(), 'env')
    return

