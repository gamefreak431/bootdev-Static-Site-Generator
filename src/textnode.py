from enum import Enum


class textType(Enum):
    """Enum for text types."""

    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    """Class representing a text node."""

    def __init__(self, text: str, text_type: textType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __str__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type}, url={self.url})"

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"