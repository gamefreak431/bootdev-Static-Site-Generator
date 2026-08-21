import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        node2 = HTMLNode(tag="div", props={"class": "container"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        node2 = HTMLNode(tag="span", props={"class": "container"})
        self.assertNotEqual(node, node2)

    def test_not_eq_different_attributes(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        node2 = HTMLNode(tag="div", props={"id": "main"})
        self.assertNotEqual(node, node2)

    def test_eq_non_htmlnode(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        self.assertNotEqual(node, "This is not an HTMLNode")

    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_repr(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=None, children=[], props={'class': 'container'})")

if __name__ == "__main__":
    unittest.main()