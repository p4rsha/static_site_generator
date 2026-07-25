import unittest

from block_proc import markdown_to_blocks , BlockType, block_to_block_type


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

    def test_excessive_blank_lines(self):
        md = "First block\n\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_single_block_no_separator(self):
        md = "just one paragraph\nwith a soft line break"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["just one paragraph\nwith a soft line break"])

    def test_whitespace_only_document(self):
        md = "   \n\n \t \n\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_leading_and_trailing_whitespace_stripped(self):
        md = "   padded block   \n\n\tother block\t"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["padded block", "other block"])

    def test_windows_style_newlines_not_split(self):
        md = "block one\r\n\r\nblock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["block one\r\n\r\nblock two"])

class TestBlockToBlockType(unittest.TestCase):
    # --- heading ---
    def test_heading_one_hash(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)

    def test_heading_six_hashes(self):
        self.assertEqual(block_to_block_type("###### six deep"), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### too many"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#nospace"), BlockType.PARAGRAPH)

    def test_bare_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("###"), BlockType.PARAGRAPH)

    # --- code ---
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')\n```"), BlockType.CODE)

    def test_code_block_multiline(self):
        md = "```\nline one\nline two\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_empty_code_block(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)

    def test_bare_fence_is_paragraph(self):
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)

    def test_inline_backticks_is_paragraph(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_unclosed_code_is_paragraph(self):
        self.assertEqual(block_to_block_type("```\nnever closed"), BlockType.PARAGRAPH)

    # --- quote ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> a wise thing"), BlockType.QUOTE)

    def test_quote_multi_line(self):
        self.assertEqual(block_to_block_type("> one\n> two\n> three"), BlockType.QUOTE)

    def test_quote_without_space_allowed(self):
        self.assertEqual(block_to_block_type(">no space needed"), BlockType.QUOTE)

    def test_quote_broken_by_plain_line(self):
        self.assertEqual(block_to_block_type("> one\nnot quoted"), BlockType.PARAGRAPH)

    # --- unordered list ---
    def test_ul_single_item(self):
        self.assertEqual(block_to_block_type("- only item"), BlockType.UL)

    def test_ul_multi_item(self):
        self.assertEqual(block_to_block_type("- a\n- b\n- c"), BlockType.UL)

    def test_ul_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-nospace"), BlockType.PARAGRAPH)

    def test_ul_broken_by_plain_line(self):
        self.assertEqual(block_to_block_type("- a\nplain line\n- c"), BlockType.PARAGRAPH)

    # --- ordered list ---
    def test_ol_single_item(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.OL)

    def test_ol_multi_item(self):
        self.assertEqual(block_to_block_type("1. a\n2. b\n3. c"), BlockType.OL)

    def test_ol_must_start_at_one(self):
        self.assertEqual(block_to_block_type("2. starts wrong"), BlockType.PARAGRAPH)

    def test_ol_must_increment(self):
        self.assertEqual(block_to_block_type("1. a\n3. skipped two"), BlockType.PARAGRAPH)

    def test_ol_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("1.nospace"), BlockType.PARAGRAPH)

    def test_ol_junk_line_in_middle(self):
        self.assertEqual(block_to_block_type("1. a\njunk\n2. b"), BlockType.PARAGRAPH)

    def test_ol_junk_line_first(self):
        self.assertEqual(block_to_block_type("junk\n1. a"), BlockType.PARAGRAPH)

    # --- paragraph ---
    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("just some ordinary text"), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        md = "first line of prose\nsecond line of prose"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()