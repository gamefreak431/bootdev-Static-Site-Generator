"""Block-level markdown parsing: a document -> blocks, and each block's type.

Knows about block-level markdown syntax (fences, markers, prefixes) and nothing
about HTML. This module is the only place that knows what a markdown block
marker looks like: it both recognises markers and strips them, so the renderer
receives content that carries no markdown syntax at all.
"""

from dataclasses import dataclass
from enum import Enum
import re


HEADING_LINE_PATTERN = re.compile(r"^(#{1,6})\s")
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
        case _ if HEADING_LINE_PATTERN.match(block):
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

@dataclass
class Block:
    """A classified markdown block with its syntax markers removed.

    Attributes:
        type (BlockType): What kind of block this is.
        content (str | list[str]): The block's text with markers stripped --
            a single string, or one string per item for list blocks.
        level (int | None): Heading depth 1-6; None for every other block type.
    """
    type: BlockType
    content: str | list[str]
    level: int | None = None

def parse_block(block: str) -> Block:
    """Classify a markdown block and strip its markdown markers.
    Args:
        block (str): The raw markdown block.
    Returns:
        Block: The block's type and its content with markers removed.
    """
    block_type = block_to_block_type(block)
    lines = block.split("\n")
    match block_type:
        case BlockType.HEADING:
            return Block(
                type=block_type,
                content=HEADING_LINE_PATTERN.sub("", block),
                level=len(HEADING_LINE_PATTERN.match(block).group(1)),
            )
        case BlockType.CODE:
            # Drop the opening fence (with any language tag) and the closing fence.
            return Block(type=block_type, content="\n".join(lines[1:-1]))
        case BlockType.QUOTE:
            return Block(
                type=block_type,
                content="\n".join(QUOTE_LINE_PATTERN.sub("", line) for line in lines),
            )
        case BlockType.ULIST:
            return Block(
                type=block_type,
                content=[ULIST_LINE_PATTERN.sub("", line) for line in lines],
            )
        case BlockType.OLIST:
            return Block(
                type=block_type,
                content=[OLIST_LINE_PATTERN.sub("", line) for line in lines],
            )
        case _:
            return Block(type=block_type, content=block)
