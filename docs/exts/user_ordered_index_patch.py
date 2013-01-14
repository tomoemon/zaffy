#
# -*- coding: utf-8 -*-

"""
    user_order_index_patch
    ~~~~~~~~~~~~~~~~~~~~~~

    The Sphinx extension to allow assign the order to sort terms in index.

    :copyright: (c) 2011 by Suzumizaki-Kimitaka(about Additional works)
    :license: 2-clause BSD.
"""

"""User ordered index hack for Sphinx.

This is the extension for for Sphinx( http://sphinx.pocoo.org/ ).
To use this, read the usage of extensions with/for Sphinx.
And please make sure sort_order.py and any sort_order_XX.py
(both only you want use) can be imported from this extension.

You may also have to use the extension 'yogosyu.py' to give
Yomigana string used to sort in 'genindex.html'.

Currently, this extension does hack sphinx.environment.\
BuildEnvironment.create_index, and adding no role, directive,
domain or so.

Extension work is done by Suzumizaki-Kimitaka, May 2011.
"""

import sphinx.environment
import re
import string
from itertools import groupby

_sort_order_obj = None
_name_to_yomi = None

def yomi_or_given(s):
    s = s.lower()
    if s in _name_to_yomi:
        return _name_to_yomi[s]
    return s

def keyfunc(entry, lcletters=string.ascii_lowercase + '_'):
    """Sort the index entries

    @param entry the element to sort. entry[0] is the name of it.
    @param lcletters somewhat 'unrefactored' parameter.
    @return the comparable string to sort.

    called from MyCreateIndex().

    entry[0] is the name of the entry
    entry[1] is a list.
    entry[1][0] is a list of the urls include filename,
                extention and anchor to the entry.
    entry[1][1] is the dict of subwords.

    each entry is created in add_entry() in MyCreateIndex().
    
    Important: You should complete grouping entries by THIS function.
               Otherwise, keyfunc2 makes multi headings that have same name.
    """
    global _string_of_sort_order_to_yomi
    y = yomi_or_given(entry[0])
    r = _sort_order_obj.get_string_to_sort(y)
    return r

def keyfunc2(item, letters=string.ascii_uppercase + '_'):
    """Group the entries by letter.

    @param item key:value = the string to sort order: content
    @param letters somewhat 'unrefactored' parameter.
    @return group name in which (k, v) entry belongs.

    called from MyCreateIndex().
    see Important section written in keyfunc().
    """
    k, v = item
    # hack: mutating the subitems dicts to a list in the keyfunc
    v[1] = sorted((si, se) for (si, (se, void)) in v[1].iteritems())
    return _sort_order_obj.get_group_name(yomi_or_given(k))

# ========================================================
# Hacking functions
# ========================================================

def my_env_buildenv_create_index(self, builder, group_entries=True,
                                 _fixre=re.compile(r'(.*) ([(][^()]*[)])')):
    """Hack function to alter sphinx.environment.BuildEnvironment.create_index

    In real, this function is almost same except:
    - keyfunc and keyfunc2 are not inner function
    - setup _name_to_yomi dictionary at first
    """
    global _name_to_yomi
    _name_to_yomi = {}
    for k, v in self.domaindata['std']['objects'].iteritems():
        if not isinstance(v[1], basestring):
            _name_to_yomi[k[1]] = v[1][1]
    new = {}
    
    def add_entry(word, subword, dic=new):
        entry = dic.get(word)
        if not entry:
            dic[word] = entry = [[], {}]
        if subword:
            add_entry(subword, '', dic=entry[1])
        else:
            try:
                entry[0].append(builder.get_relative_uri('genindex', fn)
                                + '#' + tid)
            except NoUri:
                pass

    for fn, entries in self.indexentries.iteritems():
        # new entry types must be listed in directives/other.py!
        for type, value, tid, alias in entries:
            if type == 'single':
                try:
                    entry, subentry = value.split(';', 1)
                except ValueError:
                    entry, subentry = value, ''
                if not entry:
                    self.warn(fn, 'invalid index entry %r' % value)
                    continue
                add_entry(entry.strip(), subentry.strip())
            elif type == 'pair':
                try:
                    first, second = map(lambda x: x.strip(),
                                        value.split(';', 1))
                    if not first or not second:
                        raise ValueError
                except ValueError:
                    self.warn(fn, 'invalid pair index entry %r' % value)
                    continue
                add_entry(first, second)
                add_entry(second, first)
            elif type == 'triple':
                try:
                    first, second, third = map(lambda x: x.strip(),
                                               value.split(';', 2))
                    if not first or not second or not third:
                        raise ValueError
                except ValueError:
                    self.warn(fn, 'invalid triple index entry %r' % value)
                    continue
                add_entry(first, second+' '+third)
                add_entry(second, third+', '+first)
                add_entry(third, first+' '+second)
            else:
                self.warn(fn, 'unknown index entry type %r' % type)
    newlist = new.items()
    newlist.sort(key = keyfunc)

    if group_entries:
        # fixup entries: transform
        #   func() (in module foo)
        #   func() (in module bar)
        # into
        #   func()
        #     (in module foo)
        #     (in module bar)
        oldkey = ''
        oldsubitems = None
        i = 0
        while i < len(newlist):
            key, (targets, subitems) = newlist[i]
            # cannot move if it has subitems; structure gets too complex
            if not subitems:
                m = _fixre.match(key)
                if m:
                    if oldkey == m.group(1):
                        # prefixes match: add entry as subitem of the
                        # previous entry
                        oldsubitems.setdefault(m.group(2), [[], {}])[0].\
                                    extend(targets)
                        del newlist[i]
                        continue
                    oldkey = m.group(1)
                else:
                    oldkey = key
            oldsubitems = subitems
            i += 1

    return [(key, list(group))
            for (key, group) in groupby(newlist, keyfunc2)]

# ========================================================
# Initializing functions
# ========================================================

def determine_sort_order(app):
    """Determine sort order used in this module

    Called by Sphinx, on the event 'bulider-inited'.
    """
    global _sort_order_obj
    import sort_order
    _sort_order_obj = sort_order.get_sort_order(app.config)
    if _sort_order_obj.__class__ == sort_order.SortOrderLegacy:
        print ('user_ordered_index_patch.py: Using SortOrderLegacy.')
    return

def setup(app):
    """Extends Sphinx as we want

    @param app sphinx.application.Sphinx object to use add builder or so.
    """
    sphinx.environment.BuildEnvironment.create_index = my_env_buildenv_create_index
    app.connect('builder-inited', determine_sort_order)
    return
    
