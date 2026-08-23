import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a text node", text_type=TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a different text node", text_type=TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a text node", text_type=TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://www.boot.dev")
        node2 = TextNode(text="This is a link", text_type=TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_non_textnode(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        self.assertNotEqual(node, "This is a text node")

    def test_url(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_default_url_is_none(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_repr_with_url(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://www.boot.dev")
        self.assertEqual(
            repr(node), "TextNode(This is a link, link, https://www.boot.dev)"
        )

    def test_text(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_bold(self):
        node = TextNode(text="This is bold text", text_type=TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, {})

    def test_italic(self):
        node = TextNode(text="This is italic text", text_type=TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, {})

    def test_code(self):
        node = TextNode(text="This is code text", text_type=TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")
        self.assertEqual(html_node.props, {})

    def test_link(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://www.boot.dev")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_link_without_url_raises(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK)
        with self.assertRaises(ValueError):
            node.text_node_to_html_node()

    def test_image(self):
        node = TextNode(text="This is alt text", text_type=TextType.IMAGE, url="https://www.boot.dev/image.png")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev/image.png", "alt": "This is alt text"},
        )

    def test_image_without_url_raises(self):
        node = TextNode(text="This is alt text", text_type=TextType.IMAGE)
        with self.assertRaises(ValueError):
            node.text_node_to_html_node()


if __name__ == "__main__":
    unittest.main()
