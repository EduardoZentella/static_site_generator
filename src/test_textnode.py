import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, TextNode("This is a different text node", TextType.NORMAL_TEXT))
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a different text node", TextType.NORMAL_TEXT)
        node3 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, normal, https://www.boot.dev)")
        self.assertEqual(repr(node2), "TextNode(This is a different text node, normal, None)")
        self.assertNotEqual(repr(node), repr(node3))



if __name__ == "__main__":
    unittest.main()