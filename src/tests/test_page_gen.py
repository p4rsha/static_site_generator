import unittest

from page_gen import extract_title


class TestExtractTitle(unittest.TestCase):
    # --- happy path ---
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_trailing_newline(self):
        self.assertEqual(extract_title("# Hello\n"), "Hello")

    def test_title_among_other_content(self):
        md = "# Tolkien Fan Club\n\nSome intro prose here.\n"
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_title_not_on_first_line(self):
        md = "Some preamble text\n\n# The Real Title\n\nmore prose\n"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_title_is_last_line(self):
        md = "intro paragraph\n\n# Trailing Title"
        self.assertEqual(extract_title(md), "Trailing Title")

    # --- whitespace handling ---
    def test_extra_space_after_hash(self):
        self.assertEqual(extract_title("#    Padded Title"), "Padded Title")

    def test_trailing_whitespace_stripped(self):
        self.assertEqual(extract_title("# Padded Title   "), "Padded Title")

    def test_tabs_stripped_both_sides(self):
        self.assertEqual(extract_title("# \tTabbed Title\t"), "Tabbed Title")

    def test_internal_spacing_preserved(self):
        self.assertEqual(extract_title("# A  Wide   Title"), "A  Wide   Title")

    # --- rejects non-h1 headings ---
    def test_h2_only_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Not A Title\n\nsome prose\n")

    def test_h6_only_raises(self):
        with self.assertRaises(Exception):
            extract_title("###### Deep Heading")

    def test_h1_selected_over_h2s(self):
        md = "## Blog posts\n\n# The Title\n\n## Reasons\n"
        self.assertEqual(extract_title(md), "The Title")

    def test_hash_without_space_raises(self):
        with self.assertRaises(Exception):
            extract_title("#nospace")

    def test_bare_hash_raises(self):
        with self.assertRaises(Exception):
            extract_title("#")

    # --- missing title ---
    def test_no_heading_raises(self):
        with self.assertRaises(Exception):
            extract_title("just some prose\n\nand a second paragraph\n")

    def test_empty_document_raises(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_whitespace_only_document_raises(self):
        with self.assertRaises(Exception):
            extract_title("   \n\n\t\n")

    # --- multiple titles rejected ---
    def test_two_titles_raise(self):
        with self.assertRaises(Exception):
            extract_title("# First Title\n\n# Second Title\n")

    def test_three_titles_raise(self):
        with self.assertRaises(Exception):
            extract_title("# One\n\n# Two\n\n# Three\n")

    def test_second_title_far_below_raises(self):
        md = "# Real Title\n\n" + ("filler line\n" * 20) + "\n# Sneaky Second\n"
        with self.assertRaises(Exception):
            extract_title(md)

    # --- realistic document ---
    def test_full_page_document(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)

## Reasons I like Tolkien

1. Gandalf
2. Bilbo
"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")


if __name__ == "__main__":
    unittest.main()