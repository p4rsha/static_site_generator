from enum import Enum # Enum is a class that stores named choices , .name and .value

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text:str , text_type:TextType , url: str = None):
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
    
    
