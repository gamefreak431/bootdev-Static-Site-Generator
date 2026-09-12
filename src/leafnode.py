from htmlnode import HTMLNode


# HTML5 void elements: their content is their attributes, so they carry no
# value and have no closing tag. <img> is the only one this generator currently
# produces, but the set costs nothing and already covers <hr> and <br> if
# thematic breaks or hard line breaks are added later.
VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "source", "track", "wbr",
})


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str]|None=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        # Checked before the value rule: an empty value on a void element is
        # correct, not missing, so it must not be treated as an error.
        if self.tag in VOID_TAGS:
            return f"<{self.tag}{self.props_to_html()}>"
        if self.value is None:
            raise ValueError("LeafNode must have a value to render.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"