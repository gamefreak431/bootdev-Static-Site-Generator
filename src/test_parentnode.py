import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_tag_raises_error(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="", children=[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_children_raises_error(self):
        parent_node = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children_none_raises_error(self):
        parent_node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        child_node_1 = LeafNode(tag="span", value="first")
        child_node_2 = LeafNode(tag="span", value="second")
        child_node_3 = LeafNode(tag="span", value="third")
        parent_node = ParentNode(
            tag="p", children=[child_node_1, child_node_2, child_node_3]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><span>first</span><span>second</span><span>third</span></p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(
            tag="div", children=[child_node], props={"class": "box"}
        )
        self.assertEqual(
            parent_node.to_html(), '<div class="box"><span>child</span></div>'
        )

    def test_to_html_with_mixed_children(self):
        leaf_child = LeafNode(tag="span", value="leaf")
        parent_child = ParentNode(
            tag="b", children=[LeafNode(tag="i", value="nested")]
        )
        parent_node = ParentNode(tag="div", children=[leaf_child, parent_child])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>leaf</span><b><i>nested</i></b></div>",
        )

    def test_to_html_with_raw_text_child(self):
        raw_text_child = LeafNode(tag="", value="Just some text.")
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="p", children=[raw_text_child, child_node])
        self.assertEqual(
            parent_node.to_html(), "<p>Just some text.<span>child</span></p>"
        )


if __name__ == "__main__":
    unittest.main()