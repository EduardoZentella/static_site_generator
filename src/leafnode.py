from htmlnode import HTMLNode
import json

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value.")
        super().__init__(tag=tag, value=value, children=[], props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        json_props = json.dumps(self.props)
        return f"LeafNode({self.tag}, {self.value}, {json_props})"
    
