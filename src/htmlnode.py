class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        pass
    