"""
   Customization of the Sphinx HTML builder to add sections to the Toctree
"""

import html
import posixpath
import re
import sys
import warnings
from os import path
from typing import Any, Dict, IO, Iterable, Iterator, List, Set, Tuple
from urllib.parse import quote

from docutils import nodes
from docutils.core import publish_parts
from docutils.frontend import OptionParser
from docutils.io import DocTreeInput, StringOutput
from docutils.nodes import Node
from docutils.utils import relative_path

from sphinx import package_dir, __display_version__
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.config import Config, ENUM
#from sphinx.deprecation import RemovedInSphinx40Warning
from sphinx.domains import Domain, Index, IndexEntry
from sphinx.environment.adapters.asset import ImageAdapter
from sphinx.environment.adapters.indexentries import IndexEntries
from sphinx.environment.adapters.toctree import TocTree
from sphinx.errors import ConfigError, ThemeError
from sphinx.highlighting import PygmentsBridge
from sphinx.locale import _, __
from sphinx.search import js_index
from sphinx.theming import HTMLThemeFactory
from sphinx.util import logging
from hashlib import md5
from sphinx.util.display import progress_message, status_iterator
from sphinx.util.docutils import new_document
from sphinx.util.fileutil import copy_asset
from sphinx.util.i18n import format_date
from sphinx.util.inventory import InventoryFile
from sphinx.util.matching import patmatch, Matcher, DOTFILES
from sphinx.util.osutil import os_path, relative_uri, ensuredir, copyfile
from sphinx.util.tags import Tags
from sphinx.writers.html import HTMLWriter, HTMLTranslator
if False:
    # For type annotation
    from typing import Type  # for python3.5.1

from sphinx.builders.html import StandaloneHTMLBuilder, Stylesheet

class DKUHTMLBuilder(StandaloneHTMLBuilder):
    name = 'dkuhtml'
    
    def __init__(self, app: Sphinx, env) -> None:
        super().__init__(app, env)

    def handle_page(self, pagename: str, addctx: Dict, templatename: str = 'page.html',
                    outfilename: str = None, event_arg: Any = None) -> None:
        ctx = self.globalcontext.copy()
        # current_page_name is backwards compatibility
        ctx['pagename'] = ctx['current_page_name'] = pagename
        ctx['encoding'] = self.config.html_output_encoding
        default_baseuri = self.get_target_uri(pagename)
        # in the singlehtml builder, default_baseuri still contains an #anchor
        # part, which relative_uri doesn't really like...
        default_baseuri = default_baseuri.rsplit('#', 1)[0]

        if self.config.html_baseurl:
            ctx['pageurl'] = posixpath.join(self.config.html_baseurl,
                                            pagename + self.out_suffix)
        else:
            ctx['pageurl'] = None

        def pathto(otheruri: str, resource: bool = False, baseuri: str = default_baseuri) -> str:  # NOQA
            if resource and '://' in otheruri:
                # allow non-local resources given by scheme
                return otheruri
            elif not resource:
                otheruri = self.get_target_uri(otheruri)
            uri = relative_uri(baseuri, otheruri) or '#'
            if uri == '#' and not self.allow_sharp_as_current_path:
                uri = baseuri
            return uri
        ctx['pathto'] = pathto

        def css_tag(css: Stylesheet) -> str:
            attrs = []
            for key in sorted(css.attributes):
                value = css.attributes[key]
                if value is not None:
                    attrs.append('%s="%s"' % (key, html.escape(value, True)))
            attrs.append('href="%s"' % pathto(css.filename, resource=True))
            return '<link %s />' % ' '.join(attrs)
        ctx['css_tag'] = css_tag

        def hasdoc(name: str) -> bool:
            if name in self.env.all_docs:
                return True
            elif name == 'search' and self.search:
                return True
            elif name == 'genindex' and self.get_builder_config('use_index', 'html'):
                return True
            return False
        ctx['hasdoc'] = hasdoc

        # BEGIN DKU SPECIFIC
        def toctree_lambda(**kwargs):
            toctree = self._get_local_toctree(pagename, **kwargs)
            toctree_lines = toctree.split("\n")

            new_lines = []
            for line in toctree_lines:
                if line.find("concepts/index.html") >= 0 or line.find("DSS concepts") >=0:
                    new_lines.append('<li class="toctree-l0">User\'s Guide</li>')
                elif line.find("time-series/index.html") >= 0 or line.find(">Time Series<") >=0:  # Avoid other titles containing Time Series
                    new_lines.append('<li class="toctree-l0">Specific Data Processing</li>')
                elif line.find("metrics-check-data-quality/index.html") >= 0 or line.find("Metrics, checks and Data Quality") >=0:
                    new_lines.append('<li class="toctree-l0">Automation &amp; Deployment</li>')
                elif line.find("installation/index.html") >=0 or (line.find("Installing and setting up") >= 0 and line.find("Govern") == -1):
                    new_lines.append('<li class="toctree-l0">Installation &amp; Administration</li>')
                elif line.find("python-api/index.html") >=0 or line.find("Python APIs") >= 0:
                    new_lines.append('<li class="toctree-l0">APIs</li>')
                elif line.find("plugins/index.html") >=0 or line.find(">Plugins") >= 0:
                    new_lines.append('<li class="toctree-l0">Other topics</li>')
                new_lines.append(line)

            new_toctree = "\n".join(new_lines)
            return new_toctree

        ctx["toctree"] = toctree_lambda
        # END DKU SPECIFIC

        self.add_sidebars(pagename, ctx)
        ctx.update(addctx)

        self.update_page_context(pagename, templatename, ctx, event_arg)
        newtmpl = self.app.emit_firstresult('html-page-context', pagename,
                                            templatename, ctx, event_arg)
        if newtmpl:
            templatename = newtmpl

        try:
            output = self.templates.render(templatename, ctx)
        except UnicodeError:
            logger.warning(__("a Unicode error occurred when rendering the page %s. "
                              "Please make sure all config values that contain "
                              "non-ASCII content are Unicode strings."), pagename)
            return
        except Exception as exc:
            raise ThemeError(__("An error happened in rendering the page %s.\nReason: %r") %
                             (pagename, exc)) from exc

        if not outfilename:
            outfilename = self.get_outfilename(pagename)
        # outfilename's path is in general different from self.outdir
        ensuredir(path.dirname(outfilename))
        try:
            with open(outfilename, 'w', encoding=ctx['encoding'],
                      errors='xmlcharrefreplace') as f:
                f.write(output)
        except OSError as err:
            logger.warning(__("error writing file %s: %s"), outfilename, err)
        if self.copysource and ctx.get('sourcename'):
            # copy the source file for the "show source" link
            source_name = path.join(self.outdir, '_sources',
                                    os_path(ctx['sourcename']))
            ensuredir(path.dirname(source_name))
            copyfile(self.env.doc2path(pagename), source_name)

def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension("sphinx.builders.html")
    app.add_builder(DKUHTMLBuilder)
