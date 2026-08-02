from pathlib import Path
from block_proc import markdown_to_html_node


def extract_title(markdown: str) -> str:
    md_liness : list[str] = markdown.splitlines()
    title_found: bool = False
    title:str = ""

    for line in md_liness:

        if line[:2] == "# ":

            if title_found:
                raise Exception('Multiple titles were spotted, the max "# " lines allowed is 1!')
            
            title = line[2:]
            title_found = True

    if not title_found:
        raise Exception("NO TITLE FOUND!")

    return title.strip()



def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:

    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")

    page_md: str = from_path.read_text()
    template: str = template_path.read_text()

    title: str = extract_title(page_md)
    page_html: str = markdown_to_html_node(page_md).to_html()

    page_pretty_html: str = template.replace("{{ Title }}" , title).replace("{{ Content }}", page_html)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(page_pretty_html)


def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path) -> None:

    for path_inside_content in dir_path_content.iterdir():

        if path_inside_content.is_file() and path_inside_content.name.endswith(".md"):
            file_name: str = path_inside_content.name.split(".", maxsplit= 1)[0]
            dest_path: Path = dest_dir_path / f"{file_name}.html"

            print(f"Generating page from {path_inside_content} to {dest_path} using {template_path}...")


            page_md: str = path_inside_content.read_text()
            template: str = template_path.read_text()


            title: str = extract_title(page_md)
            page_html: str = markdown_to_html_node(page_md).to_html()

            page_pretty_html: str = template.replace("{{ Title }}" , title).replace("{{ Content }}", page_html)

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(page_pretty_html)

        if path_inside_content.is_dir():
            deeper_dest_path: Path = dest_dir_path / path_inside_content.name
            generate_pages_recursive(path_inside_content , template_path ,  deeper_dest_path)
