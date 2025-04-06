import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.NORMAL_TEXT),
        ])

    def test_split_multiple_delimiters(self):
        node = TextNode("a **b** c **d** e", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.NORMAL_TEXT),
            TextNode("b", TextType.BOLD_TEXT),
            TextNode(" c ", TextType.NORMAL_TEXT),
            TextNode("d", TextType.BOLD_TEXT),
            TextNode(" e", TextType.NORMAL_TEXT),
        ])

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This `has unclosed delimiter", TextType.NORMAL_TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertIn("Unmatched delimiter '`' in text", str(context.exception))

    def test_non_textnode_input_raises_error(self):
        with self.assertRaises(TypeError) as context:
            split_nodes_delimiter(["not a TextNode"], "`", TextType.CODE_TEXT)
        self.assertIn("All elements in old_nodes must be instances of TextNode", str(context.exception))

    def test_skip_non_normal_text_nodes(self):
        node1 = TextNode("**bold**", TextType.BOLD_TEXT)
        node2 = TextNode("Normal text with `code`", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            node1,
            TextNode("Normal text with ", TextType.NORMAL_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode("", TextType.NORMAL_TEXT),
        ])

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**bold text**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.NORMAL_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode("", TextType.NORMAL_TEXT),
        ])

    def test_empty_text_after_split(self):
        node = TextNode("``", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.NORMAL_TEXT),
            TextNode("", TextType.CODE_TEXT),
            TextNode("", TextType.NORMAL_TEXT),
        ])

    def test_mixed_nodes_in_old_nodes(self):
        node1 = TextNode("Normal **text**", TextType.NORMAL_TEXT)
        node2 = TextNode("Already bold", TextType.BOLD_TEXT)
        node3 = TextNode("Another `code`", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("Normal ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode("", TextType.NORMAL_TEXT),
            node2,
            TextNode("Another `code`", TextType.NORMAL_TEXT),
        ])