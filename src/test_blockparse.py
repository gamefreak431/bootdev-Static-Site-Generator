import unittest

from blockparse import (
    markdown_to_blocks,
    block_to_block_type,
    parse_block,
    extract_title,
    Block,
    BlockType,
)


class TestMarkdownToBlocks(unittest.TestCase):
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


class TestParseBlock(unittest.TestCase):
    """parse_block owns marker stripping; these assert the markers are gone."""

    def test_paragraph_is_left_alone(self):
        self.assertEqual(
            parse_block("Just plain text."),
            Block(type=BlockType.PARAGRAPH, content="Just plain text."),
        )

    def test_multiline_paragraph_keeps_its_newline(self):
        self.assertEqual(
            parse_block("Line one\nLine two"),
            Block(type=BlockType.PARAGRAPH, content="Line one\nLine two"),
        )

    def test_heading_marker_stripped_and_level_recorded(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                self.assertEqual(
                    parse_block(f"{'#' * level} Heading text"),
                    Block(type=BlockType.HEADING, content="Heading text", level=level),
                )

    def test_code_fences_stripped(self):
        self.assertEqual(
            parse_block("```\nprint('hello')\n```"),
            Block(type=BlockType.CODE, content="print('hello')"),
        )

    def test_code_language_tag_stripped(self):
        # The language identifier lives on the opening fence, so it goes with it.
        self.assertEqual(
            parse_block('```python\ndef example():\n    print("hi")\n```'),
            Block(type=BlockType.CODE, content='def example():\n    print("hi")'),
        )

    def test_code_content_is_not_inline_parsed(self):
        self.assertEqual(
            parse_block("```\n**not bold**\n```"),
            Block(type=BlockType.CODE, content="**not bold**"),
        )

    def test_empty_code_block_has_empty_content(self):
        self.assertEqual(parse_block("```\n```"), Block(type=BlockType.CODE, content=""))

    def test_quote_markers_stripped_with_and_without_space(self):
        self.assertEqual(
            parse_block("> line one\n>line two"),
            Block(type=BlockType.QUOTE, content="line one\nline two"),
        )

    def test_ulist_markers_stripped_into_one_item_per_line(self):
        self.assertEqual(
            parse_block("- first item\n- second item"),
            Block(type=BlockType.ULIST, content=["first item", "second item"]),
        )

    def test_olist_numbers_stripped_into_one_item_per_line(self):
        # The numbers are dropped entirely -- <ol> supplies its own.
        self.assertEqual(
            parse_block("1. first item\n2. second item"),
            Block(type=BlockType.OLIST, content=["first item", "second item"]),
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_with_h1(self):
        self.assertEqual(extract_title("# Hello\n\nSome text"), "Hello")

    def test_extract_title_skips_h2_before_h1(self):
        self.assertEqual(extract_title("## Sub\n\n# Title"), "Title")

    def test_extract_title_with_only_h2_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Not a title\n\nSome text")

    def test_extract_title_with_no_heading_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just a paragraph\n\n- and a list")

if __name__ == "__main__":
    unittest.main()
