import json
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def add_to_html(self):
        raise NotImplementedError("This method should be implemented in subclasses")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        if not isinstance(self.props, dict):
            raise TypeError("props should be a dictionary")
        return "".join(list(map(lambda prop: f' {prop[0]}="{prop[1]}"', self.props.items())))
    
    def __repr__(self):
        json_props = json.dumps(self.props) if self.props else None
        parts = []
        if self.tag is not None:
            parts.append(self.tag)
        if self.value is not None:
            parts.append(self.value)
        if self.children is not None:
            parts.append(self.children)
        if json_props is not None:
            parts.append(json_props)
        return f"{self.__class__.__name__}({', '.join(map(str, parts))})"