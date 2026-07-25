from enum import Enum
import re

from textnode import TextNode, TextType, text_node_to_html_node
from raw_to_txtnode import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UL = 'unordered_list'
    OL = 'ordered_list'



def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str]= []

    raw_blocks: list[str] = markdown.split('\n\n')

    for raw_block in raw_blocks:
        raw_block = raw_block.strip()
        if not raw_block:
            continue
        blocks.append(raw_block)
    
    return blocks


def block_to_block_type(mdblock: str) -> BlockType:
    # BlockType HEADING check
    if re.match(r"^#{1,6} ", mdblock):
        return BlockType.HEADING

    # BlockType CODE Check
    if mdblock.startswith('```\n') and mdblock.endswith('```'):
        return BlockType.CODE

    #List of lines for QUOTE , OL, UL
    lines: list[str] = mdblock.splitlines()

    # Block Type QUOTE Check
    is_block: bool = False
    for line in lines:
        if line.startswith(">"):
            is_block = True
        else:
            is_block = False
            break

    if is_block:
        return BlockType.QUOTE

    # Block Type UL Check
    is_ul: bool = False
    for line in lines:
        if line.startswith("- "):
            is_ul = True
        else:
            is_ul = False
            break
    if is_ul:
        return BlockType.UL

    # Block Type OL Check
    is_ol: bool = False
    ol_counter: int = 1
    for line in lines:
        if line.startswith(f"{ol_counter}. "):
            is_ol = True
            ol_counter += 1
        else:
            is_ol = False
            break
            
    if is_ol:
        return BlockType.OL

    return BlockType.PARAGRAPH



def text_to_children(text: str) -> list[HTMLNode]:
    html_nodes: list[HTMLNode] = []
    txt_nodes: list[TextNode] = text_to_textnodes(text)

    for txt_node in txt_nodes:
        html_nodes.append(text_node_to_html_node(txt_node))

    return html_nodes


def paragraph_to_html_node(block: str) -> ParentNode:
    no_new_line_block: str = " ".join(block.splitlines())
    return ParentNode('p', text_to_children(no_new_line_block))


def heading_to_html_node(block: str) -> ParentNode:
    hash_count: int = 0
    for char in block:
        if char == "#":
            hash_count += 1

        if hash_count == 6:
            break

        if char != '#':
            break

    tag:str = f'h{hash_count}'

    return ParentNode(tag, block)