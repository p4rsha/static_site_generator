import unittest

from block_proc import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
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


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_single_heading(self):
        node = markdown_to_html_node("# Heading one")
        self.assertEqual(node.to_html(), "<div><h1>Heading one</h1></div>")

    def test_all_heading_levels(self):
        md = "# One\n\n## Two\n\n### Three\n\n#### Four\n\n##### Five\n\n###### Six"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>One</h1><h2>Two</h2><h3>Three</h3><h4>Four</h4><h5>Five</h5><h6>Six</h6></div>",
        )

    def test_heading_with_inline(self):
        node = markdown_to_html_node("## A **bold** title")
        self.assertEqual(node.to_html(), "<div><h2>A <b>bold</b> title</h2></div>")

    def test_quote_single_line(self):
        node = markdown_to_html_node("> a wise thing")
        self.assertEqual(node.to_html(), "<div><blockquote>a wise thing</blockquote></div>")

    def test_quote_multi_line_joined(self):
        node = markdown_to_html_node("> line one\n> line two")
        self.assertEqual(node.to_html(), "<div><blockquote>line one line two</blockquote></div>")

    def test_quote_without_space(self):
        node = markdown_to_html_node(">tight quote")
        self.assertEqual(node.to_html(), "<div><blockquote>tight quote</blockquote></div>")

    def test_quote_with_inline(self):
        node = markdown_to_html_node("> a **bold** quote")
        self.assertEqual(node.to_html(), "<div><blockquote>a <b>bold</b> quote</blockquote></div>")

    def test_unordered_list(self):
        node = markdown_to_html_node("- one\n- two\n- three")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        node = markdown_to_html_node("- **bold** item\n- _italic_ item")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul></div>",
        )

    def test_ordered_list(self):
        node = markdown_to_html_node("1. one\n2. two\n3. three")
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_ordered_list_with_inline(self):
        node = markdown_to_html_node("1. a `code` item\n2. a **bold** item")
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>a <code>code</code> item</li><li>a <b>bold</b> item</li></ol></div>",
        )

    def test_paragraph_with_link(self):
        node = markdown_to_html_node("Go to [boot dev](https://www.boot.dev) now")
        self.assertEqual(
            node.to_html(),
            '<div><p>Go to <a href="https://www.boot.dev">boot dev</a> now</p></div>',
        )

    def test_mixed_document(self):
        md = """# Title

Some **bold** intro text
across two lines

- first item
- second item

> a quote here

1. step one
2. step two
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>Some <b>bold</b> intro text across two lines</p>"
            "<ul><li>first item</li><li>second item</li></ul>"
            "<blockquote>a quote here</blockquote>"
            "<ol><li>step one</li><li>step two</li></ol>"
            "</div>",
        )

    def test_empty_markdown(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()