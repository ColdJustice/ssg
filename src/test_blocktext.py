import unittest

from blocktext import block_to_block_type, extract_title, markdown_to_blocks

class TestBlockText(unittest.TestCase):
    def test_extract_title_found(self):
        text = """

        
        
# THE BIG STORY
## JOE'S BIG DAY"""
        title = extract_title(text)
        expected = "THE BIG STORY"
        self.assertEqual(expected, title)


    def test_extract_title_found_multiple(self):
        text = "# THE BIG STORY\nwaffles\n# ANOTHER BIG STORY!"
        title = extract_title(text)
        expected = "THE BIG STORY"
        self.assertEqual(expected, title)


    def test_markdown_to_blocks_lesson_example(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item")"""
        blocks = markdown_to_blocks(text)
        self.assertTrue(len(blocks) == 3)

    def test_markdown_to_blocks_extra_whitespace_removed(self):
        text = """
  # This is a heading  
    
  This is a paragraph of text. It has some **bold** and *italic* words inside of it.  

  * This is the first list item in a list block  
  * This is a list item  
  * This is another list item")"""
        blocks = markdown_to_blocks(text)
        self.assertTrue(len(blocks) == 3)
        self.assertTrue(blocks[0][0] != " ")
        self.assertTrue(blocks[0][-1] != " ")

    def test_markdown_to_blocks_extra_blank_lines_removed(self):
        text = """
  # This is a heading  
    
  



  This is a paragraph of text. It has some **bold** and *italic* words inside of it.  

  



  * This is the first list item in a list block  
  * This is a list item  
  * This is another list item")
  """
        blocks = markdown_to_blocks(text)
        self.assertTrue(len(blocks) == 3)
        self.assertTrue(blocks[0][0] != " ")
        self.assertTrue(blocks[0][-1] != " ")

    #
    # block_to_block_type() tests
    #
    def test_block_to_block_type_heading1(self):
        type = block_to_block_type("# A Miracle")
        self.assertEqual("heading", type)


    def test_block_to_block_type_heading6(self):
        type = block_to_block_type("###### A Miracle")
        self.assertEqual("heading", type)


    def test_block_to_block_type_heading7(self):
        type = block_to_block_type("####### A Miracle")
        self.assertEqual("paragraph", type)


    def test_block_to_block_type_heading_no_space(self):
        type = block_to_block_type("#A Miracle")
        self.assertEqual("paragraph", type)

    def test_block_to_block_type_paragraph(self):
        type = block_to_block_type("""Sentence 1
sentence 2
sentence 3
sentence 4""")
        self.assertEqual("paragraph", type)

    def test_block_to_block_type_code_good(self):
        type = block_to_block_type("""```
#this is comment
print("hello world")
```""")
        self.assertEqual("code", type)

    def test_block_to_block_type_code_bad(self):
        type = block_to_block_type("""```
#This is a comment
print("hello world")""")
        self.assertEqual("paragraph", type)

    def test_block_to_block_type_quote_good(self):
        type = block_to_block_type(""">It was the best of times
>It was the worst of times""")
        self.assertEqual("quote", type)
        
    def test_block_to_block_type_quote_bad(self):
        type = block_to_block_type(""">It was the best of times
It was the worst of times""")
        self.assertEqual("paragraph", type)

    def test_block_to_block_type_unordered_list(self):
        type = block_to_block_type("""* Testing
* Testing
* 1, 2, 3""")
        self.assertEqual("unordered list", type)


    def test_block_to_block_type_unordered_mixed(self):
        type = block_to_block_type("""* Testing
* Testing
- 1, 2, 3""")
        self.assertEqual("unordered list", type)

    def test_block_to_block_type_unordered_bad(self):
        type = block_to_block_type("""* Testing
* Testing
1. 2, 3""")
        self.assertEqual("paragraph", type)

    def test_block_to_block_type_ordered_good(self):
        type = block_to_block_type("""1. Testing
2. Testing
3. 1, 2, 3""")
        self.assertEqual("ordered list", type)

    def test_block_to_block_type_ordered_not_ordered(self):
        type = block_to_block_type("""1. Testing
2. Testing
1. 1, 2, 3""")
        self.assertEqual("paragraph", type)


if __name__ == "__main__":
    unittest.main()