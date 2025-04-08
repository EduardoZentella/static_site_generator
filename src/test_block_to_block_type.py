import unittest
from blocknode import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## This is a subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "### This is a sub-subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> This is a quote.\n> It has multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> This is a quote.\n> It has multiple lines.\n> And it ends here."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    