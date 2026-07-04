from __future__ import annotations

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict = props

    def to_html(self):
        raise NotImplementedError
    
    
    def props_to_html(self):
        if not self.props:
             return ""
        
        result: str = ""
        for attribute in self.props:
             
             result += f' {attribute}="{self.props[attribute]}"'
        
        return result
    


    def __repr__(self):
         return f"HTMLNode(\nTAG = {self.tag},\nVALUE = {self.value},\n CHILDREN = {self.children},\n PROPS = {self.props})"
    

class LeafNode(HTMLNode):
     
     def __init__(self, tag, value, props = None):
          super().__init__(tag=tag, value=value, props=props)

    
     def to_html(self):
          if self.value is None:
               raise ValueError('All leaf nodes must have a value!')
          
          if not self.tag:
               return str(self.value)
                   
          return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
     
     def __repr__(self):
          
          return f"LeafNode (\nTAG = {self.tag},\nVALUE = {self.value}, \n PROPS = {self.props})"

class ParentNode(HTMLNode):
     
     def __init__(self, tag, children , props = None):
          super().__init__(tag, children=children, props=props)

     def to_html(self):
          
          if self.tag is None:
               raise ValueError('ParentNode must have a tag!')
          
          if self.children is None:
               raise ValueError('ParentNode must have childern!')
          
          children_to_html_result:str = ''
          for child in self.children:
               children_to_html_result += child.to_html()

          
          return f'<{self.tag}{self.props_to_html()}>{children_to_html_result}</{self.tag}>'