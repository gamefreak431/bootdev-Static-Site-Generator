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




if __name__ == "__main__":
    unittest.main()
