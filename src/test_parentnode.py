import unittest

from leafnode import LeafNode
from parentnode import ParentNode


tagRequiredValueErrorText = "a tag is required for a parent node"
childrenRequiredValueErrorText = "at least one child is required for a parent node"

class TestParentNode(unittest.TestCase):
    def test_parent_with_no_tag(self):
        node = ParentNode(None, None, None )
        with self.assertRaises(ValueError) as context:
            html = node.to_html()

        self.assertEqual(tagRequiredValueErrorText, str(context.exception))
    

    def test_parent_with_empty_tag(self):
        node = ParentNode("    ", "    ", None)
        with self.assertRaises(ValueError) as context:
            html = node.to_html()

        self.assertEqual(tagRequiredValueErrorText, str(context.exception))
    

    def test_parent_with_no_child(self):
        node = ParentNode("body", None, None )
        with self.assertRaises(ValueError) as context:
            html = node.to_html()

        self.assertEqual(childrenRequiredValueErrorText, str(context.exception))
    

    def test_parent_with_empty_child(self):
        node = ParentNode("body", [], None)
        with self.assertRaises(ValueError) as context:
            html = node.to_html()

        self.assertEqual(childrenRequiredValueErrorText, str(context.exception))

    
    def test_parent_with_simple_hierarchy(self):
        children = [
            LeafNode(None, "Welcome to "),
            LeafNode("em", "THE JUNGLE!")
        ]
        parent = ParentNode("p", children, {"hidden": "hidden"})
        expected = "<p hidden=\"hidden\">Welcome to <em>THE JUNGLE!</em></p>"
        self.assertEqual(expected, parent.to_html())

    def test_parent_with_complex_hierarchy(self):
        h1 = LeafNode("h1", "Wyrmlings Unite!")
        untagged1 = LeafNode(None, "I'm sure that you've all read ")
        a = LeafNode("a", "this article")
        untagged2 = LeafNode(None, " by now and are probably ")
        em = LeafNode("em", "as mad as I am")
        untagged3 = LeafNode(None, " about it.")
        p  = ParentNode("p", [untagged1, a, untagged2, em, untagged3])
        body = ParentNode("body", [h1, p])

        expected="<body><h1>Wyrmlings Unite!</h1><p>I'm sure that you've all read <a>this article</a> by now and are probably <em>as mad as I am</em> about it.</p></body>"
        self.assertEqual(expected, body.to_html())


if __name__ == "__main__":
    unittest.main()