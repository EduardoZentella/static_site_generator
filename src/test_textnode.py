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
        self.assertEqual(repr(node2), "TextNode(This is a different text node, normal)")
        self.assertNotEqual(repr(node), repr(node3))

    def test_text_type_enum_values(self):
        self.assertEqual(TextType.NORMAL_TEXT.value, "normal")
        self.assertEqual(TextType.BOLD_TEXT.value, "bold")
        self.assertEqual(TextType.ITALIC_TEXT.value, "italic")
        self.assertEqual(TextType.CODE_TEXT.value, "code")
        self.assertEqual(TextType.LINK.value, "link")
        self.assertEqual(TextType.IMAGE.value, "image")
    
    def test_eq_different_url(self):
        node1 = TextNode("text", TextType.NORMAL_TEXT, "https://example.com")
        node2 = TextNode("text", TextType.NORMAL_TEXT, None)
        self.assertNotEqual(node1, node2)
    
    def test_eq_different_text_type(self):
        node1 = TextNode("text", TextType.BOLD_TEXT)
        node2 = TextNode("text", TextType.NORMAL_TEXT)
        self.assertNotEqual(node1, node2)
    
    def test_eq_different_text(self):
        node1 = TextNode("text1", TextType.NORMAL_TEXT)
        node2 = TextNode("text2", TextType.NORMAL_TEXT)
        self.assertNotEqual(node1, node2)
    
    def test_empty_text_node(self):
        node = TextNode("", TextType.NORMAL_TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(repr(node), "TextNode(, normal)")

    def test_url_present_for_non_link_or_image(self):
        node = TextNode("text", TextType.BOLD_TEXT, "https://example.com")
        self.assertEqual(node.url, "https://example.com")
        self.assertIn("https://example.com", repr(node))

if __name__ == "__main__":
    unittest.main()