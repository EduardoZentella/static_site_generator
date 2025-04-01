class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def add_to_html(self):
        raise NotImplementedError("This method should be implemented in subclasses")
    
    def props_to_html(self):
        return "".join(list(map(lambda prop: f' {prop[0]}="{prop[1]}"', self.props.items())))
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"