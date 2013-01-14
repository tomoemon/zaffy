#
# -*- coding: utf-8 -*-

"""
    sort_order
    ~~~~~~~~~~

    The Sphinx extension to provide sort order.

    :copyright: (c) 2011 by Suzumizaki-Kimitaka.
    :license: 2-clause BSD.
"""

"""
Sort order is used by user_ordered_index_patch.py and yogosyu.py, which
extends glossary directive.

To use this feature, make your 'ext' setting in conf.py to call both
yogosyu and user_ordered_index_patch.py.

This module itself is NOT extension.
Just for subclasses or another extensions.

Any sort_order_LANG.py should have the function
get_default_sort_order(cfg) to be called from same name function in this
source code, and the function should return the object which class inherits
SortOrderBase.
"""

import unicodedata
import string

class SortOrderBase(object):
    """Base class of any SortOrder-s

    Any sort order should be given by inheriting this class.
    SortOrderLegacy is defined in this sort_order.py and
    you can refer sort_order_ja.py as sample implementation.
    """

    def get_string_to_sort(self, name, yomi_dict = {}):
        """Return the string to sort instead of given name

        @param name the name of the entry
        @param yomi_dict name to yomigana dictionary
        @return the string to sort the given entry

        If the name doesn't have yomigana or no need to sorted string,
        just return given parameter.
        But note, even default legacy sorting makes altered string
        to sort. see SortOrderLegacy implementation.

        And also, make sure the returning strings already make
        grouped block to make the block name headings only one in
        genindex.html.
        """
        return name

    def get_group_name(self, entry_name, yomi_dict = {}):
        """Return the group name of the given entry

        Currently, grouping should be done by get_string_to_sort()
        function. See SortOrderLegacy implementation.
        """
        return entry_name[0]


class SortOrderLegacy(SortOrderBase):
    """Perform sort order given like Sphinx 1.0.7 or prior"""

    def get_string_to_sort(self, name, yomi_dict = {}):
        """Return the string to sort instead of given name

        To make the grouping done, making lowercased,
        'NFD' normalization and symbols first hack.
        """
        lcletters = string.ascii_lowercase + '_'
        lckey = unicodedata.normalize('NFD', name.lower())
        if lckey[0:1] in lcletters:
            return chr(127) + lckey
        return lckey

    def get_group_name(self, entry_name, yomi_dict = {}):
        """Return the group name of the given entry

        This class/function gives just only English specific
        sort_order. Alphabet is limited only in ascii and
        force all characters NFD normalization.
        """        
        letters = string.ascii_uppercase + '_'
        letter = unicodedata.normalize('NFD', entry_name)[0].upper()
        if letter in letters:
            return letter
        else:
            return 'Symbols'


class SortOrderLegacyLike(SortOrderBase):
    """Base class for lauguages similar to latin."""

    def get_string_to_sort(self, name, yomi_dict = {}):
        s = unicodedata.normalize('NFD', name).upper()
        if s[:1] not in self.get_uppercases():
            return u"\uffff" + s
        return s

    def get_group_name(self, entry_name, yomi_dict = {}):
        """Return the group name of the given entry"""
        s = self.get_string_to_sort(entry_name)
        if s[0] in self.get_uppercases():
            return s[0]
        return self.etc_form()

    def etc_form(self):
        """Return the word 'etc.' in your language

        Override this.
        """
        return u"Etc."

    def get_uppercases(self):
        """Return uppercased characters used in your language

        Override this.
        """
        return string.ascii_uppercase

def get_default_sort_order(cfg):
    """Return default sort order of the language assigned in conf.py

    @param cfg app.config, builder.config, etc.
    @return the object of the class inherits SortOrderBase.

    Called by another extensions.
    See also get_sort_order() function.
    """
    try:
        lang = cfg.language
    except:
        lang = None
    if not lang:
        e = 'sort_order.py: ' + \
            'No SortOrderBase object applied,' +  \
            ' and no language assigned.' +  \
            ' using SortOrderLegacy.'
        print e
        return SortOrderLegacy()
    import_target = 'sort_order_' + lang
    try:
        exec 'import ' + import_target + ' as local_sort_order'
    except ImportError:
        e = 'sort_order.py: ' + \
            'No SortOrderBase object applied,' + \
            ' and module {0} not found.' + \
            ' using SortOrderLegacy.'
        print e.format(import_target)
        return SortOrderLegacy()
    return local_sort_order.get_default_sort_order(cfg)


def get_sort_order(cfg):
    """Return sort order object with current configure

    @param cfg app.config, builder.config, etc.
    @return the object of the class inherits SortOrderBase.

    More convenient function than get_default_sort_order().
    Called by another extensions.
    """
    try:
        r = cfg.sort_order
        try:
            assert isinstance(r, SortOrderBase)
            return r
        except:
           print 'get_sort_order.py: ' + \
                 'config "sort_order" should be' + \
                 'the object of SortOrderBase.' 
    except:
        pass
    return get_default_sort_order(cfg)


def setup(app):
    """Called from Sphinx to extend.

    @param app sphinx.application.Sphinx object to use add builder or so.
    """
    # place holder. Do nothing.
    return
