import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", attributes={"class": "container"})
        node2 = HTMLNode("div", attributes={"class": "container"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("div", attributes={"class": "container"})
        node2 = HTMLNode("span", attributes={"class": "container"})
        self.assertNotEqual(node, node2)

    def test_not_eq_different_attributes(self):
        node = HTMLNode("div", attributes={"class": "container"})
        node2 = HTMLNode("div", attributes={"id": "main"})
        self.assertNotEqual(node, node2)

    def test_eq_non_htmlnode(self):
        node = HTMLNode("div", attributes={"class": "container"})
        self.assertNotEqual(node, "This is not an HTMLNode")

    def test_props_to_html(self):
        node = HTMLNode("div", attributes={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_repr(self):
        node = HTMLNode("div", attributes={"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=None, children=[], attributes={'class': 'container'})")

if __name__ == "__main__":
    unittest.main()