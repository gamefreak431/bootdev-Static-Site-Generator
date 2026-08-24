from textnode import TextNode, TextType


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
        if node.count(delimiter) % 2 != 0:
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