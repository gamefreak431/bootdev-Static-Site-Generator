from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    """Enum for text types."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """Class representing a text node."""

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=self.text)
            case TextType.BOLD:
                return LeafNode(tag="b", value=self.text)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=self.text)
            case TextType.CODE:
                return LeafNode(tag="code", value=self.text)
            case TextType.LINK:
                if self.url is None:
                    raise ValueError(f"URL must be provided for link text type at: {self.text}")
                return LeafNode(
                    tag="a", value=self.text, props={"href": self.url}
                )
            case TextType.IMAGE:
                if self.url is None:
                    raise ValueError(f"URL must be provided for image text type at: {self.text}")
                return LeafNode(
                    tag="img", value="", props={"src": self.url, "alt": self.text}
                )
            case _:
                raise ValueError(f"Unsupported text type: {self.text_type}")

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"