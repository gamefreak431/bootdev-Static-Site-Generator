

class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}

    def to_html(self) -> str:
        raise NotImplementedError("Subclasses must implement the to_html method.")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_attribute(self, key, value):
        self.props[key] = value