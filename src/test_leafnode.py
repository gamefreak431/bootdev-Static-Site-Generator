import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_to_html_with_tag_value_and_props(self):
        node = LeafNode(tag="a", value="Click here", props={"href": "https://www.boot.dev"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.boot.dev">Click here</a>'
        )

    def test_to_html_without_tag(self):
        node = LeafNode(tag="", value="This is just text.")
        self.assertEqual(node.to_html(), "This is just text.")

    def test_to_html_without_value_raises_error(self):
        node = LeafNode(tag="p", value="")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode(tag="p", value="This is a paragraph.", props={"class": "text"})
        self.assertEqual(
            repr(node), "LeafNode(tag=p, value=This is a paragraph., props={'class': 'text'})"
        )

if __name__ == "__main__":
    unittest.main()