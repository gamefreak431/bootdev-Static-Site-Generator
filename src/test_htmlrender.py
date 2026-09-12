import unittest
from pathlib import Path

from blockparse import Block, BlockType
from htmlrender import block_to_html_node, markdown_to_html_node, text_node_to_html_node
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_bold(self):
        node = TextNode(text="This is bold text", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, {})

    def test_italic(self):
        node = TextNode(text="This is italic text", text_type=TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, {})

    def test_code(self):
        node = TextNode(text="This is code text", text_type=TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")
        self.assertEqual(html_node.props, {})

    def test_link(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_link_without_url_raises(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image(self):
        node = TextNode(text="This is alt text", text_type=TextType.IMAGE, url="https://www.boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev/image.png", "alt": "This is alt text"},
        )

    def test_image_without_url_raises(self):
        node = TextNode(text="This is alt text", text_type=TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestBlockToHtmlNode(unittest.TestCase):
    """block_to_html_node is given already-stripped content, so these build
    Block objects directly rather than going through parse_block."""

    def test_paragraph(self):
        node = block_to_html_node(Block(type=BlockType.PARAGRAPH, content="Just plain text."))
        self.assertEqual(
            node,
            ParentNode(tag="p", children=[LeafNode(tag=None, value="Just plain text.")]),
        )

    def test_paragraph_with_inline_formatting(self):
        node = block_to_html_node(
            Block(type=BlockType.PARAGRAPH, content="This is **bold** and _italic_ text.")
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
        node = block_to_html_node(
            Block(type=BlockType.HEADING, content="Heading text", level=1)
        )
        self.assertEqual(
            node,
            ParentNode(tag="h1", children=[LeafNode(tag=None, value="Heading text")]),
        )

    def test_heading_level_6(self):
        node = block_to_html_node(
            Block(type=BlockType.HEADING, content="Deep heading", level=6)
        )
        self.assertEqual(
            node,
            ParentNode(tag="h6", children=[LeafNode(tag=None, value="Deep heading")]),
        )

    def test_code_block(self):
        node = block_to_html_node(Block(type=BlockType.CODE, content="print('hello')"))
        self.assertEqual(
            node,
            ParentNode(tag="pre", children=[LeafNode(tag="code", value="print('hello')")]),
        )

    def test_code_block_content_is_literal_not_parsed_as_markdown(self):
        # Code content bypasses text_to_textnodes entirely, so markdown-looking
        # characters inside it stay literal.
        node = block_to_html_node(Block(type=BlockType.CODE, content="**not bold**"))
        self.assertEqual(
            node,
            ParentNode(tag="pre", children=[LeafNode(tag="code", value="**not bold**")]),
        )

    def test_quote_single_line(self):
        node = block_to_html_node(Block(type=BlockType.QUOTE, content="a wise quote"))
        self.assertEqual(
            node,
            ParentNode(tag="blockquote", children=[LeafNode(tag=None, value="a wise quote")]),
        )

    def test_quote_multiple_lines_joined_with_newline(self):
        node = block_to_html_node(
            Block(type=BlockType.QUOTE, content="line one\nline two")
        )
        self.assertEqual(
            node,
            ParentNode(
                tag="blockquote",
                children=[LeafNode(tag=None, value="line one\nline two")],
            ),
        )

    def test_ulist(self):
        node = block_to_html_node(
            Block(type=BlockType.ULIST, content=["first item", "second **bold** item"])
        )
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
        node = block_to_html_node(
            Block(type=BlockType.OLIST, content=["first item", "second item"])
        )
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

    def test_unsupported_block_type_raises(self):
        node = Block(type="not a block type", content="whatever")
        with self.assertRaises(ValueError):
            block_to_html_node(node)


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

    def test_markdown_to_html_node_with_empty_code_block(self):
        # An empty fenced block is valid HTML and renders as an empty element
        # rather than raising.
        self.assertEqual(
            markdown_to_html_node("```\n```").to_html(),
            "<div><pre><code></code></pre></div>",
        )

    def test_markdown_to_html_node_with_empty_quote(self):
        self.assertEqual(
            markdown_to_html_node("> ").to_html(),
            "<div><blockquote></blockquote></div>",
        )

    def test_markdown_to_html_node_with_image(self):
        md = "Look at this ![alt text](https://boot.dev/image.png)"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><p>Look at this <img src="https://boot.dev/image.png" alt="alt text"></p></div>',
        )

if __name__ == "__main__":
    unittest.main()
