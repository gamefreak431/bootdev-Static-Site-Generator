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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return IMAGE_REGEX.findall(text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return LINK_REGEX.findall(text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        last_index = 0
        for match in IMAGE_REGEX.finditer(node.text):
            if match.start() > last_index:
                new_nodes.append(TextNode(text=node.text[last_index:match.start()], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=match.group(1), text_type=TextType.IMAGE, url=match.group(2)))
            last_index = match.end()
        if last_index == 0:
            new_nodes.append(node)
        elif last_index < len(node.text):
            new_nodes.append(TextNode(text=node.text[last_index:], text_type=TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        last_index = 0
        for match in LINK_REGEX.finditer(node.text):
            start_index = match.start()
            if start_index > last_index:
                new_nodes.append(TextNode(text=node.text[last_index:start_index], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=match.group(1), text_type=TextType.LINK, url=match.group(2)))
            last_index = match.end()
        if last_index == 0:
            new_nodes.append(node)
        elif last_index < len(node.text):
            new_nodes.append(TextNode(text=node.text[last_index:], text_type=TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    # Images and links are extracted first so a URL's characters (e.g. an
    # underscore) are never mistaken for a bold/italic/code delimiter.
    # Code spans are split before bold/italic for the same reason: a code
    # span's contents are literal and shouldn't be interpreted as markdown.
    delimiters = [
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
    ]
    nodes = split_nodes_link(split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)]))
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type) or nodes
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    """Convert a markdown string to a list of markdown blocks.

    Args:
        markdown (str): The markdown string to convert.

    Returns:
        list[str]: A list of strings representing the markdown blocks.
    """
    return [line.strip() for line in markdown.split("\n\n") if line.strip() != ""]