from utils import markdown_to_block, text_to_textnodes, text_node_to_html_node
from blocknode import block_to_block_type, BlockType
from parentnode import ParentNode
from leafnode import LeafNode

def encase_blocks(blocks):
    """
    Creates a Parent Node and assigns the blocks to it.
    """
    parent_node = ParentNode(tag="div", children=blocks)
    return parent_node

def process_block(block, block_type):
    """
    Processes a block and converts it to the appropriate HTML node.
    """
    if block_type == BlockType.HEADING:
        return convert_heading(block)
    elif block_type == BlockType.CODE:
        return convert_code(block)
    elif block_type == BlockType.QUOTE:
        return convert_quote(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return convert_ulist(block)
    elif block_type == BlockType.ORDERED_LIST:
        return convert_olist(block)
    elif block_type == BlockType.PARAGRAPH:
        return convert_paragraph(block)
    else:
        return convert_paragraph(block)

def text_to_children(text):
    """
    Converts text to a list of TextNodes.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def convert_paragraph(block):
    """
    Converts a block of text to a paragraph HTML node.
    """
    lines = block.split('\n')
    cleaned_lines = [line.strip() for line in lines]
    joined_text = ' '.join(cleaned_lines)
    children = text_to_children(joined_text)
    return ParentNode(tag="p", children=children)

def convert_heading(block):
    """
    Converts a block of text to a heading HTML node.
    """
    level = min(block.count("#"), 6)
    content = block.lstrip("#").strip()
    children = text_to_children(content)
    return ParentNode(tag=f"h{level}", children=children)

def convert_code(block):
    """
    Converts a block of code to a code HTML node.
    """
    lines = block.split('\n')
    if len(lines) < 2:
        content = block.strip('`').strip()
    else:
        content = '\n'.join(lines[1:-1]).strip()
    code_node = LeafNode(tag="code", value=content+"\n")
    pre_node = ParentNode(tag="pre", children=[code_node])
    return pre_node

def convert_quote(block):
    """
    Converts a block of text to a quote HTML node.
    """
    lines = block.split('\n')
    content = ' '.join(line.lstrip("> ").strip() for line in lines)
    children = text_to_children(content)
    return ParentNode(tag="blockquote", children=children)

def convert_ulist(block):
    """
    Converts a block of text to an unordered list HTML node.
    """
    items = block.split('\n')
    list_items = []
    for item in items:
        text = item[2:].strip()
        children = text_to_children(text)
        list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=list_items)

def convert_olist(block):
    """
    Converts a block of text to an ordered list HTML node.
    """
    items = block.split('\n')
    list_items = []
    for item in items:
        dot_pos = item.find('.')
        text = item[dot_pos+1:].strip() if dot_pos != -1 else item.strip()
        children = text_to_children(text)
        list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=list_items)

def markdown_to_html_node(markdown):
    """
    Converts a markdown string to an HTML node.
    """
    blocks = markdown_to_block(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = process_block(block, block_type)
        html_nodes.append(html_node)
    return encase_blocks(html_nodes)
