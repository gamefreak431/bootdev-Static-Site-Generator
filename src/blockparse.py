"""Block-level markdown parsing: a document -> blocks, and each block's type.

Knows about block-level markdown syntax (fences, markers, prefixes) and nothing
about HTML. Produces plain strings and BlockType values.
"""

from enum import Enum
import re


QUOTE_LINE_PATTERN = re.compile(r"^>\s?")
ULIST_LINE_PATTERN = re.compile(r"^\-\s")
OLIST_LINE_PATTERN = re.compile(r"^(\d+)\.\s")

class BlockType(Enum):
    """Enum for block types."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    """Convert a markdown string to a list of markdown blocks.
    Args:
        markdown (str): The markdown string to convert.
    Returns:
        list[str]: A list of strings representing the markdown blocks.
    """
    return [line.strip() for line in markdown.split("\n\n") if line.strip() != ""]

def block_to_block_type(block: str) -> BlockType:
    """Determine the block type of a markdown block.
    Args:
        block (str): The markdown block to analyze.
    Returns:
        BlockType: The type of the markdown block.
    """
    def _is_valid_ulist(block: str) -> bool:
        return all(ULIST_LINE_PATTERN.match(line) for line in block.split("\n"))

    def _is_valid_olist(block: str) -> bool:
        for i, line in enumerate(block.split("\n"), start=1):
            match = OLIST_LINE_PATTERN.match(line)
            if not match or int(match.group(1)) != i:
                return False
        return True

    def _is_valid_quote(block: str) -> bool:
        return all(QUOTE_LINE_PATTERN.match(line) for line in block.split("\n"))

    def _is_valid_code_block(block: str) -> bool:
        lines = block.split("\n")
        return len(lines) > 1 and lines[0].startswith("```") and lines[-1] == "```"

    match block:
        case _ if re.match(r"^#{1,6}\s", block):
            return BlockType.HEADING
        case _ if _is_valid_quote(block):
            return BlockType.QUOTE
        case _ if _is_valid_ulist(block):
            return BlockType.ULIST
        case _ if _is_valid_olist(block):
            return BlockType.OLIST
        case _ if _is_valid_code_block(block):
            return BlockType.CODE
        case _:
            return BlockType.PARAGRAPH
