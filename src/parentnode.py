from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag to render.")
        if not self.children:
            raise ValueError("ParentNode must have children to render.")
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        children_html = "".join(child.to_html() for child in self.children)
        return f"{opening_tag}{children_html}{closing_tag}"