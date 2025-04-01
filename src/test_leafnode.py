import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_value_required(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)
            
    def test_to_html_no_tag(self):
        node = LeafNode("Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_to_html_empty_value(self):
        node = LeafNode("", "span")
        self.assertEqual(node.to_html(), "<span></span>")

    def test_to_html_props_no_tag(self):
        node = LeafNode( "Hello", None, {"class": "greeting"})
        self.assertEqual(node.to_html(), "Hello")
    
    def test_to_html_props_special_chars(self):
        node = LeafNode("", "img", {"alt": 'Image"1'})
        self.assertEqual(node.to_html(), '<img alt="Image"1"></img>')
    
    def test_repr_special_chars_props(self):
        node = LeafNode("", "img", {"alt": 'Image"1'})
        expected_repr = 'LeafNode(img, , {"alt": "Image\\"1"})'
        self.assertEqual(repr(node), expected_repr)
    
    def test_repr_no_tag(self):
        node = LeafNode("Raw text")
        self.assertEqual(repr(node), "LeafNode(Raw text)")

    def test_leaf_to_html_p(self):
        node = LeafNode("Hello, world!", "p")
        node2 = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_rpr(self):
        node = LeafNode("Hello, world!", "p")
        node2 = LeafNode( "Click me!", "a", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!)")
        self.assertEqual(repr(node2), 'LeafNode(a, Click me!, {"href": "https://www.google.com"})')