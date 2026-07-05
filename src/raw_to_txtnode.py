from textnode import TextType , TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
   output: list[TextNode] = []
   for node in old_nodes:
      if node.text_type != TextType.TEXT:
         output.append(node)
         continue
      str_components: list[str] = node.text.split(delimiter)

      if len(str_components) % 2 == 0:
         raise Exception('closing delimiter not found !!!')

      # NOTE : this indexing only works because the lesson only allows 1 .. would have to write more complex logic to allow nested
      for i in range(len(str_components)):

         comp_type = TextType.TEXT if i % 2 == 0 else text_type
         output.append(TextNode(str_components[i], comp_type))

    
   return output 
