import unittest
from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter

class TestUtils(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_text(self):
        node = TextNode("Bold text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        node = TextNode("Italic text", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        node = TextNode("Code text", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
    
    def test_link_text(self):
        node = TextNode("Link text", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
    
    def test_image_text(self):
        node = TextNode("Image text", TextType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "Image text"})
    
    def test_image_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["alt"], "")
        self.assertEqual(html_node.props["src"], "image.png")
        self.assertEqual(html_node.tag, "img")
    
    def test_link_missing_url(self):
        node = TextNode("Link", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["href"], None)

    def test_invalid_text_type(self):
        node = TextNode("Invalid text", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
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
