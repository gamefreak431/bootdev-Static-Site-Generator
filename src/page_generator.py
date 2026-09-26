"""File I/O for the static site generator.

This module owns the parts of the pipeline that touch the filesystem, so that
the parsing and rendering modules stay pure functions of their input:

    extract   read the source markdown file and the HTML template   (here)
    transform markdown -> blocks -> HTMLNode tree                   (htmlrender)
    load      HTMLNode tree -> html string -> write to output dir  (here)

The whole transform step is reached through one call, markdown_to_html_node():
htmlrender drives blockparse (document -> marker-stripped Blocks) and
inlineparse (block content -> TextNodes) itself, so this module never imports
either parser.

Intended responsibilities:
    - copy static assets from a source directory into the output directory
    - read a markdown file and an HTML template
    - hand the markdown to markdown_to_html_node() and call .to_html()
    - substitute the rendered HTML (and the page title) into the template
    - write the finished page to its destination path
    - walk a content directory and generate a page for every markdown file

Callers pass in every path; this module doesn't know where the project's
directories are.

Nothing here should know anything about markdown syntax or HTML node classes
beyond calling markdown_to_html_node().
"""

import shutil
from pathlib import Path
from htmlrender import markdown_to_html_node
from blockparse import extract_title

def copy_static_assets(static_path: Path, public_path: Path) -> None:
    """Replace the contents of public_path with a copy of static_path.

    Args:
        static_path (Path): Directory holding the static assets to copy.
        public_path (Path): Output directory. Deleted first if it exists.
    """
    shutil.rmtree(public_path, ignore_errors=True)
    shutil.copytree(static_path, public_path)

def generate_page(source_path: Path, template_path: Path, dest_path: Path, base_path: str) -> None:
    """Generate a page from a markdown source file and an HTML template.

    Args:
        source_path (Path): Path to the source markdown file.
        template_path (Path): Path to the HTML template file.
        dest_path (Path): Path to write the generated HTML file.
        base_path (str): Base path for the generated site.
    """
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")
    # Read the source markdown file
    with open(source_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read the HTML template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTMLNode tree
    html_node_tree = markdown_to_html_node(markdown_content)

    # Render the HTMLNode tree to an HTML string
    rendered_html = html_node_tree.to_html()

    # Substitute the page title into the template
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)

    # Substitute the rendered HTML into the template
    final_html = template_content.replace("{{ Content }}", rendered_html)

    # Substitute the base path into the template
    final_html = final_html.replace('href="/', f'href="{base_path}')
    final_html = final_html.replace('src="/', f'src="{base_path}')

    # Write the finished page to its destination path
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, base_path: str) -> None:
    """Generate an HTML page for every markdown file under dir_path_content.

    The directory structure is mirrored into dest_dir_path, so
    content/blog/tom/index.md is written to <dest_dir_path>/blog/tom/index.html.

    Args:
        dir_path_content (Path): Root directory of the markdown source files.
        template_path (Path): Path to the HTML template file.
        dest_dir_path (Path): Root directory to write the generated pages to.
        base_path (str): Base path for the generated site.
    """
    for md_file in dir_path_content.rglob("*.md"):
        dest_file = (dest_dir_path / md_file.relative_to(dir_path_content)).with_suffix(".html")
        generate_page(
            source_path=md_file,
            template_path=template_path,
            dest_path=dest_file,
            base_path=base_path
        )
