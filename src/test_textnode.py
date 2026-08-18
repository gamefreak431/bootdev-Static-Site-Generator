import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a link", TextType.LINK, url="https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_non_textnode(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a text node")

    def test_url(self):
        node = TextNode("This is a link", TextType.LINK, url="https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_default_url_is_none(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            repr(node), "TextNode(This is a link, link, https://www.boot.dev)"
        )


if __name__ == "__main__":
    unittest.main()