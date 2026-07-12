import unittest

from block_proc import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()