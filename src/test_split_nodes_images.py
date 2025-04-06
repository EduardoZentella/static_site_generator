import unittest

from textnode import TextNode, TextType
from utils import split_nodes_image

class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode("Texto ![imagen](img.png) fin", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("Texto ", TextType.NORMAL_TEXT),
            TextNode("imagen", TextType.IMAGE, "img.png"),
            TextNode(" fin", TextType.NORMAL_TEXT),
        ])

    def test_image_at_start(self):
        node = TextNode("![primer](first.png) texto", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("primer", TextType.IMAGE, "first.png"),
            TextNode(" texto", TextType.NORMAL_TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode("Texto final ![ultima](end.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("Texto final ", TextType.NORMAL_TEXT),
            TextNode("ultima", TextType.IMAGE, "end.png"),
        ])

    def test_empty_alt_text(self):
        node = TextNode("![](url.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("", TextType.IMAGE, "url.png"),
        ])

    def test_no_images(self):
        node = TextNode("Texto sin imágenes", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_skip_non_normal_nodes(self):
        node1 = TextNode("**bold**", TextType.BOLD_TEXT)
        node2 = TextNode("Texto ![img](img.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertEqual(new_nodes, [
            node1,
            TextNode("Texto ", TextType.NORMAL_TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
        ])

    def test_empty_text_parts(self):
        node = TextNode("![sola](sola.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("sola", TextType.IMAGE, "sola.png"),
        ])

    def test_recursive_split(self):
        node = TextNode(
            "![a](a.png)![b](b.png)", 
            TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("a", TextType.IMAGE, "a.png"),
            TextNode("b", TextType.IMAGE, "b.png"),
        ])

    def test_invalid_node_type(self):
        with self.assertRaises(TypeError):
            split_nodes_image([TextNode("text", TextType.NORMAL_TEXT), "not a node"])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ]
        )
