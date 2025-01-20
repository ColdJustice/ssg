import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    #
    # (In)Equality tests
    #
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_is_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_is_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_is_not_equal(self):
        node = TextNode("This is a text node", TextType.IMAGE, "http://imgur.com")
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    #
    # __repr__ tests
    #
    def test_repr_with_no_url(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        expected = "TextNode(\"This is a text node\", TextType.IMAGE, None)"
        self.assertEqual(expected, repr(node))
        
    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://imgur.com/")
        expected = "TextNode(\"This is a text node\", TextType.IMAGE, \"https://imgur.com/\")"
        self.assertEqual(expected, repr(node))
    

    #
    # text_node_to_html_node tests
    #
    def test_text_conversion(self):
        node = TextNode("Howdy, Pardner!", TextType.TEXT)
        expected = "Howdy, Pardner!"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_bold_conversion(self):
        node = TextNode("Howdy, Pardner!", TextType.BOLD)
        expected = "<b>Howdy, Pardner!</b>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_italic_conversion(self):
        node = TextNode("Howdy, Pardner!", TextType.ITALIC)
        expected = "<i>Howdy, Pardner!</i>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_code_conversion(self):
        node = TextNode("Howdy, Pardner!", TextType.CODE)
        expected = "<code>Howdy, Pardner!</code>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_link_conversion(self):
        node = TextNode("Howdy, Pardner!", TextType.LINK, "https://howdy.partner.us")
        expected = "<a href=\"https://howdy.partner.us\">Howdy, Pardner!</a>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_image_conversion(self):
        node = TextNode("Howdy, Pardner!", TextType.IMAGE, "https://imgur.com")
        expected = "<img src=\"https://imgur.com\" alt=\"Howdy, Pardner!\"></img>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())

    

if __name__ == "__main__":
    unittest.main()