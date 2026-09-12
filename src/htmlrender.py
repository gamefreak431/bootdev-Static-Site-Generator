"""Rendering: parsed markdown -> an HTMLNode tree.

This is the only module that decides HTML tags. It imports the parsers; the
parsers never import it.

NOTE: the line patterns imported from blockparse below are a temporary leak --
this module still strips markdown markers itself. A later step moves that
stripping into blockparse, after which this module needs no markdown knowledge
at all. When the blockparse import below reads only `BlockType`, the parse/render
boundary is clean.
"""

import re

from blockparse import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    OLIST_LINE_PATTERN,
    QUOTE_LINE_PATTERN,
    ULIST_LINE_PATTERN,
)
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

def block_type_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    match block_type:
        case BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block)
            html_children = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return ParentNode(tag="p", children=html_children)
        case BlockType.HEADING:
            heading_level = len(re.match(r"^(#+)\s", block).group(1))
            heading_text = re.sub(r"^#{1,6}\s", "", block)
            text_nodes = text_to_textnodes(heading_text)
            html_children = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return ParentNode(tag=f"h{heading_level}", children=html_children)
        case BlockType.CODE:
            code_content = "\n".join(block.split("\n")[1:-1])
            return ParentNode(tag="pre", children=[LeafNode(tag="code", value=code_content)])
        case BlockType.QUOTE:
            quote_lines = [re.sub(QUOTE_LINE_PATTERN, "", line) for line in block.split("\n")]
            quote_text = "\n".join(quote_lines)
            text_nodes = text_to_textnodes(quote_text)
            html_children = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return ParentNode(tag="blockquote", children=html_children)
        case BlockType.ULIST:
            list_items = [re.sub(ULIST_LINE_PATTERN, "", line) for line in block.split("\n")]
            html_children = []
            for item in list_items:
                text_nodes = text_to_textnodes(item)
                li_children = [text_node_to_html_node(text_node) for text_node in text_nodes]
                html_children.append(ParentNode(tag="li", children=li_children))
            return ParentNode(tag="ul", children=html_children)
        case BlockType.OLIST:
            list_items = [re.sub(OLIST_LINE_PATTERN, "", line) for line in block.split("\n")]
            html_children = []
            for item in list_items:
                text_nodes = text_to_textnodes(item)
                li_children = [text_node_to_html_node(text_node) for text_node in text_nodes]
                html_children.append(ParentNode(tag="li", children=li_children))
            return ParentNode(tag="ol", children=html_children)
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert a markdown string to an HTML node.
    Args:
        markdown (str): The markdown string to convert.
    Returns:
        ParentNode: The HTML node representing the markdown.
    """
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_type_to_html_node(block, block_type)
        html_nodes.append(node)
    return ParentNode(tag="div", children=html_nodes)