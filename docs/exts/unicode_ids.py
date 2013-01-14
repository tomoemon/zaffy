#
# -*- coding: utf-8 -*-

"""
    unicode_ids
    ~~~~~~~~~~~

    The Sphinx extension to allow HTML builder to use non-ASCII ids.

    :copyright: (c) 2011 by Suzumizaki-Kimitaka(about Additional works)
    :license: 2-clause BSD.
"""

"""The extension non-ascii id support for Sphinx

Both HTML4 and 5 supports Unicode standard used in url, includes
anchor.

But currently docutils (0.7) force the identifiers to ascii limited,
like #id-1234 or just snipping Unicode characters. Also, first of all,
it can't treat the filename using non-ascii characters.

Today, this behavior is just nonsence at least using HTML.
This module hacks docutils to enable
Unicode_file_name#Unicode-charctered_anchor.

Currently, this module hacks sphinx.environment./
BuildEnvironment.resolve_toctree. And because of this, just cover
characters in the set of sys.getdefaultencoding(), not all of Unicode
characters.

For Windows, you might create sitecustomize.py to call
sys.setdefaultencoding('mbcs').
See PEP 370 http://www.python.org/ dev/peps/pep-0370/ 

This hack should be rewritten especially the time to go Python 3.

Hack work is done by Suzumizaki-Kimitaka, May 2011.
"""

#
# the imports need to define alternate functions. copied from:
# environment.py
#

import os
import sys
from os import path
from docutils import nodes
from sphinx import addnodes
from sphinx.util import url_re, get_matching_docs, docname_join, \
     FilenameUniqDict, patfilter

#
# to define new builder.
#
import sphinx.builders.html

#
# to support my_make_id() function
#
import re
import docutils

#
# to define alternate functions.
#
def to_unicode(docname):
    """get unicode object with encoding sys.getfilesystemencoding()."""
    if isinstance(docname, str):
        return docname.decode(sys.getdefaultencoding(), "replace")
    return docname

#
# alternate functions.
#

def my_resolve_toctree(self, docname, builder, toctree, prune=True, maxdepth=0,
                       titles_only=False, collapse=False, includehidden=False):
    """alter 'sphinx.environment.BuildEnvironment.resolve_toctree'.

    Very long copied function but only to replace one str() with unicode() :-(

    Note: Difference of this function between 1.0.7 and 1.1pre is only 1 line.
          search to see "added 1.1".

    Original description is following:
    Resolve a *toctree* node into individual bullet lists with titles
    as items, returning None (if no containing titles are found) or
    a new node.

    If *prune* is True, the tree is pruned to *maxdepth*, or if that is 0,
    to the value of the *maxdepth* option on the *toctree* node.
    If *titles_only* is True, only toplevel document titles will be in the
    resulting tree.
    If *collapse* is True, all branches not containing docname will
    be collapsed.
    """
    if toctree.get('hidden', False) and not includehidden:
        return None

    def _walk_depth(node, depth, maxdepth):
        """Utility: Cut a TOC at a specified depth."""

        # For reading this function, it is useful to keep in mind the node
        # structure of a toctree (using HTML-like node names for brevity):
        #
        # <ul>
        #   <li>
        #     <p><a></p>
        #     <p><a></p>
        #     ...
        #     <ul>
        #       ...
        #     </ul>
        #   </li>
        # </ul>

        for subnode in node.children[:]:
            if isinstance(subnode, (addnodes.compact_paragraph,
                                    nodes.list_item)):
                # for <p> and <li>, just indicate the depth level and
                # recurse to children
                subnode['classes'].append('toctree-l%d' % (depth-1))
                _walk_depth(subnode, depth, maxdepth)

            elif isinstance(subnode, nodes.bullet_list):
                # for <ul>, determine if the depth is too large or if the
                # entry is to be collapsed
                if maxdepth > 0 and depth > maxdepth:
                    subnode.parent.replace(subnode, [])
                else:
                    # to find out what to collapse, *first* walk subitems,
                    # since that determines which children point to the
                    # current page
                    _walk_depth(subnode, depth+1, maxdepth)
                    # cull sub-entries whose parents aren't 'current'
                    if (collapse and depth > 1 and
                        'iscurrent' not in subnode.parent):
                        subnode.parent.remove(subnode)

            elif isinstance(subnode, nodes.reference):
                # for <a>, identify which entries point to the current
                # document and therefore may not be collapsed
                if subnode['refuri'] == docname:
                    if not subnode['anchorname']:
                        # give the whole branch a 'current' class
                        # (useful for styling it differently)
                        branchnode = subnode
                        while branchnode:
                            branchnode['classes'].append('current')
                            branchnode = branchnode.parent
                    # mark the list_item as "on current page"
                    if subnode.parent.parent.get('iscurrent'):
                        # but only if it's not already done
                        return
                    while subnode:
                        subnode['iscurrent'] = True
                        subnode = subnode.parent

    def _entries_from_toctree(toctreenode, separate=False, subtree=False):
        """Return TOC entries for a toctree node."""
        refs = [(e[0], to_unicode(e[1])) for e in toctreenode['entries']]
        entries = []
        for (title, ref) in refs:
            try:
                if url_re.match(ref):
                    reference = nodes.reference('', '', internal=False,
                                                refuri=ref, anchorname='',
                                                *[nodes.Text(title)])
                    para = addnodes.compact_paragraph('', '', reference)
                    item = nodes.list_item('', para)
                    toc = nodes.bullet_list('', item)
                elif ref == 'self':
                    # 'self' refers to the document from which this
                    # toctree originates
                    ref = toctreenode['parent']
                    if not title:
                        title = clean_astext(self.titles[ref])
                    reference = nodes.reference('', '', internal=True,
                                                refuri=ref,
                                                anchorname='',
                                                *[nodes.Text(title)])
                    para = addnodes.compact_paragraph('', '', reference)
                    item = nodes.list_item('', para)
                    # don't show subitems
                    toc = nodes.bullet_list('', item)
                else:
                    toc = self.tocs[ref].deepcopy()
                    self.process_only_nodes(toc, builder, ref) # added 1.1
                    if title and toc.children and len(toc.children) == 1:
                        child = toc.children[0]
                        for refnode in child.traverse(nodes.reference):
                            if refnode['refuri'] == ref and \
                                   not refnode['anchorname']:
                                refnode.children = [nodes.Text(title)]
                if not toc.children:
                    # empty toc means: no titles will show up in the toctree
                    self.warn(docname,
                              'toctree contains reference to document '
                              '%r that doesn\'t have a title: no link '
                              'will be generated' % ref, toctreenode.line)
            except KeyError:
                # this is raised if the included file does not exist
                self.warn(docname, 'toctree contains reference to '
                          'nonexisting document %r' % ref,
                          toctreenode.line)
            else:
                # if titles_only is given, only keep the main title and
                # sub-toctrees
                if titles_only:
                    # delete everything but the toplevel title(s)
                    # and toctrees
                    for toplevel in toc:
                        # nodes with length 1 don't have any children anyway
                        if len(toplevel) > 1:
                            subtrees = toplevel.traverse(addnodes.toctree)
                            toplevel[1][:] = subtrees
                # resolve all sub-toctrees
                for toctreenode in toc.traverse(addnodes.toctree):
                    i = toctreenode.parent.index(toctreenode) + 1
                    for item in _entries_from_toctree(toctreenode,
                                                      subtree=True):
                        toctreenode.parent.insert(i, item)
                        i += 1
                    toctreenode.parent.remove(toctreenode)
                if separate:
                    entries.append(toc)
                else:
                    entries.extend(toc.children)
        if not subtree and not separate:
            ret = nodes.bullet_list()
            ret += entries
            return [ret]
        return entries

    maxdepth = maxdepth or toctree.get('maxdepth', -1)
    if not titles_only and toctree.get('titlesonly', False):
        titles_only = True

    # NOTE: previously, this was separate=True, but that leads to artificial
    # separation when two or more toctree entries form a logical unit, so
    # separating mode is no longer used -- it's kept here for history's sake
    tocentries = _entries_from_toctree(toctree, separate=False)
    if not tocentries:
        return None

    newnode = addnodes.compact_paragraph('', '', *tocentries)
    newnode['toctree'] = True

    # prune the tree to maxdepth and replace titles, also set level classes
    _walk_depth(newnode, 1, prune and maxdepth or 0)

    # set the target paths in the toctrees (they are not known at TOC
    # generation time)
    for refnode in newnode.traverse(nodes.reference):
        if not url_re.match(refnode['refuri']):
            refnode['refuri'] = builder.get_relative_uri(
                docname, refnode['refuri']) + refnode['anchorname']
    return newnode

_non_id_at_ends = re.compile(u'^[-0-9]+|-+$')

def my_make_id(s):
    """Return Identifier keeping Unicode characters.

    Used to replace the function -> docutils.nodes.make_id
    """
    s = to_unicode(s.lower())
    s = u'-'.join(s.split())
    s = _non_id_at_ends.sub(u'', s)
    return s # we need unicode object, NOT str.

from sphinx.util.nodes import explicit_title_re

def my_toctree_run(self):
    """Show non existing entries of toctree

    Used to replace the function -> sphinx.directives.other.TocTree.run

    Only %r following are replaced %s to avoid unreadable string.
    """
    env = self.state.document.settings.env
    suffix = env.config.source_suffix
    glob = 'glob' in self.options

    ret = []
    # (title, ref) pairs, where ref may be a document, or an external link,
    # and title may be None if the document's title is to be used
    entries = []
    includefiles = []
    all_docnames = env.found_docs.copy()
    # don't add the currently visited file in catch-all patterns
    all_docnames.remove(env.docname)
    for entry in self.content:
        if not entry:
            continue
        if not glob:
            # look for explicit titles ("Some Title <document>")
            m = explicit_title_re.match(entry)
            if m:
                ref = m.group(2)
                title = m.group(1)
                docname = ref
            else:
                ref = docname = entry
                title = None
            # remove suffixes (backwards compatibility)
            if docname.endswith(suffix):
                docname = docname[:-len(suffix)]
            # absolutize filenames
            docname = docname_join(env.docname, docname)
            if url_re.match(ref) or ref == 'self':
                entries.append((title, ref))
            elif docname not in env.found_docs:
                ret.append(self.state.document.reporter.warning(
                    u'toctree contains reference to nonexisting '
                    u'document %s' % docname, line=self.lineno))
                env.note_reread()
            else:
                entries.append((title, docname))
                includefiles.append(docname)
        else:
            patname = docname_join(env.docname, entry)
            docnames = sorted(patfilter(all_docnames, patname))
            for docname in docnames:
                all_docnames.remove(docname) # don't include it again
                entries.append((None, docname))
                includefiles.append(docname)
            if not docnames:
                ret.append(self.state.document.reporter.warning(
                    'toctree glob pattern %s didn\'t match any documents'
                    % entry, line=self.lineno))
    subnode = addnodes.toctree()
    subnode['parent'] = env.docname
    # entries contains all entries (self references, external links etc.)
    subnode['entries'] = entries
    # includefiles only entries that are documents
    subnode['includefiles'] = includefiles
    subnode['maxdepth'] = self.options.get('maxdepth', -1)
    subnode['glob'] = glob
    subnode['hidden'] = 'hidden' in self.options
    subnode['numbered'] = 'numbered' in self.options
    subnode['titlesonly'] = 'titlesonly' in self.options
    wrappernode = nodes.compound(classes=['toctree-wrapper'])
    wrappernode.append(subnode)
    ret.append(wrappernode)
    return ret

def setup(app):
    """Extend Sphinx as we want

    @param app sphinx.application.Sphinx object to use add builder or so.
    """

    #
    # reset dirs to unicode, otherwise several 'replace(SEP, os.sep)'
    # codes make bad string with MBCS.  
    #
    app.srcdir = to_unicode(app.srcdir)
    app.confdir = to_unicode(app.confdir)
    app.outdir = to_unicode(app.outdir)
    app.doctreedir = to_unicode(app.doctreedir)

    #
    # The function forces unicode to str, so we need replace that function.
    #
    sphinx.environment.BuildEnvironment.resolve_toctree = my_resolve_toctree

    #
    # The original make_id() targets HTML 4.01 and CSS1,
    # we need replace the function to use unicode directly in identifier.
    # (when the function returns empty string, docutils.nodes.document.set_id()
    #  makes 'id1' or so.)
    #
    docutils.nodes.make_id = my_make_id

    #
    # The function forces unicode to str with '%r', so we need replace.
    #
    sphinx.directives.other.TocTree.run = my_toctree_run

    return
    
