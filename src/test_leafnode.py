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
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_value_renders_empty_element(self):
        # An empty string is content, not a missing value: only None means the
        # leaf was built without one.
        node = LeafNode(tag="code", value="")
        self.assertEqual(node.to_html(), "<code></code>")

    def test_to_html_with_void_tag_has_no_closing_tag(self):
        node = LeafNode(tag="img", value="", props={"src": "a.png", "alt": "alt text"})
        self.assertEqual(node.to_html(), '<img src="a.png" alt="alt text">')

    def test_to_html_with_void_tag_and_no_props(self):
        node = LeafNode(tag="hr", value="")
        self.assertEqual(node.to_html(), "<hr>")

    def test_to_html_with_void_tag_does_not_raise_on_empty_value(self):
        # A void element's content is its attributes, so an empty value is
        # expected rather than a missing one.
        node = LeafNode(tag="br", value="")
        self.assertEqual(node.to_html(), "<br>")

    def test_repr(self):
        node = LeafNode(tag="p", value="This is a paragraph.", props={"class": "text"})
        self.assertEqual(
            repr(node), "LeafNode(tag=p, value=This is a paragraph., props={'class': 'text'})"
        )

if __name__ == "__main__":
    unittest.main()