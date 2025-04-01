import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_children_initialization(self):
        child1 = HTMLNode("span")
        child2 = HTMLNode("b")
        node = HTMLNode(children=[child1, child2])
        self.assertEqual(node.children, [child1, child2])
        node_with_none_children = HTMLNode(children=None)
        self.assertEqual(node_with_none_children.children, None)
    
    def test_props_initialization(self):
        props = {"id": "main", "data-key": "123"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props, props)
        node_with_none_props = HTMLNode(props=None)
        self.assertEqual(node_with_none_props.props, None)
    
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"id": "container"})
        self.assertEqual(node.props_to_html(), ' id="container"')
    
    def test_props_to_html_special_characters(self):
        node = HTMLNode(props={"alt": "Image \"Logo\""})
        self.assertEqual(node.props_to_html(), ' alt="Image \"Logo\""')
    
    def test_repr_with_none_value(self):
        node = HTMLNode("br", props = {"id": "br1"})
        self.assertEqual(repr(node), 'HTMLNode(br, {"id": "br1"})')
    
    def test_repr_all_defaults(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode()")

    def test_props_to_html(self):
        node = HTMLNode("p", "this is a paragraph", props = {"style": "color: red", "class": "text"})
        node2 = HTMLNode("p")
        self.assertEqual(node.props_to_html(), ' style="color: red" class="text"')
        self.assertEqual(node2.props_to_html(), '')
    
    def test_repr(self):
        node = HTMLNode("p", "this is a paragraph", props = {"style": "color: red", "class": "text"})
        node2 = HTMLNode("p")
        self.assertEqual(repr(node), 'HTMLNode(p, this is a paragraph, {"style": "color: red", "class": "text"})')
        self.assertEqual(repr(node2), "HTMLNode(p)")
    
    def test_add_to_html(self):
        node = HTMLNode("p", "this is a paragraph", props = {"style": "color: red", "class": "text"})
        try:
            node.add_to_html()
        except NotImplementedError:
            self.assertTrue(True)
