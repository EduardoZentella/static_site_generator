import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")])
    
    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div",None)
        
    def test_to_html_multiple_children(self):
        children = [
            LeafNode("child1", "span"),
            LeafNode("child2", "span"),
            ParentNode("ul", [LeafNode("item", "li")])
        ]
        parent = ParentNode("div", children)
        self.assertEqual(
            parent.to_html(),
            "<div><span>child1</span><span>child2</span><ul><li>item</li></ul></div>"
        )
    
    def test_to_html_with_props(self):
        child = LeafNode("child", "span")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )
    
    def test_to_html_mixed_children(self):
        children = [
            LeafNode("Raw text"),
            ParentNode("p", [LeafNode("bold text", "b")])
        ]
        parent = ParentNode("div", children)
        self.assertEqual(
            parent.to_html(),
            "<div>Raw text<p><b>bold text</b></p></div>"
        )
    
    def test_repr_with_children_and_props(self):
        child = LeafNode("child", "span", {"class": "child"})
        parent = ParentNode("div", [child], {"id": "parent"})
        expected_repr = '''ParentNode(div, [LeafNode(span, child, {"class": "child"})], {"id": "parent"})'''
        self.assertEqual(repr(parent), expected_repr)
    
    def test_repr_with_no_props(self):
        child = LeafNode("child", "span")
        parent = ParentNode("div", [child])
        expected_repr = '''ParentNode(div, [LeafNode(span, child)])'''
        self.assertEqual(repr(parent), expected_repr)

    def test_to_html_with_children(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )