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




# Block to HTML FUNCS

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

    return ParentNode(tag, text_to_children(block[hash_count + 1:]))

def quote_to_html_node(block: str) -> ParentNode:
    clean_lines: list[str] = []
    lines_in_block: list[str] = block.splitlines()

    for line in lines_in_block:
        clean_lines.append(
            line.replace(">", "", 1).removeprefix(" ")
        )
    clean_block: str = ' '.join(clean_lines)

    return ParentNode('blockquote', text_to_children(clean_block))



def ul_to_html_node(block: str) -> ParentNode:
    li_htmls: list[ParentNode] = []
    lines:list[str] = block.splitlines()

    for line in lines:
        li_htmls.append(
            ParentNode("li", text_to_children(line[2:]))
        )

    return ParentNode("ul", li_htmls)
    


def ol_to_html_node(block: str) -> ParentNode:
    li_htmls: list[ParentNode] = []
    lines:list[str] = block.splitlines()

    for line in lines:
        li_htmls.append(
            ParentNode("li", text_to_children(line.split(". ", maxsplit= 1)[1]))
        )

    return ParentNode("ol", li_htmls)




def code_to_html_node(block: str) -> ParentNode:
    clean_block: str = block.replace('```', "").removeprefix('\n')

    return ParentNode('pre', [ParentNode('code', [text_node_to_html_node(TextNode(clean_block, TextType.TEXT))])])



'''class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UL = 'unordered_list'
    OL = 'ordered_list'
'''


def markdown_to_html_node(markdown: str) -> ParentNode:
    md_blocks: list[str] = markdown_to_blocks(markdown)

    children_html_nodes: list[HTMLNode] = []

    for md_block in md_blocks:
        block_type = block_to_block_type(md_block)
        current_node: HTMLNode | None = None
        
        if block_type is BlockType.PARAGRAPH:
            current_node = paragraph_to_html_node(md_block)

        elif block_type is BlockType.HEADING:
            current_node = heading_to_html_node(md_block)

        elif block_type is BlockType.CODE:
            current_node = code_to_html_node(md_block)

        elif block_type is BlockType.QUOTE:
            current_node = quote_to_html_node(md_block)

        elif block_type is BlockType.UL:
            current_node = ul_to_html_node(md_block)

        elif block_type is BlockType.OL:
            current_node = ol_to_html_node(md_block)

        else:
            raise Exception("Shit must have hit the fan")

        children_html_nodes.append(current_node)

    return ParentNode('div', children= children_html_nodes)