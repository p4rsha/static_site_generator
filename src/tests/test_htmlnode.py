import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_two_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(props={"class": "main-heading"})
        self.assertEqual(node.props_to_html(), ' class="main-heading"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_no_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_no_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_parent_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "hi")],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container"><span>hi</span></div>',
        )

    def test_to_html_deeply_nested(self):
        leaf = LeafNode("b", "deep")
        level3 = ParentNode("span", [leaf])
        level2 = ParentNode("p", [level3])
        level1 = ParentNode("div", [level2])
        self.assertEqual(
            level1.to_html(),
            "<div><p><span><b>deep</b></span></p></div>",
        )

    def test_to_html_no_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "x")]).to_html()

    def test_to_html_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()


if __name__ == "__main__":
    unittest.main()