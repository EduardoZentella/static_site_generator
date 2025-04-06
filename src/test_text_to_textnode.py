import unittest
from textnode import TextNode, TextType
from utils import text_to_textnodes

class TestTextToTextNode(unittest.TestCase):
    def test_multiple_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        self.assertEqual(result, expected)
    
    def test_all_element_types(self):
        text = "This is **bold** with an ![image](img.png) and _italic_ text `code`, plus [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text ", TextType.NORMAL_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(", plus ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_nested_delimiters_in_link_text(self):
        text = "A [link with **bold** text](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("A ", TextType.NORMAL_TEXT),
            TextNode("link with **bold** text", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)
    
    def test_empty_input(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            text_to_textnodes(123)

    def test_multiple_images_links(self):
        text = "![img1](1.png)x[link1](1.com)![img2](2.png)y[link2](2.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("img1", TextType.IMAGE, "1.png"),
            TextNode("x", TextType.NORMAL_TEXT),
            TextNode("link1", TextType.LINK, "1.com"),
            TextNode("img2", TextType.IMAGE, "2.png"),
            TextNode("y", TextType.NORMAL_TEXT),
            TextNode("link2", TextType.LINK, "2.com"),
        ]
        self.assertEqual(result, expected)
    
    def test_image_link_no_space(self):
        text = "![img](img.png)[link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)
