"""Rendering: parsed markdown -> an HTMLNode tree.

This is the only module that decides HTML tags. It imports the parsers; the
parsers never import it.

It holds no markdown knowledge: it never imports `re` and never sees a `#`, a
`>` or a `-`. The parsers hand it content with every marker already stripped,
so its only job is choosing a tag and nesting the children.
"""

from blockparse import Block, BlockType, markdown_to_blocks, parse_block
from inlineparse import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Render a single inline TextNode as its HTML leaf.
    Args:
        text_node (TextNode): The text node to render.
    Returns:
        LeafNode: The HTML leaf node for that text node.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError(f"URL must be provided for link text type at: {text_node.text}")
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError(f"URL must be provided for image text type at: {text_node.text}")
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")

def block_to_html_node(block: Block) -> ParentNode:
    """Render a parsed block as its HTML element, inline markup included.

    This is where the two halves of the pipeline meet: the block decides the
    parent tag, and `_inline_children` runs the block's content through
    `text_to_textnodes` and renders each TextNode as a LeafNode. There is no
    separate inline-parsing stage between blockparse and here -- the whole
    inline pass happens inside this function's children.

    Args:
        block (Block): The classified, marker-stripped block.
    Returns:
        ParentNode: The HTML element for that block, with its inline markup
            already rendered as LeafNode children.
    """
    match block.type:
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=_inline_children(block.content))
        case BlockType.HEADING:
            return ParentNode(tag=f"h{block.level}", children=_inline_children(block.content))
        case BlockType.CODE:
            return ParentNode(tag="pre", children=[LeafNode(tag="code", value=block.content)])
        case BlockType.QUOTE:
            return ParentNode(tag="blockquote", children=_inline_children(block.content))
        case BlockType.ULIST:
            return ParentNode(tag="ul", children=_list_items(block.content))
        case BlockType.OLIST:
            # <ol> numbers its own items, so ordered and unordered lists render
            # identically once their markers are gone.
            return ParentNode(tag="ol", children=_list_items(block.content))
        case _:
            raise ValueError(f"Unsupported block type: {block.type}")

def _inline_children(text: str) -> list[LeafNode]:
    """Parse inline markdown in a string and render each piece as an HTML leaf."""
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]

def _list_items(items: list[str]) -> list[ParentNode]:
    """Render each already-stripped list item as an <li>."""
    return [ParentNode(tag="li", children=_inline_children(item)) for item in items]

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert a markdown string to an HTML node.
    Args:
        markdown (str): The markdown string to convert.
    Returns:
        ParentNode: The HTML node representing the markdown.
    """
    return ParentNode(
        tag="div",
        children=[block_to_html_node(parse_block(block)) for block in markdown_to_blocks(markdown)],
    )
