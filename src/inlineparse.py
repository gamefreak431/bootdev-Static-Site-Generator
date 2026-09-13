"""Inline markdown parsing: a text string -> a list of TextNodes.

Knows about inline markdown syntax (delimiters, images, links) and nothing
about HTML. Produces TextNodes; something else decides what to render them as.
"""

import re

from textnode import TextNode, TextType


IMAGE_REGEX = re.compile(r'!\[(.*?)\]\((.*?)\)')
LINK_REGEX = re.compile(r'(?<!!)\[(.*?)\]\((.*?)\)')

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split text nodes by a delimiter and return a list of new text nodes.
    Args:
        old_nodes (list[TextNode]): The list of old text nodes to split.
        delimiter (str): The delimiter to split the text nodes by.
        text_type (TextType): The type of the new text nodes.
    Returns:
        list[TextNode]: A list of new text nodes after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text: {node.text}")
        parts = node.text.split(delimiter)
        new_nodes.extend(
            TextNode(text=part, text_type=text_type if i % 2 else TextType.TEXT)
            for i, part in enumerate(parts) if part
        )
    return new_nodes

def _split_link_or_image(old_nodes: list[TextNode], regex: re.Pattern[str], text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        last_index = 0
        for match in regex.finditer(node.text):
            if match.start() > last_index:
                new_nodes.append(TextNode(text=node.text[last_index:match.start()], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=match.group(1), text_type=text_type, url=match.group(2)))
            last_index = match.end()
        if last_index == 0:
            new_nodes.append(node)
        elif last_index < len(node.text):
            new_nodes.append(TextNode(text=node.text[last_index:], text_type=TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    """Images and links are extracted first so a URL's characters 
    (e.g. an underscore) are never mistaken for a bold/italic/code delimiter.
    Code spans are split before bold/italic for the same reason: 
    a code span's contents are literal and shouldn't be interpreted as markdown.
    """
    delimiters = [
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
    ]

    nodes = _split_link_or_image([TextNode(text=text, text_type=TextType.TEXT)], IMAGE_REGEX, TextType.IMAGE)
    nodes = _split_link_or_image(nodes, LINK_REGEX, TextType.LINK)
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type) or nodes
    return nodes
