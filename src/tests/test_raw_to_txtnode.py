import unittest

from textnode import TextType, TextNode
from raw_to_txtnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_same_delimiter(self):
        node = TextNode("`one` and `two` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("one", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" at start", TextType.TEXT),
            ],
        )

    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_multiple_input_nodes(self):
        node1 = TextNode("text with `code`", TextType.TEXT)
        node2 = TextNode("already italic", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
        )

    def test_unbalanced_delimiter_raises(self):
        node = TextNode("This is `broken markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


    class TestExtractMarkdown(unittest.TestCase):
        def test_extract_image_single(self):
            matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        def test_extract_image_multiple(self):
            matches = extract_markdown_images(
                "![rick](https://i.imgur.com/aKaOqIh.gif) and ![obi](https://i.imgur.com/fJRm4Vk.jpeg)"
            )
            self.assertListEqual(
                [
                    ("rick", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ],
                matches,
            )

        def test_extract_image_none(self):
            self.assertListEqual([], extract_markdown_images("no images here"))

        def test_extract_link_single(self):
            matches = extract_markdown_links(
                "This is a link [to boot dev](https://www.boot.dev)"
            )
            self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

        def test_extract_link_multiple(self):
            matches = extract_markdown_links(
                "[to boot dev](https://www.boot.dev) and [to yt](https://www.youtube.com/@bootdotdev)"
            )
            self.assertListEqual(
                [
                    ("to boot dev", "https://www.boot.dev"),
                    ("to yt", "https://www.youtube.com/@bootdotdev"),
                ],
                matches,
            )

        def test_extract_link_none(self):
            self.assertListEqual([], extract_markdown_links("no links here"))

        def test_link_does_not_match_image(self):
            matches = extract_markdown_links(
                "An image ![alt](https://example.com/x.png) here"
            )
            self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()