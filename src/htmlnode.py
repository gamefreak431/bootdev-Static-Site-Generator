

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

    def render(self):
        attrs = self.props_to_html()
        opening_tag = f'<{self.tag} {attrs}>' if attrs else f'<{self.tag}>'
        closing_tag = f'</{self.tag}>'
        if self.value:
            return f'{opening_tag}{self.value}{closing_tag}'
        children_html = ''.join(child.render() for child in self.children)
        return f'{opening_tag}{children_html}{closing_tag}'