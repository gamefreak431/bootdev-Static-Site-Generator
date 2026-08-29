import unittest
from mdparse import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)
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

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_with_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](https://boot.dev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link text", "https://boot.dev")])

    def test_extract_markdown_links_with_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_ignores_images(self):
        text = "This has an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link", "https://boot.dev")])

    def test_extract_markdown_images_ignores_links(self):
        text = "This has an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_with_no_matches(self):
        text = "This is plain text with no images."
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_links_with_no_matches(self):
        text = "This is plain text with no links."
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_images_with_empty_alt_text(self):
        text = "![](https://i.imgur.com/zjjcJKZ.png)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_links_with_empty_link_text(self):
        text = "[](https://boot.dev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("", "https://boot.dev")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_no_images(self):
        node = TextNode("This is plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_with_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and text after", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_image_at_end(self):
        node = TextNode(
            "text before and ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_split_images_with_adjacent_images(self):
        node = TextNode(
            "![a](https://i.imgur.com/aaa.png)![b](https://i.imgur.com/bbb.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://i.imgur.com/aaa.png"),
                TextNode("b", TextType.IMAGE, "https://i.imgur.com/bbb.png"),
            ],
            new_nodes,
        )

    def test_split_images_passes_through_non_text_nodes(self):
        old_nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("a link", TextType.LINK, "https://boot.dev"),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(old_nodes, new_nodes)

    def test_split_images_with_multiple_nodes_mixed(self):
        old_nodes = [
            TextNode("no images here", TextType.TEXT),
            TextNode(
                "with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("no images here", TextType.TEXT),
                TextNode("with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_matched_node_then_no_match_node(self):
        old_nodes = [
            TextNode(
                "with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
            ),
            TextNode("no images here", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("no images here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_empty_old_nodes(self):
        self.assertListEqual([], split_nodes_image([]))

    def test_split_images_with_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_ignores_links(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_link_at_start(self):
        node = TextNode("[link](https://boot.dev) and text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_link_at_end(self):
        node = TextNode("text before and [link](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text before and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_with_only_link(self):
        node = TextNode("[link](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://boot.dev")], new_nodes
        )

    def test_split_links_with_adjacent_links(self):
        node = TextNode(
            "[a](https://boot.dev/a)[b](https://boot.dev/b)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://boot.dev/a"),
                TextNode("b", TextType.LINK, "https://boot.dev/b"),
            ],
            new_nodes,
        )

    def test_split_links_passes_through_non_text_nodes(self):
        old_nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(old_nodes, new_nodes)

    def test_split_links_with_multiple_nodes_mixed(self):
        old_nodes = [
            TextNode("no links here", TextType.TEXT),
            TextNode("with a [link](https://boot.dev)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("no links here", TextType.TEXT),
                TextNode("with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_with_matched_node_then_no_match_node(self):
        old_nodes = [
            TextNode("with a [link](https://boot.dev)", TextType.TEXT),
            TextNode("no links here", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("no links here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_empty_old_nodes(self):
        self.assertListEqual([], split_nodes_link([]))

    def test_split_links_with_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_ignores_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )