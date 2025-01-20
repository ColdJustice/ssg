import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_text_to_html_with_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            html = node.to_html()

        self.assertEqual("a value is required for a leaf node", str(context.exception))

    
    def test_text_to_html_with_tag(self):
        node = LeafNode("p", "paragraph")
        expected = "<p>paragraph</p>"
        self.assertEqual(expected, node.to_html())


    def test_text_to_html_with_no_tag(self):
        node = LeafNode(None, "paragraph")
        expected = "paragraph"
        self.assertEqual(expected, node.to_html())


if __name__ == "__main__":
    unittest.main()