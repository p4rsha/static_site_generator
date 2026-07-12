from enum import Enum # Enum is a class that stores named choices , .name and .value
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text:str , text_type:TextType , url: str | None= None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        
        equal_text = self.text == other.text
        equal_type = self.text_type == other.text_type
        equal_url = self.url == other.url

        return equal_text and equal_type and equal_url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag= None, value= text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value= text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag= 'i', value= text_node.text)
    
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag= 'code', value= text_node.text)
    
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag= 'a', value= text_node.text, props= {'href' : text_node.url})
    
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag='img' , value="" , props= {'src' : text_node.url , 'alt': text_node.text })

    raise Exception('INVALID TextNode')