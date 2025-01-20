import unittest

from converter import markdown_to_html_node
from leafnode import LeafNode
from parentnode import ParentNode

class TestConverter(unittest.TestCase):
    #
    # Paragraph tests
    #
    def test_converter_test_single_paragraph(self):
        markdown = "Hello, world!\nI'm here to make this a better place!"
        node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            LeafNode("p", "Hello, world!\nI'm here to make this a better place!", None)
        ], None)
        self.assertEqual(expected.to_html(), node.to_html())

    def test_converter_with_single_paragraph_with_inline_stuff(self):
        markdown = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None,"This is "),
                LeafNode("b", "text"),
                LeafNode(None, " with an "),
                LeafNode("i", "italic"),
                LeafNode(None, " word and a "),
                LeafNode("code", "code block"),
                LeafNode(None, " and an "),
                LeafNode("img", "", {"src":"https://i.imgur.com/fJRm4Vk.jpeg", "alt":"obi wan image"}),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href" : "https://boot.dev"}),
            ])
        ])
        self.maxDiff = None
        self.assertEqual(expected.to_html(), node.to_html())


    def test_converter_with_level_one_heading(self):
        markdown = "# *The Great Sacrifice*"
        node = markdown_to_html_node(markdown)
        expected = "<div><h1><i>The Great Sacrifice</i></h1></div>"
        self.assertEqual(expected, node.to_html())

    def test_converter_with_level_six_heading(self):
        markdown = "###### **The Great Sacrifice**"
        node = markdown_to_html_node(markdown)
        expected = "<div><h6><b>The Great Sacrifice</b></h6></div>"
        self.assertEqual(expected, node.to_html())

    def test_converter_with_simple_blockquote(self):
        markdown = ">To be or not to be?\n>That is the question."
        node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode(None, "To be or not to be?\nThat is the question.")
            ])
        ])
        self.assertEqual(expected.to_html(), node.to_html())


    def test_converter_with_code(self):
        markdown="```py\nprint(\"Hello World!\")\nprint(\"Goodbye World!\")\n```"
        node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("pre", [
                LeafNode("code", "print(\"Hello World!\")\nprint(\"Goodbye World!\")")
            ])
        ])
        self.assertEqual(expected.to_html(), node.to_html())
        

    def test_converter_with_complex_unordered_list(self):
        markdown = """* [wiki](https://wikipedia.org/)
* ![Obi-wan](https://i.imgur.com/fJRm4Vk.jpeg)
- and the *best candy of all time!*"""
        node = markdown_to_html_node(markdown)
        expected = ParentNode("div", {
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode("a", "wiki", {"href":"https://wikipedia.org/"})
                ]),
                ParentNode("li", [
                    LeafNode("img", "", {"src":"https://i.imgur.com/fJRm4Vk.jpeg", "alt":"Obi-wan"})
                ]),
                ParentNode("li", [
                    LeafNode(None, "and the "),
                    LeafNode("i", "best candy of all time!")
                ])
            ])
        })
        self.assertEqual(expected.to_html(), node.to_html())


    def test_converter_with_long_ordered_list(self):
        markdown = """1. One
2. Two
3. Three
4. Four
5. Five
6. Six
7. Seven
8. Eight
9. Nine
10. Ten"""
        node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "One")]),
                ParentNode("li", [LeafNode(None, "Two")]),
                ParentNode("li", [LeafNode(None, "Three")]),
                ParentNode("li", [LeafNode(None, "Four")]),
                ParentNode("li", [LeafNode(None, "Five")]),
                ParentNode("li", [LeafNode(None, "Six")]),
                ParentNode("li", [LeafNode(None, "Seven")]),
                ParentNode("li", [LeafNode(None, "Eight")]),
                ParentNode("li", [LeafNode(None, "Nine")]),
                ParentNode("li", [LeafNode(None, "Ten")])
            ])
        ])
        self.assertEqual(expected.to_html(), node.to_html())


if __name__ == "__main__":
    unittest.main()