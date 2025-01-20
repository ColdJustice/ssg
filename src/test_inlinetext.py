import unittest

from inlinetext import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestInlineText(unittest.TestCase):
    #
    # spit_nodes_delimiter() tests
    #
    def test_split_nodes_delimiter_empty_list(self):
        old_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = []
        self.assertEqual(len(expected), len(new_nodes))


    def test_split_nodes_delimiter_non_text_only_node(self):
        old_nodes = [TextNode("you bettah shop around!", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.ITALIC)
        expected = [
            TextNode("you bettah shop around!", TextType.BOLD)
        ]
        self.assertEqual(len(expected), len(new_nodes))

    
    def test_split_nodes_delimiter_single_item(self):
        old_nodes = [TextNode("My mama tole me **you bettah shop around!**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("My mama tole *me* ", TextType.TEXT),
            TextNode("you bettah shop around!", TextType.BOLD)
        ]
        self.assertEqual(len(expected), len(new_nodes))
        self.assertEqual("you bettah shop around!", new_nodes[1].text)


    def test_split_nodes_delimiter_complex(self):
        old_nodes = [
            TextNode("My mama tole *me* ", TextType.TEXT),
            TextNode("you bettah shop around!", TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("My mama tole *me* ", TextType.TEXT),
            TextNode("me", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("you bettah shop around!", TextType.BOLD)
        ]
        self.assertEqual(len(expected), len(new_nodes))
        self.assertEqual(expected[1], new_nodes[1])
        self.assertEqual(expected[2], new_nodes[2])
        

    def test_split_nodes_delimiter_successive_calls(self):
        old_nodes = [
            TextNode("When writing *Clean Code* you want to **avoid** mistakes like `x/0 * 5`", TextType.TEXT),
        ]
        new_nodes1 = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter(new_nodes1, "**", TextType.BOLD)
        new_nodes3 = split_nodes_delimiter(new_nodes2, "*", TextType.ITALIC)
        expected = [
            TextNode("When writing ", TextType.TEXT),
            TextNode("Clean Code", TextType.ITALIC),
            TextNode(" you want to ", TextType.TEXT),
            TextNode("avoid", TextType.BOLD),
            TextNode(" mistakes like ", TextType.TEXT),
            TextNode("x/0 * 5", TextType.CODE)
        ]
        self.assertEqual(len(expected), len(new_nodes3))


    #
    # extract_markdown_images() tests
    #
    def test_extract_markdown_images_lesson_example(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected, result)

    def test_extract_markdown_links_does_not_see_images_as_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(expected, result)

    #
    # extract_markdown_links() tests
    #
    def test_extract_markdown_links_lesson_example(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(expected, result)


    def test_split_nodes_image_lesson_example(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_link_lesson_example(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_notes_link_with_trailing_text(self):
        node = TextNode("[link1](https://google.com) is a great place to start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, url="https://google.com"),
            TextNode(" is a great place to start", TextType.TEXT)
        ]
        self.assertEqual(expected, new_nodes)


    def test_text_to_textnodes_lesson_example(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.maxDiff = None
        self.assertEqual(expected, nodes)


    def test_text_to_textnodes_with_initial_link(self):
        text = "[boot.dev](https://boot.dev) is an excellent resource"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("boot.dev", TextType.LINK, url="https://boot.dev"),
            TextNode(" is an excellent resource", TextType.TEXT)
        ]
        self.assertEqual(expected, nodes)

if __name__ == "__main__":
    unittest.main()