import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "this is a paragraph", [],{"style": "color: red", "class": "text"})
        node2 = HTMLNode("p")
        self.assertEqual(node.props_to_html(), ' style="color: red" class="text"')
        self.assertEqual(node2.props_to_html(), '')
    
    def test_repr(self):
        node = HTMLNode("p", "this is a paragraph", [],{"style": "color: red", "class": "text"})
        node2 = HTMLNode("p")
        self.assertEqual(repr(node), "HTMLNode(p, this is a paragraph, [], {'style': 'color: red', 'class': 'text'})")
        self.assertEqual(repr(node2), "HTMLNode(p, None, [], {})")
    
    def test_add_to_html(self):
        node = HTMLNode("p", "this is a paragraph", [],{"style": "color: red", "class": "text"})
        try:
            node.add_to_html()
        except NotImplementedError:
            self.assertTrue(True)

    
if __name__ == "__main__":
    unittest.main()
