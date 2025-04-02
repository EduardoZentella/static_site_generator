from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    """
    Converts a TextNode to a LeafNode.
    """
    if not isinstance(text_node, TextNode):
        raise TypeError("text_node must be an instance of TextNode")
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC_TEXT:
            return LeafNode(text_node.text, "i")
        case TextType.CODE_TEXT:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Converts a list of TextNodes with delimiters into a list of TextNodes.
    """
    new_nodes = []
    
    def split_and_create_nodes(text, delimiter, text_type):
        parts = text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text}")
        return [
            TextNode(part, text_type if i % 2 else TextType.NORMAL_TEXT)
            for i, part in enumerate(parts)
        ]

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise TypeError("All elements in old_nodes must be instances of TextNode")
        
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_and_create_nodes(node.text, delimiter, text_type))    
    return new_nodes