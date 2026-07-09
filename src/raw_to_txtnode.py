from textnode import TextType , TextNode
import re

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


def extract_markdown_images(text: str) -> list[tuple]:
   return re.findall(r"!\[(.*?)\]\((.*?)\)", text)



def extract_markdown_links(text: str) -> list[tuple]:

   return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)




def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
   output: list[TextNode] = []

   
   for old_node in old_nodes:

      if old_node.text_type != TextType.TEXT:
         output.append(old_node)
         continue

      alt_urls: list[tuple] = extract_markdown_images(old_node.text)

      remaining: str = old_node.text

      for tple in alt_urls:
         sections = remaining.split(f"![{tple[0]}]({tple[1]})", 1)

         if sections[0]:
            output.append( TextNode(
                  text= sections[0],
                  text_type= TextType.TEXT
               ))
            
         output.append(TextNode(
               text= tple[0],
               text_type= TextType.IMAGE,
               url= tple[1]
            ))
                  
         remaining = sections[1]

      if remaining:
         output.append(TextNode(
            remaining,
            TextType.TEXT
         ))
      
   return output



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]: 
   output: list[TextNode] = []

   for old_node in old_nodes:
      
      if old_node.text_type != TextType.TEXT:
         output.append(old_node)
         continue


      txt_url_extracts: list[tuple] = extract_markdown_links(old_node.text)

      tbp_txt: str =  old_node.text

      for extract in txt_url_extracts:
         link_txt = extract[0]
         link_url = extract[1]

         delim: str = f"[{link_txt}]({link_url})"

         sections: list[str] = tbp_txt.split(delim, maxsplit= 1)

         pre_delim = sections[0]
         post_delim = sections[1]

         if not pre_delim:
            output.append(TextNode(link_txt, TextType.LINK, link_url))
            tbp_txt = sections[1]
            continue

         output.append(TextNode(pre_delim, TextType.TEXT))
         output.append(TextNode(link_txt, TextType.LINK,link_url))


         tbp_txt = post_delim

      if tbp_txt:  
         output.append(TextNode(tbp_txt, TextType.TEXT))

   return output

def text_to_textnodes(raw_text: str) -> list[TextNode]:
   nodes: list[TextNode] = [TextNode(raw_text, TextType.TEXT)]
   # no props
   pass1 = split_nodes_delimiter(nodes, '**', TextType.BOLD)
   pass2 = split_nodes_delimiter(pass1, "_", TextType.ITALIC)
   pass3 = split_nodes_delimiter(pass2, '`', TextType.CODE)

   # img and links
   pass4 = split_nodes_image(pass3)
   pass5 = split_nodes_link(pass4)

   return pass5