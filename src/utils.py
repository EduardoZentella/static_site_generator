from textnode import TextNode, TextType
from leafnode import LeafNode
import re

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

def split_nodes_image(old_nodes):
    """
    Converts a list of TextNodes with image delimiters into a list of TextNodes.
    """
    new_nodes = []
    def create_image_nodes_recursively(text):
        images = extract_markdown_images(text)
        if not images:
            return [TextNode(text, TextType.NORMAL_TEXT)] if text.strip() else []
        
        alt, url = images[0]
        parts = text.split(f"![{alt}]({url})", 1)
        nodes = []
        before = parts[0]
        after = parts[1] if len(parts) > 1 else ""
        if before.strip():
            nodes.append(TextNode(before, TextType.NORMAL_TEXT))
        nodes.append(TextNode(alt if alt.strip() else "", TextType.IMAGE, url))
        if after.strip():
            nodes += create_image_nodes_recursively(after)
        return nodes

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise TypeError("All elements in old_nodes must be instances of TextNode")
        
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            nodes_found = create_image_nodes_recursively(node.text)
            new_nodes.extend([node for node in nodes_found if node.text.strip() or node.text_type == TextType.IMAGE])
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Converts a list of TextNodes with link delimiters into a list of TextNodes.
    """
    new_nodes = []
    def create_link_nodes_recursively(text):
        links = extract_markdown_links(text)
        if not links:
            return [TextNode(text, TextType.NORMAL_TEXT)] if text.strip() else []
        
        link_text, url = links[0]
        parts = text.split(f"[{link_text}]({url})", 1)
        nodes = []
        before = parts[0]
        after = parts[1] if len(parts) > 1 else ""
        if before.strip():
            nodes.append(TextNode(before, TextType.NORMAL_TEXT))
        nodes.append(TextNode(link_text, TextType.LINK, url))
        if after.strip():
            nodes += create_link_nodes_recursively(after)
        return nodes

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise TypeError("All elements in old_nodes must be instances of TextNode")
        
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            nodes_found = create_link_nodes_recursively(node.text)
            new_nodes.extend([node for node in nodes_found if node.text.strip()])
    return new_nodes

def extract_markdown_images(text):
    """
    Extracts alt text and image URLs from markdown text.
    """
    pattern = r'\!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts link text and URLs from markdown text.
    """
    pattern = r'(?<!\!)\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    """
    Converts a string to a list of TextNodes.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    nodes = [TextNode(text, TextType.NORMAL_TEXT)] 
    nodes = split_nodes_image(nodes) # Images
    nodes = split_nodes_link(nodes) # Links
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT) # Bold text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT) # Italic text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT) # Code text
    return nodes

def markdown_to_block(text):
    """
    Converts a string to a list of block strings.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    
    blocks = text.split("\n\n")
    processed_blocks = []
    for block in blocks:
        lines = block.split("\n")
        cleaned_lines = filter(None, map(str.strip, lines))
        cleaned_block = "\n".join(cleaned_lines)
        if cleaned_block:
            processed_blocks.append(cleaned_block)
    
    return processed_blocks