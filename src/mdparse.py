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
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text: {node.text}")
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            new_nodes.extend(
                TextNode(text=part, text_type=text_type if i % 2 else TextType.TEXT)
                for i, part in enumerate(parts) if part
            )
        else:
            new_nodes.append(node)
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