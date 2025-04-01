from htmlnode import HTMLNode
import json

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode requires a tag.")
        if not children:
            raise ValueError("ParentNode requires at least one child.")
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    