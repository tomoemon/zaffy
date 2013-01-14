#
# -*- coding: utf-8 -*-

"""
    yogosyu
    ~~~~~~~

    The Sphinx extension to provide yomigana to 'glossary'.

    :copyright: (c) 2011 by Suzumizaki-Kimitaka(about Additional works)
    :license: 2-clause BSD.
"""

"""The yogosyu extension, 'glossary' enhancement for Sphinx

This is the extension for Sphinx( http://sphinx.pocoo.org/ ).
To use this, read the usage of extensions with/for Sphinx.
And please make sure sort_order.py and any sort_order_XX.py
(both only you want use) can be imported from this extension.

You should also use the extension 'user_ordered_index_patch.py'
to make same sort order in 'genindex.html'.

This extension adds 'yogosyu' Directive.
The Directive bases on sphinx.domains.std.Glossary, and adds
Yomigana feature.

Yomigana is 'How to read kanzi (or so), written in Kana'.
Kanzi(kanji) is known CJK/CJKV Ideographs in Unicode Standard,
and Kana is known the set includes Hiragana and Katakana.

We should use Yomigana to sort Japanese words, instead of
using the code points of the Unicode.

In addtion, we should know the needs, each end-user may want
to use different sort order:
- Small form first or Normal form first(e.g. U+3041 and U+3042)
- How to order symbols and alphabets
- How to treat separating symbols
  - Simply ignore, go first or go last.
- Or native order in ANY language.

As shown last in above, 'sort order' feature can be required any
language, even Yomigana itself is required by only severals.

You can inherit SortOrderBase or SortOrderLegacyLike classes
provided with sort_order.py, and use as the generic extension.
When 'language' configure is XX in your conf.py and the file
named sort_order_XX.py exists, this module automatically
imports it.

If suitable extension not exist, this module sort the word
just Sphinx 1.0.7 or prior does by using SortOrderLegacy.

Kanzi, Hiragana, Katakana and Kana is all the words to talk
about Japanese, but ofcourse you can use this feature if you
have the needs.

Yomigana is given after 'yomimark' in the term, not some inline
markup or so, because there can be the case almost all entries
requires Yomigana, especially any *cultural* works.

'yomimark' is the option, so that it goes besides 'sorted'.

'yomimark' can be "single_char_or_whitespace_or_unicode".
the acceptable words are defined docutils.parsers.rst.\
directives.__init__.py like follows:
- one of the words: tab space
- any single unicode character except white-spaces
  - the character itself, or the code point represented by:
  - the decimal number
  - the hexadecimal number prefixed x, \\x, U+, u, or \\u
  - XML style like &#x262E;

The every term is splited by yomimark. 1st is the term itself,
2nd is treated as Yomigana. Currently 3rd and follower is
simply ignored, but using this way, the 'mono ruby' may be
supported for the future. (see HTML ruby module for example.)

Not all the entry have to give yomigana. Such entries treat as
the name of entry and the yomigana of it are same string.

Yomigana itself is currently not shown in builded HTML files.
They're only used to sort.

Extension work is done by Suzumizaki-Kimitaka, May 2011.
"""

from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from docutils import nodes
from sphinx.util.compat import Directive
from sphinx import addnodes

_sort_order_obj = None # Place Holder, and internal only.

class Yogosyu(Directive):
    """Yomigana featured version of sphinx.domains.std.Glossary

    The option 'yomimark' is added.
    """

    # root base class Directive is defined docutils.parsers.rst.__init__.py.
    # option parser functions defined docutils.parsers.rst.directives.py.

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'sorted': directives.flag,
        'yomimark': directives.single_char_or_whitespace_or_unicode
    }
 
    def run(self):
        """Inherit sphinx.util.compatDerective.run

        Base codes are copied from sphinx.domains.std.Glossary.
        """
        env = self.state.document.settings.env
        objects = env.domaindata['std']['objects']
        gloss_entries = env.temp_data.setdefault('gloss_entries', set())
        node = addnodes.glossary()
        node.document = self.state.document

        # This directive implements a custom format of the reST definition list
        # that allows multiple lines of terms before the definition.  This is
        # easy to parse since we know that the contents of the glossary *must
        # be* a definition list.

        # first, collect single entries
        entries = []
        in_definition = True
        was_empty = True
        messages = []
        for line, (source, lineno) in zip(self.content, self.content.items):
            # empty line -> add to last definition
            if not line:
                if in_definition and entries:
                    entries[-1][1].append('', source, lineno)
                was_empty = True
                continue
            # unindented line -> a term
            if line and not line[0].isspace():
                # first term of definition
                if in_definition:
                    if not was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary term must be preceded by empty line',
                            source=source, line=lineno))
                    entries.append(([(line, source, lineno)], ViewList()))
                    in_definition = False
                # second term and following
                else:
                    if was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary terms must not be separated by empty '
                            'lines', source=source, line=lineno))
                    entries[-1][0].append((line, source, lineno))
            else:
                if not in_definition:
                    # first line of definition, determines indentation
                    in_definition = True
                    indent_len = len(line) - len(line.lstrip())
                entries[-1][1].append(line[indent_len:], source, lineno)
            was_empty = False

        # now, parse all the entries into a big definition list
        items = []
        for terms, definition in entries:
            termtexts = []
            termnodes = []
            system_messages = []
            ids = []
            for line, source, lineno in terms:
                # split yomi from entry name
                yomi = line
                if 'yomimark' in self.options:
                    yomimark = self.options['yomimark']
                    line_and_yomi = line.split(yomimark)
                    line = line_and_yomi[0]
                    if len(line_and_yomi) > 1:
                        yomi = line_and_yomi[1]
                # parse the term with inline markup
                res = self.state.inline_text(line, lineno)
                system_messages.extend(res[1])

                # get a text-only representation of the term and register it
                # as a cross-reference target
                tmp = nodes.paragraph('', '', *res[0])
                termtext = tmp.astext()
                new_id = 'term-' + nodes.make_id(termtext)
                if new_id in gloss_entries:
                    new_id = 'term-' + str(len(gloss_entries))
                gloss_entries.add(new_id)
                ids.append(new_id)
                objects['term', termtext.lower()] = env.docname, (new_id, yomi)
                termtexts.append(termtext)
                # add an index entry too
                indexnode = addnodes.index()
                indexnode['entries'] = [('single', termtext, new_id, 'main')]
                termnodes.append(indexnode)
                termnodes.extend(res[0])
                termnodes.append(addnodes.termsep())
            # make a single "term" node with all the terms, separated by termsep
            # nodes (remove the dangling trailing separator)
            term = nodes.term('', '', *termnodes[:-1])
            term['ids'].extend(ids)
            term['names'].extend(ids)
            term += system_messages

            defnode = nodes.definition()
            self.state.nested_parse(definition, definition.items[0][1], defnode)

            items.append((termtexts,
                          nodes.definition_list_item('', term, defnode),
                          yomi))

        if 'sorted' in self.options:
            items.sort(key = self.get_sort_entry)

        dlist = nodes.definition_list()
        dlist['classes'].append('glossary')
        dlist.extend(item[1] for item in items)
        node += dlist
        return messages + [node]

    def get_sort_entry(self, entry):
        """Get the string to sort binded/instead of the given entry

        Called by run(), only when 'sorted' is given.
        """
        return _sort_order_obj.get_string_to_sort(entry[2])

# ========================================================
# Hacking functions
# ========================================================

def my_make_refnode(builder, fromdocname, todocname, targetid, child, title=None):
    """Shortcut to create a reference node

    This is hacking function to replace sphinx.util.nodes.make_refnode.
    """
    if isinstance(targetid, tuple):
        targetid = targetid[0]
    node = nodes.reference('', '', internal=True)
    if fromdocname == todocname:
        node['refid'] = targetid
    else:
        node['refuri'] = (builder.get_relative_uri(fromdocname, todocname)
                          + '#' + targetid)
    if title:
        node['reftitle'] = title
    node.append(child)
    return node

def my_std_domain_get_objects(self):
    """Collect and return iterators of objects

    This is hacking function to replace
    sphinx.domains.std.StandardDomain.get_objects.
    """
    for (prog, option), info in self.data['progoptions'].iteritems():
        yield (option, option, 'option', info[0], info[1], 1)
    for (type, name), info in self.data['objects'].iteritems():
        if isinstance(info[1], tuple):
            yield (name, name, type, info[0], info[1][0],
                   self.object_types[type].attrs['searchprio'])
        else:
            yield (name, name, type, info[0], info[1],
                   self.object_types[type].attrs['searchprio'])
    for name, info in self.data['labels'].iteritems():
        yield (name, info[2], 'label', info[0], info[1], -1)

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
        print ('yogosyu.py: Using SortOrderLegacy.')
    return

def setup(app):
    """Extends Sphinx as we want

    Called from Sphinx to extend.
    @param app sphinx.application.Sphinx object to use add builder or so.
    """
    app.add_directive('yogosyu', Yogosyu)
    app.add_directive(u'用語集', Yogosyu) # 'yogosyu' written in original.
    app.connect('builder-inited', determine_sort_order)

    # make sure import sphinx.util.nodes first, because
    # domains.std refers make_refnode by using the form
    # 'from sphinx.util.nodes import make_refnode'
    import sphinx.util.nodes
    sphinx.util.nodes.make_refnode = my_make_refnode
    import sphinx.domains.std    
    sphinx.domains.std.make_refnode = my_make_refnode
    sphinx.domains.std.StandardDomain.get_objects = my_std_domain_get_objects
    return
    
