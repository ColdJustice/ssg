import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "Click Me!", None, { "href": "https://boot.dev", "target": "_blank"})
        expected = " href=\"https://boot.dev\" target=\"_blank\""
        self.assertEqual(expected, node.props_to_html())

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "Ohhhhhh... I'm a paragraph and I'm okay...", None, None)
        expected = ""
        self.assertEqual(expected, node.props_to_html())

    def test_repr(self):
        child = HTMLNode("b", "You really should be using strong instead of b", None, None)
        node = HTMLNode("p", "Ohhhhhh... I'm a paragraph and I'm okay...", [child], None)
        expected = "HTMLNode(\"p\", \"Ohhhhhh... I'm a paragraph and I'm okay...\", [1 children], None)"
        self.assertEqual(expected, repr(node))

    def test_repr_with_props(self):
        node = HTMLNode("a", "Click Me!", None, { "href": "https://boot.dev", "target": "_blank"})
        expected = "HTMLNode(\"a\", \"Click Me!\", None, {'href': 'https://boot.dev', 'target': '_blank'})"
        self.assertEqual(expected, repr(node))


if __name__ == "__main__":
    unittest.main()