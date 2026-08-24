import unittest
from mdparse import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_with_valid_input(self):
        old_nodes = [
            TextNode(text="This is _italic_ text.", text_type=TextType.TEXT),
            TextNode(text="This is **bold** text.", text_type=TextType.TEXT),
        ]
        delimiter = "_"
        text_type = TextType.ITALIC
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text.")
        self.assertEqual(new_nodes[3].text, "This is **bold** text.")

    def test_split_nodes_delimiter_with_unmatched_delimiter(self):
        old_nodes = [
            TextNode(text="This is _italic text.", text_type=TextType.TEXT),
        ]
        delimiter = "_"
        text_type = TextType.ITALIC
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_delimiter_passes_through_non_text_nodes(self):
        old_nodes = [
            TextNode(text="already bold", text_type=TextType.BOLD),
            TextNode(text="a link", text_type=TextType.LINK, url="https://boot.dev"),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_delimiter_with_multiple_delimiter_pairs(self):
        old_nodes = [
            TextNode(text="This is _italic_ and _more italic_ text.", text_type=TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="more italic", text_type=TextType.ITALIC),
                TextNode(text=" text.", text_type=TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_with_leading_delimiter(self):
        old_nodes = [TextNode(text="_italic_ text", text_type=TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=" text", text_type=TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_with_trailing_delimiter(self):
        old_nodes = [TextNode(text="text _italic_", text_type=TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode(text="text ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
            ],
        )

    def test_split_nodes_delimiter_with_empty_old_nodes(self):
        self.assertEqual(split_nodes_delimiter([], "_", TextType.ITALIC), [])

    def test_split_nodes_delimiter_with_multi_char_delimiter(self):
        old_nodes = [TextNode(text="This is **bold** text.", text_type=TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=" text.", text_type=TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_with_delimiter_only_text(self):
        old_nodes = [TextNode(text="__", text_type=TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [])