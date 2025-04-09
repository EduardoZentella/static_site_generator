from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Converts a block to its corresponding BlockType.
    """
    lines = block.strip().split("\n")
    
    if all(line.startswith("#") and line.lstrip("#").startswith(" ") for line in lines):
        return BlockType.HEADING
    
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(line.split(". ", 1)[0].isdigit() and int(line.split(". ", 1)[0]) == idx + 1 
           for idx, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH