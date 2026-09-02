import unittest
from pathlib import Path

from mdparse import (
    markdown_to_blocks,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    block_to_block_type,
    block_type_to_html_node,
    markdown_to_html_node,
    BlockType,
)
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode


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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_text_to_textnodes_delimiter_in_already_split_node_does_not_raise(self):
        # Regression test: an underscore inside an already-BOLD node used to
        # trip the odd/even delimiter check meant only for TEXT nodes.
        nodes = text_to_textnodes("**bold_word** and _italic_")
        self.assertEqual(
            nodes,
            [
                TextNode(text="bold_word", text_type=TextType.BOLD),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
            ],
        )

    def test_text_to_textnodes_with_plain_text(self):
        text = "This is plain text with no markdown at all."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode(text=text, text_type=TextType.TEXT)])

    def test_text_to_textnodes_with_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertEqual(nodes, [TextNode(text="", text_type=TextType.TEXT)])

    def test_text_to_textnodes_with_unmatched_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is _broken italic")

    def test_text_to_textnodes_with_adjacent_styles_no_space(self):
        nodes = text_to_textnodes("**bold**_italic_")
        self.assertEqual(
            nodes,
            [
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text="italic", text_type=TextType.ITALIC),
            ],
        )

    def test_text_to_textnodes_with_multiple_images_and_links(self):
        text = "![a](https://boot.dev/a.png)![b](https://boot.dev/b.png) and [c](https://boot.dev/c)[d](https://boot.dev/d)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode(text="a", text_type=TextType.IMAGE, url="https://boot.dev/a.png"),
                TextNode(text="b", text_type=TextType.IMAGE, url="https://boot.dev/b.png"),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="c", text_type=TextType.LINK, url="https://boot.dev/c"),
                TextNode(text="d", text_type=TextType.LINK, url="https://boot.dev/d"),
            ],
        )

    def test_text_to_textnodes_with_underscore_in_url(self):
        # Images/links are extracted before delimiter splitting, so an
        # underscore inside a URL is no longer misread as an italic
        # delimiter.
        nodes = text_to_textnodes("![alt](https://example.com/foo_bar.png)")
        self.assertEqual(
            nodes,
            [TextNode(text="alt", text_type=TextType.IMAGE, url="https://example.com/foo_bar.png")],
        )

    def test_text_to_textnodes_with_underscore_in_code_span(self):
        # Code spans are split before bold/italic, so their contents are
        # treated as literal text instead of being scanned for markdown.
        nodes = text_to_textnodes("This is `snake_case` code")
        self.assertEqual(
            nodes,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="snake_case", text_type=TextType.CODE),
                TextNode(text=" code", text_type=TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_with_bold_inside_code_span(self):
        # Code spans should be treated as literal even when they contain
        # characters that would otherwise be a bold/italic delimiter.
        nodes = text_to_textnodes("This is `**not bold**` code")
        self.assertEqual(
            nodes,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="**not bold**", text_type=TextType.CODE),
                TextNode(text=" code", text_type=TextType.TEXT),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_link_at_end_of_block(self):
        md = """Check out this [link](https://boot.dev)

Next paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Check out this [link](https://boot.dev)",
                "Next paragraph",
            ],
        )

    def test_markdown_to_blocks_with_link_at_start_of_block(self):
        md = """Intro paragraph

[link](https://boot.dev) is here"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Intro paragraph",
                "[link](https://boot.dev) is here",
            ],
        )

    def test_markdown_to_blocks_with_leading_newline_before_image_block(self):
        # A newline directly before a block that is only an image: strip()
        # should remove the leading newline without touching any of the
        # image markdown itself, including the URL.
        md = "\n![alt text](https://boot.dev/image.png)\n\nSome other text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "![alt text](https://boot.dev/image.png)",
                "Some other text",
            ],
        )

    def test_markdown_to_blocks_with_trailing_newline_after_link_block(self):
        # A newline directly after the final block's link: strip() should
        # remove the trailing newline without truncating the URL.
        md = "First block\n\nSecond block with a [link](https://boot.dev)\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block with a [link](https://boot.dev)",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_with_headings(self):
        for level in range(1, 7):
            block = f"{'#' * level} Heading text"
            with self.subTest(level=level):
                self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_with_heading_missing_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_quote(self):
        self.assertEqual(block_to_block_type("> a quote"), BlockType.QUOTE)

    def test_block_to_block_type_with_quote_no_space_after_marker(self):
        self.assertEqual(block_to_block_type(">a quote"), BlockType.QUOTE)

    def test_block_to_block_type_with_quote_multiple_lines(self):
        # Spec allows the > marker with or without the trailing space, and
        # both forms may appear in the same quote block.
        block = "> line one\n>line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_with_quote_broken_second_line(self):
        # Regression test: previously only the first line was checked, so a
        # block like this one was misclassified as QUOTE.
        block = "> line one\nnot a quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph of text."),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_with_multiline_paragraph(self):
        self.assertEqual(
            block_to_block_type("Line one\nLine two continues here"),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_with_ulist_single_line(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.ULIST)

    def test_block_to_block_type_with_ulist_multiple_lines(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_block_to_block_type_with_ulist_missing_space_after_dash(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_ulist_broken_second_line(self):
        # Regression test: previously only the first line was checked, so a
        # block like this one was misclassified as ULIST.
        block = "- item one\nnot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_olist_single_line(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.OLIST)

    def test_block_to_block_type_with_olist_multiple_lines_sequential(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_block_to_block_type_with_olist_not_starting_at_one(self):
        block = "2. item one\n3. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_olist_skipped_number(self):
        block = "1. item one\n3. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_olist_repeated_number(self):
        block = "1. item one\n1. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_olist_line_missing_marker(self):
        # Regression test: a line with no number match must short-circuit
        # before group(1) is accessed, not raise IndexError.
        block = "1. item one\njust some text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_with_code_block_language_tag(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_with_code_block_empty(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_with_code_block_unclosed(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_code_block_single_line(self):
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)

    def test_block_to_block_type_with_code_block_closing_fence_has_trailing_content(self):
        # Regression test: the closing fence must be exactly ``` — a line
        # like "```stray" must not count as a valid close.
        block = "```\nprint('hello')\n```stray"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestBlockTypeToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        node = block_type_to_html_node("Just plain text.", BlockType.PARAGRAPH)
        self.assertEqual(
            node,
            ParentNode(tag="p", children=[LeafNode(tag=None, value="Just plain text.")]),
        )

    def test_paragraph_with_inline_formatting(self):
        node = block_type_to_html_node(
            "This is **bold** and _italic_ text.", BlockType.PARAGRAPH
        )
        self.assertEqual(
            node,
            ParentNode(
                tag="p",
                children=[
                    LeafNode(tag=None, value="This is "),
                    LeafNode(tag="b", value="bold"),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="i", value="italic"),
                    LeafNode(tag=None, value=" text."),
                ],
            ),
        )

    def test_heading_level_1(self):
        node = block_type_to_html_node("# Heading text", BlockType.HEADING)
        self.assertEqual(
            node,
            ParentNode(tag="h1", children=[LeafNode(tag=None, value="Heading text")]),
        )

    def test_heading_level_6(self):
        node = block_type_to_html_node("###### Deep heading", BlockType.HEADING)
        self.assertEqual(
            node,
            ParentNode(tag="h6", children=[LeafNode(tag=None, value="Deep heading")]),
        )

    def test_code_block_without_language(self):
        block = "```\nprint('hello')\n```"
        node = block_type_to_html_node(block, BlockType.CODE)
        self.assertEqual(
            node,
            ParentNode(tag="pre", children=[LeafNode(tag="code", value="print('hello')")]),
        )

    def test_code_block_with_language_tag_is_stripped(self):
        # The language identifier on the opening fence must not leak into
        # the rendered code content.
        block = "```python\ndef example():\n    print(\"hi\")\n```"
        node = block_type_to_html_node(block, BlockType.CODE)
        self.assertEqual(
            node,
            ParentNode(
                tag="pre",
                children=[LeafNode(tag="code", value="def example():\n    print(\"hi\")")],
            ),
        )

    def test_code_block_content_is_literal_not_parsed_as_markdown(self):
        # Code block content bypasses text_to_textnodes entirely, so
        # markdown-looking characters inside it stay literal.
        block = "```\n**not bold**\n```"
        node = block_type_to_html_node(block, BlockType.CODE)
        self.assertEqual(
            node,
            ParentNode(tag="pre", children=[LeafNode(tag="code", value="**not bold**")]),
        )

    def test_quote_single_line(self):
        node = block_type_to_html_node("> a wise quote", BlockType.QUOTE)
        self.assertEqual(
            node,
            ParentNode(tag="blockquote", children=[LeafNode(tag=None, value="a wise quote")]),
        )

    def test_quote_multiple_lines_joined_with_newline(self):
        block = "> line one\n>line two"
        node = block_type_to_html_node(block, BlockType.QUOTE)
        self.assertEqual(
            node,
            ParentNode(
                tag="blockquote",
                children=[LeafNode(tag=None, value="line one\nline two")],
            ),
        )

    def test_ulist(self):
        block = "- first item\n- second **bold** item"
        node = block_type_to_html_node(block, BlockType.ULIST)
        self.assertEqual(
            node,
            ParentNode(
                tag="ul",
                children=[
                    ParentNode(tag="li", children=[LeafNode(tag=None, value="first item")]),
                    ParentNode(
                        tag="li",
                        children=[
                            LeafNode(tag=None, value="second "),
                            LeafNode(tag="b", value="bold"),
                            LeafNode(tag=None, value=" item"),
                        ],
                    ),
                ],
            ),
        )

    def test_olist(self):
        block = "1. first item\n2. second item"
        node = block_type_to_html_node(block, BlockType.OLIST)
        self.assertEqual(
            node,
            ParentNode(
                tag="ol",
                children=[
                    ParentNode(tag="li", children=[LeafNode(tag=None, value="first item")]),
                    ParentNode(tag="li", children=[LeafNode(tag=None, value="second item")]),
                ],
            ),
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
    EXAMPLE_MARKDOWN_PATH = Path(__file__).resolve().parent.parent / "example_markdown.md"

    def test_markdown_to_html_node_with_headings_paragraphs_and_lists(self):
        md = """# This is a heading

This is a paragraph and beneath it is an unordered list:

- list item
- another list item
- one more

Another paragraph before an ordered list:

1. list item
2. another list item
3. one more
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>This is a heading</h1>"
            "<p>This is a paragraph and beneath it is an unordered list:</p>"
            "<ul><li>list item</li><li>another list item</li><li>one more</li></ul>"
            "<p>Another paragraph before an ordered list:</p>"
            "<ol><li>list item</li><li>another list item</li><li>one more</li></ol>"
            "</div>",
        )

    def test_markdown_to_html_node_with_quote_and_code_block(self):
        md = """> You miss 100% of the shots you don't take
> Wayne Gretzky

```python
def example_code(args):
\tprint("hello world, this is python in a code block")
```
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<blockquote>You miss 100% of the shots you don't take\nWayne Gretzky</blockquote>"
            '<pre><code>def example_code(args):\n\tprint("hello world, this is python in a code block")</code></pre>'
            "</div>",
        )

    def test_markdown_to_html_node_with_example_file(self):
        # Full-document integration test: every block type composed
        # together in one pass, using the example file kept in the repo
        # root as the source of truth for the input.
        markdown = self.EXAMPLE_MARKDOWN_PATH.read_text()
        html = markdown_to_html_node(markdown).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>This is a heading</h1>"
            "<p>This is a paragraph and beneath it is an unordered list:</p>"
            "<ul><li>list item</li><li>another list item</li><li>one more</li></ul>"
            "<p>Another paragraph before an ordered list:</p>"
            "<ol><li>list item</li><li>another list item</li><li>one more</li></ol>"
            "<h2>Here's a second level heading.</h2>"
            "<p>Next up, we will test quotes:</p>"
            "<blockquote>You miss 100% of the shots you don't take\nWayne Gretzky</blockquote>"
            "<p>Now a code block:</p>"
            '<pre><code>def example_code(args):\n\tprint("hello world, this is python in a code block")</code></pre>'
            "</div>",
        )