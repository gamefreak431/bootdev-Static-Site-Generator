"""File I/O for the static site generator.

STUB — not implemented yet.

This module owns the parts of the pipeline that touch the filesystem, so that
the parsing and rendering modules stay pure functions of their input:

    extract   read the source markdown file and the HTML template   (here)
    transform markdown -> blocks -> HTMLNode tree                   (htmlrender)
    load      HTMLNode tree -> html string -> write to public/      (here)

The whole transform step is reached through one call, markdown_to_html_node():
htmlrender drives blockparse (document -> marker-stripped Blocks) and
inlineparse (block content -> TextNodes) itself, so this module never imports
either parser.

Intended responsibilities:
    - copy static assets from a source directory into public/
    - read a markdown file and an HTML template
    - hand the markdown to markdown_to_html_node() and call .to_html()
    - substitute the rendered HTML (and the page title) into the template
    - write the finished page to its destination path

Nothing here should know anything about markdown syntax or HTML node classes
beyond calling markdown_to_html_node().
"""

import shutil
from pathlib import Path

from htmlrender import markdown_to_html_node
